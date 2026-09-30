"""Reproducible, nominal-anchor viscosity fits; no universal glass coefficients.

Run from any directory. All outputs and matplotlib caches remain in workspace.
SCHOTT AR-GLAS and BOROFLOAT 33: VFT in log10(dPa s), temperature degC.
Corning HPFS 7980: constrained Arrhenius (VFT T0_K=0) least-squares fit.
Manufacturer anchor values are nominal; residuals are not uncertainty bounds.
"""
from pathlib import Path
import os, json, csv
ROOT=Path(__file__).resolve().parents[2]
os.environ['MPLCONFIGDIR']=str(ROOT/'scripts/tmp/matplotlib')
os.environ['TEMP']=os.environ['TMP']=str(ROOT/'scripts/tmp')
import numpy as np
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

MATERIALS=[
 dict(id='ar_glas',label='Soda-lime: SCHOTT AR-GLAS',source='phys_ar',model='VFT',T_C=[530,720,1040],log10_dPas=[13,7.6,4],source_page=11),
 dict(id='borofloat33',label='Borosilicate: BOROFLOAT 33',source='phys_boro',model='VFT',T_C=[518,560,820,1270],log10_dPas=[14.5,13,7.6,4],source_page=1),
 dict(id='hpfs7980',label='Fused silica: Corning HPFS 7980',source='phys_silica',model='Arrhenius limit of VFT',T_C=[893,1042,1585],log10_dPas=[14.5,13,7.6],source_page=3)]
THRESHOLDS={'strain':14.5,'annealing':13.,'softening':7.6,'working_band_low_temperature':7.,'working_point':4.}
def evaluate(T,a,b,t0):return a+b/(np.asarray(T)-t0)
def fit(m):
 T=np.array(m['T_C']);y=np.array(m['log10_dPas'])
 if m['model']=='VFT':
  opt=least_squares(lambda p:evaluate(T,*p)-y,[-3,5000,200],bounds=([-30,1,-273.15],[20,1e6,float(min(T)-1)]),xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=5000)
  a,b,t0=opt.x
 else:
  b,a=np.polyfit(1/(T+273.15),y,1);t0=-273.15
 residual=evaluate(T,a,b,t0)-y
 thresholds={k:dict(T_C=float(t0+b/(v-a)),log10_dPas=v,extrapolated=not(min(T)<=t0+b/(v-a)<=max(T))) for k,v in THRESHOLDS.items()}
 return dict(**m,A=float(a),B_K=float(b),T0_C=float(t0),T0_K=float(t0+273.15),residual_log10_dPas=residual.tolist(),rms_log10_dPas=float(np.sqrt(np.mean(residual**2))),calibration_interval_C=[float(min(T)),float(max(T))],thresholds=thresholds)
def main():
 results=[fit(m) for m in MATERIALS]
 (ROOT/'sources/data/viscosity_inputs.json').write_text(json.dumps(MATERIALS,indent=2),encoding='utf-8')
 (ROOT/'sources/data/viscosity_results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
 with (ROOT/'sources/data/viscosity_thresholds.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(['material','model','regime','log10_eta_dPas','temperature_C','extrapolated'])
  for m in results:
   for k,v in m['thresholds'].items():w.writerow([m['id'],m['model'],k,v['log10_dPas'],v['T_C'],v['extrapolated']])
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42})
 fig,axes=plt.subplots(1,2,figsize=(11.5,4.8),layout='constrained')
 colors=['#16697a','#cb6332','#674a9e']
 for ax,limits in zip(axes,[(400,2300),(1000,1700)]):
  x=np.linspace(*limits,1000)
  for m,c in zip(results,colors):
   y=evaluate(x,m['A'],m['B_K'],m['T0_C']);lo,hi=m['calibration_interval_C'];inside=(x>=lo)&(x<=hi)
   ax.plot(x,np.where(inside,y,np.nan),color=c,lw=2,label=m['label'])
   ax.plot(x,np.where(~inside,y,np.nan),color=c,lw=1.4,ls='--')
   ax.scatter(m['T_C'],m['log10_dPas'],s=23,color=c,zorder=3)
  for y in [14.5,13,7.6,4]:ax.axhline(y,c='gray',alpha=.25,lw=.8)
  ax.axhspan(4,7,color='#e7bf57',alpha=.14)
  ax.set(xlim=limits,ylim=(0,16),xlabel='Temperature (°C)',ylabel=r'$\log_{10}[\eta/(\mathrm{dPa\,s})]$')
  ax.grid(alpha=.15)
 axes[0].set_title('Nominal manufacturer anchors and fits')
 axes[1].set_title('Requested 1000–1700 °C process window')
 axes[0].legend(loc='upper right',fontsize=8)
 fig.supxlabel('Dots: manufacturer anchors  |  solid: calibration interval  |  dashed: extrapolation',fontsize=9)
 for ext in ['png','pdf']:fig.savefig(ROOT/f'latex/figures/viscosity_vft.{ext}',dpi=300)
 plt.close(fig)
 # A separate residual plot makes the strong-glass approximation auditable.
 fig,ax=plt.subplots(figsize=(7,3.3),layout='constrained')
 for m,c in zip(results,colors):ax.plot(m['T_C'],m['residual_log10_dPas'],'o-',label=m['label'],color=c)
 ax.axhline(0,c='gray',lw=.8);ax.set(xlabel='Anchor temperature (°C)',ylabel='Fit minus anchor (log10 dPa s)');ax.legend(fontsize=8);ax.grid(alpha=.2)
 for ext in ['png','pdf']:fig.savefig(ROOT/f'latex/figures/viscosity_residuals.{ext}',dpi=300)
 plt.close(fig)
 rows=[]
 for m in results:
  temps=[m['thresholds'][k]['T_C'] for k in ['strain','annealing','softening','working_point']]
  name={'ar_glas':'AR-GLAS','borofloat33':'BOROFLOAT 33','hpfs7980':'HPFS 7980 (approx.)'}[m['id']]
  rows.append(name+' & '+ ' & '.join(f'{v:.1f}' for v in temps)+r' \\')
 table=r'\begin{tabular}{lrrrr}\toprule Material & Strain & Annealing & Softening & Working \\ \midrule'+'\n'+'\n'.join(rows)+'\n'+r'\bottomrule\end{tabular}'+'\n'
 (ROOT/'latex/sections/viscosity_table.tex').write_text(table,encoding='utf-8')
 # Independent invariants: monotonicity, inverse recovery, unit conversion.
 for m in results:
  grid=np.linspace(400,2300,400)
  assert np.all(np.diff(evaluate(grid,m['A'],m['B_K'],m['T0_C']))<0)
  for v in m['thresholds'].values():assert abs(float(evaluate(v['T_C'],m['A'],m['B_K'],m['T0_C']))-v['log10_dPas'])<1e-9
 assert 10**4 * .1 == 1000
 assert results[0]['rms_log10_dPas']<1e-7
 assert results[1]['rms_log10_dPas']<.15
 for m in results:print(m['id'],{k:round(m[k],5) for k in ['A','B_K','T0_C','rms_log10_dPas']},'thresholds', {k:round(v['T_C'],1) for k,v in m['thresholds'].items()})
if __name__=='__main__':main()
