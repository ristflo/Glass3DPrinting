"""Integrate separate source records and bibliography; retain a DOI alias map."""
from pathlib import Path
import json,re,csv,hashlib
from datetime import date
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
ROOT=Path(__file__).resolve().parents[2]
records=[]
for name in ['academic_sources','commercial_sources','physics_sources','asset_sources','asset_addendum']:
 p=ROOT/f'sources/data/{name}.json'
 if p.exists():
  data=json.loads(p.read_text(encoding='utf-8-sig'))
  if isinstance(data,dict):data=data.get('sources',data.get('assets',data.get('records',[])))
  for x in data:
   x=dict(x,ledger_origin=name);records.append(x)
entries=[]
for p in [ROOT/'notes/academic_notes/academic_references.bib',ROOT/'notes/commercial_notes/commercial_references.bib']:
 entries.extend(bibtexparser.loads(p.read_text(encoding='utf-8')).entries)
for s in json.loads((ROOT/'sources/data/physics_sources.json').read_text(encoding='utf-8')):
 e={'ID':s['id'],'ENTRYTYPE':'article' if s.get('doi') else 'misc','title':'{'+s['title']+'}',
    'author':' and '.join(s['authors']) if s.get('doi') else '{{'+s['authors'][0]+'}}',
    'url':s['url'],'publisher':s.get('publisher',''),'note':'Accessed '+s['accessed']}
 for k in ['year','doi','volume','journal','pages']:
  if s.get(k):e[k]=str(s[k])
 if not s.get('year'):e['note']+='; publication date not stated'
 entries.append(e)
# Repairs established by the independent primary-source review.
for e in entries:
 if e['ID']=='com_liu':e.update(pages='460--466',number='2')
 if e['ID']=='acad_baudet2019':e.update(pages='2307--2317',number='5')
 if e.get('ENTRYTYPE')=='misc' and any(x in e.get('note','').lower() for x in ['undated','access year','publication date not verified']):
  e.pop('year',None)
  e['note']=e.get('note','').replace('undated website, access year used','undated website; publication year not stated')
 # Preserve case-sensitive product names and chemical symbols.
 if not e.get('title','').startswith('{'):e['title']='{'+e['title']+'}'
 if e.get('ENTRYTYPE')=='misc' and not e.get('year'):e['year']='n.d.'
aliases={'com_chhadeh':'acad_chhadeh2026'};bydoi={};out=[];seen=set()
for e in entries:
 doi=e.get('doi','').strip().lower()
 if doi and doi in bydoi:aliases[e['ID']]=bydoi[doi];continue
 if e['ID'] in seen:continue
 if doi:bydoi[doi]=e['ID']
 seen.add(e['ID']);out.append(e)
db=BibDatabase();db.entries=out
writer=BibTexWriter();writer.order_entries_by=('ID',)
(ROOT/'latex/references.bib').write_text(writer.write(db),encoding='utf-8')
(ROOT/'sources/data/citation_aliases.json').write_text(json.dumps(aliases,indent=2),encoding='utf-8')
def rewrite(m):return m.group(1)+'{'+','.join(aliases.get(k.strip(),k.strip()) for k in m.group(2).split(','))+'}'
for p in (ROOT/'latex/sections').glob('*.tex'):
 text=p.read_text(encoding='utf-8')
 text=re.sub(r'(\\cite(?:p|t)?)(?:\{)([^}]+)\}',rewrite,text)
 if p.name.startswith('02_'):
  text=text.replace('\\caption*{','\\caption{')
  text=re.sub(r'\\begin\{table\}.*?\\end\{table\}',lambda m:m.group(0).replace('\\caption{','\\caption*{'),text,flags=re.S)
 text=text.replace('a inventory','an inventory').replace('increasing viscosity halves flow if viscosity doubles','doubling viscosity halves predicted flow')
 text='\n'.join(line.replace('p{','P{').replace('X','Y') if line.lstrip().startswith(('\\begin{tabularx}','\\begin{longtable}')) else line for line in text.split('\n'))
 p.write_text(text,encoding='utf-8')
for s in records:
 if s.get('id') in {'com_evenline','com_evenlinepeople','com_maple','com_glassomer','com_glassomerhistory','com_nobula','acad_mcgill','acad_heraeus','acad_delft','acad_nagaoka'}:
  s['year']=None
  s['publication_date_note']='Undated or unverified publication date; access date retained separately.'
 s['canonical_citation']=aliases.get(s.get('id',''),s.get('id',''))
 local=s.get('local_path')
 if local:
  p=ROOT/local
  if p.is_file():s['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();s['bytes']=p.stat().st_size
manifest={'project':'Molten glass additive manufacturing','initial_research_date':'2026-09-26','integration_date':date.today().isoformat(),'method':'Scoped primary-source technical review; duplicate source records retain their independent evidence provenance. Bibliography n.d. means no verified publication date; source ledger retains null dates.','sources':records}
(ROOT/'artifacts/MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
fields=['id','canonical_citation','title','authors','year','doi_or_url','url','evidence_type','local_path','status','license','summary','accessed']
with (ROOT/'output/master_source_index.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader()
 for s in records:
  row=dict(s)
  if isinstance(row.get('authors'),list):row['authors']='; '.join(row['authors'])
  w.writerow(row)
print(f'Integrated {len(records)} source/asset records and {len(out)} unique bibliography entries; {len(aliases)} citation aliases.')
