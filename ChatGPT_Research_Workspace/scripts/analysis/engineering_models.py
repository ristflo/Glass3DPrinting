"""Illustrative flow and thermal scales, not machine performance or annealing recipes."""
from pathlib import Path
import os,json,csv
ROOT=Path(__file__).resolve().parents[2]
os.environ['MPLCONFIGDIR']=str(ROOT/'scripts/tmp/matplotlib')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
rho,g,gamma,eta=2500.,9.81,.3,1000.
r,L,h=0.005,.01,.2
dp=rho*g*h
Q=np.pi*r**4*dp/(8*eta*L)
v=Q/(np.pi*r*r)
out={'assumptions':{'density_kg_m3':rho,'gravity_m_s2':g,'surface_tension_N_m':gamma,'viscosity_Pa_s':eta,'nozzle_radius_m':r,'nozzle_length_m':L,'head_m':h},
 'pressure_Pa':dp,'flow_m3_s':Q,'mass_rate_kg_h':rho*Q*3600,'mean_nozzle_speed_m_s':v,
 'Re_diameter':rho*v*2*r/eta,'Ca':eta*v/gamma,'Bo_radius':rho*g*r*r/gamma,'Oh_radius':eta/np.sqrt(rho*gamma*r),
 'viscous_capillary_time_s':eta*r/gamma,'gravity_strain_time_s':eta/(rho*g*.1),
 'fully_restrained_room_temperature_stress_50K_MPa':73000*9.1e-6*50/(1-.22),
 'borofloat_low_temperature_diffusivity_m2_s':1.2/(2230*830),
 'borofloat_reference_properties':{'conductivity_W_mK':1.2,'conductivity_temperature_C':90,'heat_capacity_J_kgK':830,'heat_capacity_range_C':[20,100],'nominal_density_kg_m3':2230,'interpretation':'Approximate low-temperature scaling; not a high-temperature annealing model.'}}
out['thermal_diffusion_scales_s']={str(d):d*d/out['borofloat_low_temperature_diffusivity_m2_s'] for d in [.001,.005,.01,.02]}
(ROOT/'sources/data/engineering_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
plt.rcParams.update({'font.size':10,'pdf.fonttype':42})
fig,ax=plt.subplots(figsize=(7.3,4.4),layout='constrained')
visc=np.logspace(2,5,200)
for radius in [.002,.003,.005]:
 q=np.pi*radius**4*dp/(8*visc*L)
 ax.loglog(visc,rho*q*3600,label=f'Nozzle radius {radius*1000:.0f} mm')
ax.set(xlabel='Viscosity (Pa s)',ylabel='Idealized mass flow (kg/h)',title='Gravity-fed, isothermal cylindrical capillary model')
ax.legend();ax.grid(which='both',alpha=.2)
for ext in ['png','pdf']:fig.savefig(ROOT/f'latex/figures/flow_sensitivity.{ext}',dpi=300)
plt.close(fig)
fig,ax=plt.subplots(figsize=(9,4.4),layout='constrained');ax.set(xlim=(0,10),ylim=(0,5));ax.axis('off')
def box(x,y,w,h,label,color):
 ax.add_patch(Rectangle((x,y),w,h,facecolor=color,edgecolor='#26364a',lw=1.2));ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=9)
box(.4,3.1,2.2,1.2,'Reservoir / crucible\ncomposition, head, T1','#f7d7a3')
box(.9,1.95,1.2,.65,'Nozzle\nT2, Q','#eaa66e')
box(3.3,.6,3.2,2.6,'Heated build enclosure\nsubstrate and layers: T3\n\n\nMotion and shape feedback','#daecf4')
box(3.7,1.0,2.4,.25,'','#85b2cc')
box(7.3,1.35,2.3,1.4,'Separate annealing\nand controlled cooling\nthen metrology','#e2ddf1')
for a,b in [((1.5,3.1),(1.5,2.6)),((2.1,2.25),(3.3,2.25)),((6.5,2.1),(7.3,2.1))]:ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=14,color='#26364a'))
ax.text(5,4.3,'Functional architecture — original schematic, not a vendor machine',ha='center',fontsize=11)
for ext in ['png','pdf']:fig.savefig(ROOT/f'latex/figures/process_architecture.{ext}',dpi=300)
plt.close(fig)
assert Q>0 and out['Re_diameter']<1
assert abs((2*r)**4/r**4-16)<1e-10
print(json.dumps(out,indent=2))
