"""Build independently checked academic source fragment; writes only inside workspace."""
from pathlib import Path
import json, requests, concurrent.futures, re, time
ROOT = Path(__file__).resolve().parents[2]
ARTICLES = [
('acad_klein2015','10.1089/3dp.2015.0021','Reservoir-fed molten glass extrusion; foundational G3DP demonstration.'),
('acad_inamura2018','10.1089/3dp.2018.0157','G3DP2 integrates three thermal zones and four-axis motion; architectural assembly demonstration.'),
('acad_liu2022','10.3389/fmats.2022.978861','KTH/Nobula symmetric laser heating of fused silica filament; repeatable multilayer wall deposition.'),
('acad_witzendorff2018','10.1016/j.procir.2018.08.109','Laser Zentrum Hannover quartz filament deposition with CO2 laser and moving substrate.'),
('acad_baudet2019','10.1364/OME.9.002307','Laval direct extrusion of arsenic sulfide chalcogenide glass; not a silicate process.'),
('acad_nguyen2017','10.1002/adma.201701181','LLNL direct ink writing followed by thermal densification; not molten deposition.'),
('acad_destino2018','10.1002/admt.201700323','Sol-gel feedstocks, direct ink writing, thermal processing, and optical characterization.'),
('acad_chen2025','10.3390/mi16010029','Closed-loop laser power control for quartz glass deposition; issue year 2025, online 2024-12-28.'),
('acad_chhadeh2026','10.1038/s44334-026-00072-1','TU Darmstadt/Deakin four-point bend experiments link toolpath and heat retention to mechanical performance.'),
('acad_stern2024','10.47982/cgc.9.583','Evenline/MIT tests recycled container and float glass printability; not TU Delft apparatus.'),
]
WEB = [
('acad_mitproject','Glass I', ['MIT Media Lab'],2015,'https://www.media.mit.edu/projects/g3p/overview/','MIT Media Lab','Historical two-chamber G3DP architecture and nozzle description; project page differs in material terminology from author manuscript.'),
('acad_schott2023','TIE-27: Stress in optical glass',['SCHOTT'],2023,'https://media.schott.com/api/public/content/d33171e170af4b94a8e49b11d758258e?v=610aa3b1','SCHOTT','August 2023 technical note: annealing, stress optics, geometry dependence and birefringence.'),
('acad_heraeus','Glass Manufacturing Equipment',['Heraeus Precious Metals'],2026,'https://www.heraeus-precious-metals.com/en/products-solutions/category/precious-metal-components/glass-manufacturing-equipment/','Heraeus Precious Metals','Undated manufacturer technical guidance accessed 2026; platinum alloys and composition-dependent equipment selection, not AM printer validation.'),
('acad_delft','F. Oikonomopoulou: Research outputs',['TU Delft'],2026,'https://research.tudelft.nl/en/persons/f-oikonomopoulou/','TU Delft','Institutional directory verifies structural/cast glass and collaboration with Telesilla Bristogianni; no direct printer identification.'),
('acad_ikts','Additive glass shaping improves selectivity of photomultipliers',['Fraunhofer IKTS'],2022,'https://www.ikts.fraunhofer.de/en/blog/additive-glass-shaping-improves-selectivity-of-photomultipliers.html','Fraunhofer IKTS','Glass-filled filament printing and subsequent sintering for photomultiplier-related parts; indirect route.'),
('acad_isc','3D-printed optics for individualized mass production',['Fraunhofer ISC'],2019,'https://www.isc.fraunhofer.de/en/press-and-media/press-releases/3d-printed-optics-for-individualized-mass-production.html','Fraunhofer ISC','ISC/IOF ORMOCER hybrid polymer optics, not equivalent to fully inorganic molten glass.'),
('acad_ipt','3DHeat: Hybrid Additive Manufacturing of Molding Tools for Glass Molding',['Fraunhofer IPT'],2025,'https://www.ipt.fraunhofer.de/en/projects/3dheat.html','Fraunhofer IPT','2025-2027 project prints metal tools for glass molding; not direct printing of glass.'),
('acad_kthrise','Laser based 3D printing and processing: SSF financed research',['KTH Royal Institute of Technology'],2019,'https://www.aphys.kth.se/lamp/research/laserphysics/research/laser-based-3d-print','KTH','Institutional evidence of KTH/NTNU/RISE Acreo collaboration; contact Michel Fokine on historical page.'),
('acad_lavalproject','Additive manufacturing of glasses for the fabrication of optical components: Summer 2025 internship',['Universite Laval LRIO'],2025,'https://lrio.copl.ulaval.ca/images/E25-Stage-Fabrication_verre.pdf','Universite Laval','Nanocomposite vat photopolymerization followed by thermal treatment and optical finishing; separate from chalcogenide extrusion.'),
('acad_mcgill','Engineering human-scale perfusable tissues for diabetes cell therapy using 3D printing',['McGill University'],2026,'https://escholarship.mcgill.ca/concern/theses/sf268c17j','McGill University','Repository item retrieved in 2026 concerns carbohydrate/sugar glass; excluded from inorganic molten-glass evidence. Publication year not verified.'),
('acad_nagaoka','Research publications: Takayuki Komatsu',['Nagaoka University of Technology'],2026,'https://etigo.nagaokaut.ac.jp/koudoka/prmt/komatsu.html','Nagaoka University of Technology','Historical institutional glass/crystal hybrid research page; molten deposition apparatus and current leadership not verified.'),
]

def fetch(item):
    key,doi,summary=item
    cache=ROOT/'sources/data'/f'{key}_crossref.json'
    if cache.exists():
        m=json.loads(cache.read_text(encoding='utf-8'))
    else:
        for attempt in range(4):
            r=requests.get('https://api.crossref.org/works/'+doi,timeout=45)
            if r.status_code!=429: break
            time.sleep(2+attempt*2)
        r.raise_for_status(); m=r.json()['message']
    (ROOT/'sources/data'/f'{key}_crossref.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
    authors=[(a.get('given','')+' '+a.get('family','')).strip() for a in m.get('author',[])]
    year=m.get('published',m.get('issued'))['date-parts'][0][0]
    if key=='acad_chen2025': year=2025
    record=dict(id=key,title=m['title'][0],authors=authors,year=year,doi_or_url=doi,doi=doi,url='https://doi.org/'+doi,publisher=m.get('publisher',''),volume=m.get('volume',''),summary=summary,evidence_type='peer-reviewed primary research',accessed='2026-09-26')
    fields=dict(title=m['title'][0],author=' and '.join((a.get('family','')+', '+a.get('given','')).strip(', ') for a in m.get('author',[])),year=str(year),journal=m.get('container-title',[''])[0],publisher=m.get('publisher',''),doi=doi,url='https://doi.org/'+doi)
    for f in ('volume','number','page','article-number'):
        if f in m: fields[{'page':'pages','article-number':'eid'}.get(f,f)]=str(m[f]).replace('–','--')
    return record,'@article{'+key+',\n'+''.join('  '+k+' = {'+tex(v)+'},\n' for k,v in fields.items())+'}\n'

def tex(s):
    return s.replace('&',r'\&').replace('‐','-').replace('–','--').replace('−','-').replace('’',"'")

if __name__=='__main__':
    results=[fetch(item) for item in ARTICLES]
    records=[r[0] for r in results]; bib=[r[1] for r in results]
    for key,title,authors,year,url,pub,summary in WEB:
        records.append(dict(id=key,title=title,authors=authors,year=year,doi_or_url=url,url=url,publisher=pub,summary=summary,evidence_type='institutional or manufacturer primary webpage',accessed='2026-09-26'))
        # Retrieval-only dates are not represented as publication years.
        dated=key not in ('acad_heraeus','acad_delft','acad_mcgill','acad_nagaoka')
        bib.append('@misc{'+key+',\n  title={'+tex(title)+'},\n  author={{'+tex(authors[0])+'}},\n'+('  year={'+str(year)+'},\n' if dated else '')+'  howpublished={'+tex(pub)+'},\n  url={'+url+'},\n  note={Accessed 2026-09-26'+('' if dated else '; publication date not verified')+'}\n}\n')
    (ROOT/'sources/data/academic_sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'notes/academic_notes/academic_references.bib').write_text('\n'.join(bib),encoding='utf-8')
    print(f'Wrote {len(records)} source records and bibliography entries')
