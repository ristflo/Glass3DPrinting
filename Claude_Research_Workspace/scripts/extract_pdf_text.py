import pathlib, sys
from pypdf import PdfReader
ROOT = pathlib.Path(__file__).resolve().parent.parent
out = ROOT/"sources"/"data"/"text"
for pdf in sorted((ROOT/"sources"/"papers").glob("*.pdf")) + sorted((ROOT/"sources"/"patents").glob("*.pdf")):
    dest = out/(pdf.stem + ".txt")
    if dest.exists(): continue
    try:
        r = PdfReader(str(pdf)); txt = "\n".join((p.extract_text() or "") for p in r.pages[:60])
        dest.write_text(txt, encoding="utf-8"); print(f"{pdf.name}: {len(r.pages)} pages, {len(txt)} chars")
    except Exception as e: print(f"{pdf.name}: ERROR {e}")
