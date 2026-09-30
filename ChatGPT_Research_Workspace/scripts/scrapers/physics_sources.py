"""Retrieve source metadata and manufacturer data; retain raw responses."""
from pathlib import Path
import requests, json, hashlib, concurrent.futures, time
from urllib.parse import quote
import pymupdf
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'sources/data'
SPECS=[
 ('phys_ar','AR-GLAS: Tubing and Rod of Special Glass','SCHOTT','https://media.schott.com/api/public/content/79a671737b4a4833aa91c99f68c4b5a3?v=eb1ee445'),
 ('phys_boro','BOROFLOAT 33: Thermal Properties','SCHOTT','https://media.schott.com/api/public/content/4fd51376b9d54a68b47be78fadfdd32d?download=true&v=1fc0ea9c'),
 ('phys_silica','HPFS 7979, 7980, 8655 Fused Silica: Optical Materials Product Information','Corning','https://www.corning.com/media/worldwide/csm/documents/HPFS_Product_Brochure_All_Grades_2025_11.pdf')]
DOIS={
 'phys_rayleigh':'10.1112/plms/s1-10.1.4','phys_tomotika':'10.1098/rspa.1935.0104',
 'phys_klein':'10.1089/3dp.2015.0021','phys_inamura':'10.1089/3dp.2018.0157',
 'phys_kotz':'10.1038/nature22061','phys_datsiou':'10.1111/jace.16440',
 'phys_toombs':'10.1126/science.abm6459','phys_liu':'10.3389/fmats.2022.978861',
 'phys_masonry':'10.1007/s40940-024-00279-8'}
def get(url):
 for attempt in range(4):
  r=requests.get(url,timeout=50,headers={'User-Agent':'GlassAM-research/1.0'})
  if r.status_code != 429: break
  time.sleep(3*(attempt+1))
 r.raise_for_status();return r
def spec(x):
 key,title,author,url=x;r=get(url)
 if not r.content.startswith(b'%PDF'):raise ValueError(url+' is not a PDF')
 p=ROOT/'sources/papers'/(key+'.pdf');p.write_bytes(r.content)
 pdf=pymupdf.open(p)
 (DATA/(key+'.txt')).write_text('\n'.join(f'PAGE {i+1}\n'+v.get_text() for i,v in enumerate(pdf)),encoding='utf-8')
 return dict(id=key,title=title,authors=[author],year=None,doi_or_url=url,url=url,publisher=author,summary='Manufacturer reference points; nominal values, not measured AM performance.',evidence_type='manufacturer datasheet',local_path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(r.content).hexdigest(),accessed='2026-09-26',status='downloaded and parsed')
def doi(x):
 key,d=x;r=get('https://api.crossref.org/works/'+quote(d,safe=''));m=r.json()['message']
 (DATA/(key+'_crossref.json')).write_text(r.text,encoding='utf-8')
 return dict(id=key,title=m['title'][0],authors=[(a.get('given','')+' '+a.get('family','')).strip() for a in m.get('author',[])],year=m.get('published',m['issued'])['date-parts'][0][0],doi=d,doi_or_url='https://doi.org/'+d,url='https://doi.org/'+d,publisher=m.get('publisher',''),volume=m.get('volume',''),journal=(m.get('container-title') or [''])[0],pages=m.get('page',''),summary='Primary publication; Crossref metadata checked. Claim-specific reading documented in the monograph and research notes.',evidence_type='primary research',accessed='2026-09-26',status='metadata verified')
if __name__=='__main__':
 results=json.loads((DATA/'physics_sources.json').read_text(encoding='utf-8')) if (DATA/'physics_sources.json').exists() else []
 done={s['id'] for s in results}
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
  futures=[ex.submit(spec,x) for x in SPECS if x[0] not in done]+[ex.submit(doi,x) for x in DOIS.items() if x[0] not in done]
  for f in concurrent.futures.as_completed(futures):
   try:s=f.result();results.append(s);print(s['id'],s['title'],flush=True)
   except Exception as e:print('FAILED',str(e),flush=True)
 (DATA/'physics_sources.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
