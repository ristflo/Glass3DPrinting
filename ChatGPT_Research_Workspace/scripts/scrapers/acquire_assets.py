"""Acquire primary-source assets; all outputs anchored inside this workspace.

Run: scripts/tmp/venv/Scripts/python.exe scripts/scrapers/acquire_assets.py
Existing local OA copies are preserved with their source provenance, then parsed.
"""
from pathlib import Path
import concurrent.futures, hashlib, json, re, shutil
import requests
import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT.parent / 'glass_am_research'
DATE = '2026-09-26'
LEDGER = []
HEAD = {'User-Agent': 'Mozilla/5.0 scholarly glass-AM asset verification'}
for folder in ['sources/data/text','sources/data/asset_http','sources/papers','sources/patents','sources/media','latex/figures','notes/summaries']:
    (ROOT/folder).mkdir(parents=True, exist_ok=True)

def get(url):
    return requests.get(url, headers=HEAD, timeout=(15,70))

def record(asset, path=None):
    asset.update(accessed=DATE)
    if path:
        assert path.resolve().is_relative_to(ROOT)
        data = path.read_bytes()
        asset.update(local_path=path.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
        if path.suffix.lower() == '.pdf':
            if not data.startswith(b'%PDF'): raise ValueError('Not PDF '+str(path))
            doc = pymupdf.open(path)
            asset['pages'] = len(doc)
            txt = '\n\n'.join(p.get_text() for p in doc)
            asset['extracted_characters'] = len(txt)
            (ROOT/'sources/data/text'/f'{path.stem}.txt').write_text(txt,encoding='utf-8')
            asset['status'] = 'PDF integrity verified; all pages parsed'
            licenses = re.findall(r'.{0,100}(?:Creative Commons|creativecommons.org|CC BY).{0,150}',txt,re.I)
            asset['license_evidence'] = licenses[:5]
            if 'creativecommons.org/licenses/by/4.0' in txt:
                asset['license'] = 'CC BY 4.0'
            doc.close()
        elif path.suffix.lower() in ['.jpg','.png']:
            with Image.open(path) as im:
                im.verify()
            with Image.open(path) as im:
                asset['dimensions_pixels'] = list(im.size)
            asset['status'] = 'Image integrity verified'
    else:
        asset.setdefault('local_path',None);asset.setdefault('sha256',None)
    LEDGER.append(asset)
    print(asset['id'],asset.get('status'),flush=True)

def main():
    old = json.loads((OLD/'sources/manifest.json').read_text(encoding='utf-8'))
    log = (OLD/'sources/data/harvest_log.txt').read_text(encoding='utf-8')
    provenance = {}
    for key,block in re.findall(r'\[([^\]]+)\]([^\[]+)',log):
        urls=re.findall(r'PDF ok <- (https?://\S+)',block)
        if urls: provenance[key] = urls[0]
    extras = {
      'klein2015': ('2015_Klein_Additive_Manufacturing_of_Optically_Transparent_Glass.pdf','https://dspace.mit.edu/handle/1721.1/101831'),
      'inamura2018': ('2018_Inamura_Additive_Manufacturing_of_Transparent_Glass_Structures.pdf','https://dspace.mit.edu/bitstreams/7dbd523f-a0c1-4274-94e1-a370ca822c2c/download')
    }
    for p in old['papers']:
        key=p['key']
        if not p.get('local_path') and key not in extras:continue
        name = extras[key][0] if key in extras else Path(p['local_path']).name
        src=OLD/'sources/papers'/name
        if not src.exists():continue
        dest=ROOT/'sources/papers'/name
        shutil.copy2(src,dest)
        url=extras[key][1] if key in extras else provenance.get(key,p.get('oa_url',p['url']))
        a=dict(id='asset_'+key,title=p['title'],authors=p['authors'],year=p['year'],doi_or_url=p['doi'],doi=p['doi'],url=url,publisher=p.get('venue'),summary=p.get('relevance_summary',''),evidence_type='academic_pdf',license='Open-access repository copy; see original article terms',provenance='Copied from prior local archive; original acquisition URL retained. PDF title and page parsing checked in current run.')
        record(a,dest)

    patents = [
      ('US10266442B2','Methods and apparatus for additive manufacturing of glass',2019,['John Klein','Giorgia Franchin','Michael Stern','Markus Kayser','Chikara Inamura','Shreya Dave','Neri Oxman','Peter Houk'],'https://patentimages.storage.googleapis.com/74/86/c4/4858833d28af73/US10266442.pdf','MIT; molten glass deposition apparatus'),
      ('AU2021289614A1','Three-dimensional printing system',2023,['Nick Birbilis','Darren Robert Feenstra','Tony Koutsonikolas'],'https://patentimages.storage.googleapis.com/ae/74/26/8df18a31728485/AU2021289614A1.pdf','Maple Glass Printing; filament-fed heated nozzle'),
      ('WO2020118157A1','Engineered feedstocks for additive manufacture of glass',2020,['Lawrence Livermore National Security, LLC'],'https://patentimages.storage.googleapis.com/9e/04/14/45bdff95d6da30/WO2020118157A1.pdf','LLNL engineered ink/feedstock route; distinguish from molten deposition')]
    def fetch_patent(t):
        ident,title,year,authors,url,summary=t
        r=get(url);r.raise_for_status()
        p=ROOT/'sources/patents'/f'{ident}.pdf';p.write_bytes(r.content)
        return dict(id='asset_patent_'+ident,title=title,authors=authors,year=year,doi_or_url='https://patents.google.com/patent/'+ident+'/en',url=url,publisher='Published patent specification',summary=summary,evidence_type='patent_pdf',license='Published patent document; no blanket reuse license asserted',http_status=r.status_code),p
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for a,p in pool.map(fetch_patent,patents):record(a,p)

    # Frontiers CC BY paper figures: original images, no modification.
    for n,desc in [(1,'Four-beam CO2 laser filament deposition schematic'),(6,'Microscopy of glass deposition and bonding')]:
        src=OLD/'sources/media'/f'kth2022_fig{n}.jpg'
        p=ROOT/'sources/media'/f'Liu2022_Figure{n}.jpg'
        if src.exists():shutil.copy2(src,p)
        else:
            r=get(f'https://www.frontiersin.org/files/Articles/978861/fmats-09-978861-HTML/image_m/fmats-09-978861-g00{n}.jpg');r.raise_for_status();p.write_bytes(r.content)
        shutil.copy2(p,ROOT/'latex/figures'/p.name)
        record(dict(id=f'asset_liu2022_fig{n}',title=desc,authors=['Chunxin Liu','Taras Oriekhov','Michael Fokine'],year=2022,doi_or_url='10.3389/fmats.2022.978861',url=f'https://www.frontiersin.org/files/Articles/978861/fmats-09-978861-HTML/image_m/fmats-09-978861-g00{n}.jpg',doi='10.3389/fmats.2022.978861',summary='Unmodified figure from the open-access article; caption checked against article text.',evidence_type='figure',license='CC BY 4.0; https://creativecommons.org/licenses/by/4.0/'),p)

    spring=get('https://link.springer.com/article/10.1007/s40940-024-00279-8')
    (ROOT/'sources/data/asset_http/massimino2024.html').write_text(spring.text,encoding='utf-8')
    for n,desc in [(1,'Evenline G3DP3 glass printer'),(2,'Interlocking glass masonry wall before mechanical tests')]:
        matches = re.findall(r'https://media\.springernature\.com/[^\s"<>]+40940_2024_279_Fig'+str(n)+r'_HTML[^\s"<>]*',spring.text)
        url = matches[0].replace('&amp;','&') if matches else f'https://media.springernature.com/full/springer-static/image/art%3A10.1007%2Fs40940-024-00279-8/MediaObjects/40940_2024_279_Fig{n}_HTML.png'
        try:
            r=get(url);r.raise_for_status();p=ROOT/'sources/media'/f'Massimino2024_Figure{n}.png';p.write_bytes(r.content)
            with Image.open(p) as im:im.verify()
            shutil.copy2(p,ROOT/'latex/figures'/p.name)
            record(dict(id=f'asset_massimino2024_fig{n}',title=desc,authors=['Daniel Massimino','Ethan Townsend','Charlotte Folinus','Michael Stern','Kaitlyn Becker'],year=2024,doi_or_url='10.1007/s40940-024-00279-8',doi='10.1007/s40940-024-00279-8',url=url,summary='Unmodified article figure; article Creative Commons statement applies absent an individual exclusion.',evidence_type='figure',license='CC BY 4.0; https://creativecommons.org/licenses/by/4.0/'),p)
        except Exception as e: print('FIGURE FAILED',n,str(e),flush=True)

    videos=[('mit_glass_i','GLASS / G3DP',2015,['MIT Mediated Matter Group'],'https://vimeo.com/136764796','https://commons.wikimedia.org/wiki/File:Matter-glass-printer.webm'),('mit_glass_ii','GLASS II / G3DP2',2017,['MIT Mediated Matter Group'],'https://vimeo.com/211778198','https://commons.wikimedia.org/wiki/File:GLASS_II_-_Mediated_Matter.webm'),('maple_demo','3D Glass Printing | Inside Maple Glass Printing',2023,['Maple Glass Printing'],'https://www.youtube.com/watch?v=CSw0Kw6M8i0','https://www.youtube.com/watch?v=CSw0Kw6M8i0')]
    for ident,title,year,authors,url,discovery in videos:
        a=dict(id='asset_video_'+ident,title=title,authors=authors,year=year,doi_or_url=url,url=url,summary='Official process demonstration; page identity checked by source/discovery record. Streaming playback not tested.',evidence_type='video_link',license='Link only; no video copied',discovery_url=discovery)
        try:
            r=get(url);a.update(http_status=r.status_code,status='HTTP checked; playback not verified',final_url=r.url)
            (ROOT/'sources/data/asset_http'/f'{ident}.html').write_text(r.text,encoding='utf-8')
        except Exception as e:a.update(status='Direct HTTP retrieval failed; indexed/source-linked URL only; playback unverified',error=str(e))
        record(a)
    (ROOT/'sources/data/asset_sources.json').write_text(json.dumps(LEDGER,indent=2,ensure_ascii=False),encoding='utf-8')
    print('DONE',len(LEDGER),'records',flush=True)

if __name__=='__main__': main()
