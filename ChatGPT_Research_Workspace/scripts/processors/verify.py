"""Check bibliography, local assets, numerical results, root baseline and links."""
from pathlib import Path
import json,re,hashlib,concurrent.futures,argparse
import requests,bibtexparser,pymupdf
from datetime import date,datetime,timezone
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
def run(check_links=False):
 bib=bibtexparser.loads((ROOT/'latex/references.bib').read_text(encoding='utf-8')).entries
 ids={e['ID'] for e in bib};cites=set();missing_figures=[];sections=[]
 for p in sorted((ROOT/'latex/sections').glob('*.tex')):
  t=p.read_text(encoding='utf-8');sections.append(p.name)
  for match in re.findall(r'\\cite(?:p|t)?\{([^}]+)\}',t):cites.update(match.split(','))
  for name in re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',t):
   if not (ROOT/'latex'/name).is_file():missing_figures.append(name)
 missing_metadata=[]
 for e in bib:
  for k in ['title','author']:
   if not e.get(k):missing_metadata.append(e['ID']+':'+k)
  if not(e.get('doi') or e.get('url')):missing_metadata.append(e['ID']+':doi/url')
  if e.get('ENTRYTYPE')=='article':
   for k in ['year','journal','volume','publisher']:
    if not e.get(k):missing_metadata.append(e['ID']+':'+k)
 manifest=json.loads((ROOT/'artifacts/MANIFEST.json').read_text(encoding='utf-8'))
 pdfs=[];images=[];asset_errors=[]
 for p in sorted((ROOT/'sources').rglob('*.pdf')):
  try:
   d=pymupdf.open(p);texts=[x.get_text() for x in d]
   pdfs.append({'path':p.relative_to(ROOT).as_posix(),'pages':len(d),'text_characters':sum(map(len,texts))})
  except Exception as e:asset_errors.append({'path':str(p),'error':str(e)})
 for p in sorted((ROOT/'latex/figures').iterdir()):
  if p.suffix.lower() in ['.png','.jpg','.jpeg']:
   try:
    with Image.open(p) as im:
     im.verify()
    with Image.open(p) as im:images.append({'path':p.relative_to(ROOT).as_posix(),'width_px':im.width,'height_px':im.height})
   except Exception as e:asset_errors.append({'path':str(p),'error':str(e)})
 hash_errors=[]
 for filename in ['asset_sources.json','asset_addendum.json','physics_sources.json']:
  data=json.loads((ROOT/'sources/data'/filename).read_text(encoding='utf-8'))
  for s in data:
   if s.get('local_path') and s.get('sha256'):
    p=ROOT/s['local_path']
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=s['sha256']:hash_errors.append(s['id'])
 baseline=json.loads((ROOT/'artifacts/root_baseline.json').read_text(encoding='utf-8-sig'))
 root_changes=[];expected={r['Name']:r for r in baseline}
 for p in ROOT.parent.iterdir():
  if p.is_file():
   digest=hashlib.sha256(p.read_bytes()).hexdigest().upper()
   if p.name not in expected:root_changes.append({'name':p.name,'status':'new root file'})
   elif digest!=expected[p.name]['SHA256']:root_changes.append({'name':p.name,'status':'changed since baseline'})
 for n in expected:
  if not(ROOT.parent/n).exists():root_changes.append({'name':n,'status':'absent since baseline'})
 out={'bibliography_entries':len(bib),'cited_unique_entries':len(cites),'undefined_citations':sorted(cites-ids),'missing_metadata':missing_metadata,'missing_figures':missing_figures,'pdfs':pdfs,'images':images,'asset_errors':asset_errors,'hash_errors':hash_errors,'root_changes_since_baseline':root_changes,'sections':sections}
 out['checked_at_utc']=datetime.now(timezone.utc).isoformat()
 resume_path=ROOT/'artifacts/resume_root_baseline_20260930.json'
 if resume_path.exists():
  resume=json.loads(resume_path.read_text(encoding='utf-8-sig'))
  previous={r['Name']:r['SHA256'].upper() for r in resume}
  current={p.name:hashlib.sha256(p.read_bytes()).hexdigest().upper() for p in ROOT.parent.iterdir() if p.is_file()}
  out['root_changes_since_resume']=[n for n in sorted(previous.keys()|current.keys()) if previous.get(n)!=current.get(n)]
 (ROOT/'artifacts/validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
 if check_links:
  urls={s.get('url') for s in manifest['sources'] if s.get('url','').startswith(('http://','https://'))}
  urls.update(e.get('url') for e in bib if e.get('url'))
  for p in (ROOT/'latex').rglob('*.tex'):
   if 'build' not in p.parts:urls.update(re.findall(r'\\href\{([^}]+)\}',p.read_text(encoding='utf-8')))
  def fetch(url):
   try:
    with requests.get(url,timeout=(10,25),stream=True,headers={'User-Agent':'GlassResearch-LinkAudit/1.0'}) as r:
     return {'url':url,'status':r.status_code,'resolved_url':r.url,'checked':date.today().isoformat(),'interpretation':'HTTP reachable; content and video playback not inferred' if r.status_code<400 else 'Access failed; may be blocking or stale URL'}
   except Exception as e:return {'url':url,'status':None,'error':str(e),'checked':date.today().isoformat()}
  with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:checks=list(ex.map(fetch,sorted(urls)))
  (ROOT/'artifacts/link_validation.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
  print('Links',len(checks),'HTTP <400',sum(bool(x.get('status')) and x['status']<400 for x in checks))
 print(json.dumps({k:v for k,v in out.items() if k not in ['pdfs','images','sections']},indent=2))
 assert not(cites-ids or missing_metadata or missing_figures or asset_errors or hash_errors),'Local validation failed'
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--links',action='store_true');args=p.parse_args();run(args.links)
