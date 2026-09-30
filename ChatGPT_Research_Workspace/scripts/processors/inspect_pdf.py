"""Render every report page for layout review and record machine-checkable evidence."""
from pathlib import Path
import pymupdf,json,re,hashlib
from datetime import datetime,timezone
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
pdf=ROOT/'output/glass_3d_printing_sota_monograph.pdf'
d=pymupdf.open(pdf);out=ROOT/'scripts/tmp/pdf_review';out.mkdir(parents=True,exist_ok=True)
page_records=[];thumbs=[]
for i,p in enumerate(d):
 text=p.get_text();page_records.append({'page':i+1,'characters':len(text),'images':len(p.get_images()),'width_pt':p.rect.width,'height_pt':p.rect.height})
 pix=p.get_pixmap(matrix=pymupdf.Matrix(1.25,1.25));pix.save(out/f'page_{i+1:02}.png')
 im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((298,422))
 tile=Image.new('RGB',(318,455),'#d6dce1');tile.paste(im,((318-im.width)//2,23));ImageDraw.Draw(tile).text((10,5),f'Page {i+1}',fill='black');thumbs.append(tile)
for start in range(0,len(thumbs),12):
 sheet=Image.new('RGB',(318*4,455*3),'#c5ccd3')
 for j,im in enumerate(thumbs[start:start+12]):sheet.paste(im,((j%4)*318,(j//4)*455))
 sheet.save(out/f'contact_{start//12+1}.png')
log=(ROOT/'latex/build/main.log').read_text(encoding='utf-8',errors='replace')
warnings=[line for line in log.splitlines() if any(s in line for s in ['Warning:','Overfull','Underfull','Missing character'])]
result={'page_count':len(d),'page_records':page_records,'bookmarks':d.get_toc(),'warnings':warnings,'undefined_reference_warning':bool(re.search(r'(undefined references|Citation .*undefined|Reference .*undefined)',log))}
result['checked_at_utc']=datetime.now(timezone.utc).isoformat()
result['pdf_sha256']=hashlib.sha256(pdf.read_bytes()).hexdigest()
result['bibtex_warnings']=[line for line in (ROOT/'latex/build/main.blg').read_text(encoding='utf-8',errors='replace').splitlines() if line.startswith('Warning')]
result['link_annotation_count']=sum(len(p.get_links()) for p in d)
(ROOT/'artifacts/pdf_inspection.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
(ROOT/'scripts/tmp/report_text.txt').write_text('\n\n'.join(p.get_text() for p in d),encoding='utf-8')
print('Pages',len(d),'bookmarks',len(d.get_toc()),'warnings',len(warnings));print('\n'.join(warnings));print('Render contact sheets:',out)
assert not result['undefined_reference_warning']
assert not any('Overfull' in w or 'Missing character' in w for w in warnings)
