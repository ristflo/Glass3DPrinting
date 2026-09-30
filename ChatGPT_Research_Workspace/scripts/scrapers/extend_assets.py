"""Acquire recent primary evidence and photoelasticity media; extend asset ledger."""
import json,re,shutil
from bs4 import BeautifulSoup
import acquire_assets as a
from PIL import Image
a.LEDGER=json.loads((a.ROOT/'sources/data/asset_sources.json').read_text(encoding='utf-8'))
papers=[('chhadeh2026','https://www.nature.com/articles/s44334-026-00072-1','https://www.nature.com/articles/s44334-026-00072-1.pdf','2026_Chhadeh_Toolpath_Design_Mechanical_Strength.pdf','10.1038/s44334-026-00072-1'),('efferz2024','https://link.springer.com/article/10.1007/s40940-024-00270-3','https://link.springer.com/content/pdf/10.1007/s40940-024-00270-3.pdf','2024_Efferz_Photoelastic_Edge_Stress.pdf','10.1007/s40940-024-00270-3')]
for key,url,pdfurl,name,doi in papers:
    try:
        r=a.get(url);r.raise_for_status()
        (a.ROOT/'sources/data/asset_http'/f'{key}.html').write_text(r.text,encoding='utf-8')
        soup=BeautifulSoup(r.text,'html.parser')
        def meta(k):return [x.get('content','') for x in soup.find_all('meta',attrs={'name':k})]
        title=meta('citation_title')[0];authors=meta('citation_author');date=meta('citation_publication_date') or meta('citation_date')
        p=a.ROOT/'sources/papers'/name
        rr=a.get(pdfurl);rr.raise_for_status();p.write_bytes(rr.content)
        a.record(dict(id='asset_'+key,title=title,authors=authors,year=int(date[0][:4]),doi_or_url=doi,doi=doi,url=pdfurl,publisher=(meta('citation_journal_title') or [''])[0],summary='Primary experimental research; see extracted PDF text. Photoelastic paper studies tempered flat glass, not printed glass.' if key=='efferz2024' else 'Primary study of toolpath design and mechanical strength in glass additive manufacturing.',evidence_type='academic_pdf',license='Open access; see article terms',http_status=rr.status_code),p)
        if key=='efferz2024':
            for n in [3]:
                fig=soup.find(id='Fig'+str(n))
                print('PHOTOELASTIC CAPTION',fig.get_text(' ',strip=True) if fig else 'not found',flush=True)
                images=re.findall(r'https://media\.springernature\.com/[^\s"<>]+40940_2024_270_Fig'+str(n)+r'_HTML[^\s"<>]*',r.text)
                imageurl=images[0].replace('&amp;','&')
                ir=a.get(imageurl);ir.raise_for_status();ip=a.ROOT/'sources/media'/f'Efferz2024_Figure{n}.png';ip.write_bytes(ir.content)
                with Image.open(ip) as im:im.verify()
                shutil.copy2(ip,a.ROOT/'latex/figures'/ip.name)
                a.record(dict(id='asset_efferz2024_fig3',title='Photoelastic measurement apparatus for architectural glass',authors=authors,year=2024,doi_or_url=doi,doi=doi,url=imageurl,summary='Experimental measurement schematic for tempered flat glass; not evidence of an AM-specific stress measurement.',evidence_type='figure',license='CC BY 4.0; https://creativecommons.org/licenses/by/4.0/'),ip)
    except Exception as e:print('ACQUISITION FAILURE',key,str(e),flush=True)

for entry in a.LEDGER:
    if entry['id']=='asset_patent_WO2020118157A1':
        entry['authors']=['Rebecca Dylla-Spears','Tayyab I. Suratwala','Nikola Dudukovic','Tyler Fears','Fang Qian','Koroush Sasan','Joel Destino']
    if entry['id'] in ['asset_kth2022bonding','asset_mit2024masonry']:
        entry['license']='CC BY 4.0; https://creativecommons.org/licenses/by/4.0/'
    if entry['id']=='asset_solgel2025':entry['evidence_type']='review_pdf'
    if entry['id']=='asset_inamura2018':entry['license']='MIT repository copy; PDF contains personal-use notice; no blanket redistribution permission asserted'
    if entry['id']=='asset_toombs2022':entry['version']='arXiv preprint with supplementary information; journal metadata refers to Science publication'
(a.ROOT/'sources/data/asset_sources.json').write_text(json.dumps(a.LEDGER,indent=2,ensure_ascii=False),encoding='utf-8')
