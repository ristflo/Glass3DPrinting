"""Rebuild the 2026-09-29 asset audit without changing the original ledger."""
from pathlib import Path
import hashlib, json, shutil
import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DATE = '2026-09-29'
original = json.loads((ROOT/'sources/data/asset_sources.json').read_text(encoding='utf-8'))
if isinstance(original, dict):
    original = original.get('sources', original.get('assets', []))
records = []

captions = {
    'asset_liu2022_fig1': 'Four-beam CO2-laser heating of a glass filament during deposition (Liu, Oriekhov and Fokine, 2022, Fig. 1). Reproduced without modification, CC BY 4.0.',
    'asset_liu2022_fig6': 'Top views (A) and cross-sections (B) of deposited glass lines at 10–100 mm/min, with laser power varied as in the source article (Liu, Oriekhov and Fokine, 2022, Fig. 6). Reproduced without modification, CC BY 4.0.',
    'asset_massimino2024_fig1': 'G3DP3 apparatus: the build chamber lies behind the glazed doors, below the furnace and crucible (Massimino et al., 2024, Fig. 1). Reproduced without modification, CC BY 4.0.',
    'asset_massimino2024_fig2': 'Manufactured masonry units arranged as a wall before mechanical testing (Massimino et al., 2024, Fig. 2). Reproduced without modification, CC BY 4.0.'
}

def integrity(record):
    p = ROOT/record['local_path']
    data = p.read_bytes()
    record.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    if p.suffix.lower() == '.pdf':
        assert data.startswith(b'%PDF')
        doc = pymupdf.open(p)
        text = '\n'.join(page.get_text() for page in doc)
        record.update(pages=len(doc), extracted_characters=len(text))
    else:
        with Image.open(p) as im:
            record['dimensions_pixels'] = list(im.size)
            im.verify()

for entry in original:
    if entry['id'] in captions:
        r = dict(entry)
        r.update(id=entry['id']+'_audit_20260929', original_id=entry['id'], accessed=DATE,
                 summary=captions[entry['id']], recommended_caption=captions[entry['id']],
                 status='Image decoded and visually inspected; caption matched to primary PDF; article license checked; no individual figure exclusion found')
        integrity(r)
        records.append(r)

r = dict(id='asset_chhadeh2026', title='The effect of toolpath design on the mechanical strength of additively manufactured glass components',
         authors=['Philipp Amir Chhadeh','Emanuel Nowak','Dylan Vlahopoulos','Matthias Seel','Nick Birbilis'],year=2026,
         doi_or_url='10.1038/s44334-026-00072-1',url='https://www.nature.com/articles/s44334-026-00072-1.pdf',
         local_path='sources/papers/2026_Chhadeh_Toolpath_Design_Mechanical_Strength.pdf',
         license='CC BY-NC-ND 4.0; https://creativecommons.org/licenses/by-nc-nd/4.0/',
         summary='Primary four-point bending study of filament-extruded soda-lime glass. Toolpath and layer orientation affected mechanical performance; thermal-history explanation is a proposed mechanism. The paper is not a qualification standard.',
         status='Downloaded from publisher; PDF signature and all 11 pages parsed; license checked on final page',evidence_type='academic_pdf',accessed=DATE)
integrity(r); records.append(r)

figurl='https://media.springernature.com/full/springer-static/image/art%3A10.1007%2Fs40940-024-00270-3/MediaObjects/40940_2024_270_Fig2_HTML.png'
caption='Intensity (a) and isochromatic (b) images near the chamfered edge of 10 mm fully tempered glass; marked points lie 1.0 and 1.6 mm from the edge. Efferz, Schuler and Siebert (2024), Fig. 2, CC BY 4.0, reproduced without modification. This is conventional tempered glass, not an additively manufactured specimen.'
r=dict(id='asset_efferz2024_fig2',title='Photoelastic images near a chamfered tempered-glass edge',authors=['Lena Efferz','Christian Schuler','Geralt Siebert'],year=2024,
       doi_or_url='10.1007/s40940-024-00270-3',url=figurl,local_path='sources/media/Efferz2024_Figure2.png',
       license='CC BY 4.0; https://creativecommons.org/licenses/by/4.0/',summary=caption,recommended_caption=caption,
       status='Downloaded; image decoded and visually checked against publisher Figure 2 caption; article reuse terms checked, no figure-specific exclusion found',
       evidence_type='figure',accessed=DATE,source_page='https://link.springer.com/article/10.1007/s40940-024-00270-3')
integrity(r);records.append(r)
shutil.copy2(ROOT/r['local_path'], ROOT/'latex/figures/Efferz2024_Figure2.png')

checks=json.loads((ROOT/'sources/data/asset_http/status_20260929.json').read_text(encoding='utf-8'))
mapping={'mit1':'asset_video_mit_glass_i','mit2':'asset_video_mit_glass_ii','maple':'asset_video_maple_demo'}
for check in checks:
    if check['id'] not in mapping: continue
    source=next(x for x in original if x['id']==mapping[check['id']])
    r=dict(source)
    r.update(id=source['id']+'_audit_20260929', original_id=source['id'], accessed=DATE,http_status=check.get('http_status'),
             summary='Link only. '+('YouTube page title matches expected video.' if check['id']=='maple' else 'HTTP 200 returned a script-driven page without a title; identity relies on the earlier discovery record.'),
             status='HTTP checked; streaming playback and captions not verified',local_path=None)
    records.append(r)
records.append(dict(id='asset_video_memphis_polariscope',title='Polariscope',authors=['University of Memphis, Department of Physics and Materials Science'],year=None,
    doi_or_url='https://www.youtube.com/watch?v=IefRrdTmlbA',url='https://www.youtube.com/watch?v=IefRrdTmlbA',local_path=None,
    license='Link only; no redistribution license asserted; no video copied',
    summary='Direct video embedded by the university in its stress-birefringence demonstration page. Educational demonstration; it does not establish stress magnitudes in printed glass.',
    status='University embed identity verified and YouTube page returned HTTP 200 with title Polariscope; playback and specimen material not independently verified',
    evidence_type='video_link',accessed=DATE,discovery_url='https://www.memphis.edu/physics/demonstrations/polariscope.php'))
records.append(dict(id='asset_lazos_photoelastic_attempt',title='Photoelasticity and color on a stressed glass plate',authors=['Takis lazos'],year=2013,
    doi_or_url='https://commons.wikimedia.org/wiki/File:Photoelasticity_and_color_on_a_stressed_glass_plate.jpg',
    url='https://upload.wikimedia.org/wikipedia/commons/1/17/Photoelasticity_and_color_on_a_stressed_glass_plate.jpg',local_path=None,
    license='CC BY-SA 4.0 per Commons original-author file page; https://creativecommons.org/licenses/by-sa/4.0/',
    summary='Possible illustration of clamped glass viewed between crossed polarizers; not used in report because download failed. Efferz Figure 2 supplies the photoelastic image instead.',
    status='File-page attribution and license verified with web reader; binary acquisition returned HTTP 403',evidence_type='failed_acquisition',accessed=DATE))
(ROOT/'sources/data/asset_addendum.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Wrote {len(records)} addendum records; original ledger untouched.')
