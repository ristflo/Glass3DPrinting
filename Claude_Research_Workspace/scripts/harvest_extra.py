#!/usr/bin/env python
"""harvest_extra.py - supplementary seed batch; appends to sources/manifest.json (same logic as harvest_literature.py)."""
import json, re, time, difflib, pathlib, requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAPERS = ROOT / "sources" / "papers"; DATA = ROOT / "sources" / "data"
S = requests.Session(); S.headers["User-Agent"] = "glass-am-sota-harvester/1.0 (academic literature review; python-requests)"
LOG = open(DATA / "harvest_log.txt", "a", encoding="utf-8")
def log(m): print(m); LOG.write(m + "\n"); LOG.flush()

SEEDS = [
    ("luo2016spie", "10.1117/12.2218137", "Filament-fed CO2-laser AM of fused quartz for optics (SPIE 2016)"),
    ("capps2021interface", "T:Direct laser heating of the filament/substrate interface in digital glass forming", "Side-injected laser heating of filament/substrate interface to raise deposition rate (Kinzel group)"),
    ("dgf2023tubes", "T:Printing Hollow Tubes Using Digital Glass Forming", "Hollow tubes by digital glass forming (JMSE 2023)"),
    ("hostetler2019optics", "T:Glass Printing for Optics and Photonics Applications using a Filament-Fed Laser-Heated Process", "Filament-fed laser-heated printing for optics/photonics"),
    ("bubbles2018", "T:Bubble formation in additive manufacturing of glass", "Bubble formation mechanisms in laser filament AM of glass"),
    ("seel2018", "10.1002/mawe.201800075", "Fused glass deposition modelling for the built environment (TU Darmstadt): laser melting of glass rod onto float glass"),
    ("pointfixings2024", "10.1007/s40940-024-00290-z", "Design of additively manufactured glass components for glass point fixings"),
    ("multimat2026", "10.1007/s40964-026-01543-9", "Review: multi-material glass AM"),
    ("regolithreview2023", "10.1007/s40964-023-00537-1", "Review: regolith sintering and 3D printing for lunar construction"),
    ("regolithvac2024", "T:Additive Manufacturing with Molten Lunar Regolith under Vacuum Conditions", "Molten regolith extrusion from Pt-Rh crucible under vacuum"),
    ("grotesk2022", "10.1007/978-3-030-96501-3_1", "GROTESK: LGD of glass for optical, thermal, structural components (LZH)"),
    ("pgm2010", "10.1595/147106710x514012", "Platinum-group metals in glass making: Pt-Rh bushings/nozzles, corrosion"),
    ("stern2024cgc", "10.47982/cgc.9.583", "Evenline/MIT: recycled float and container glass on G3DP3, VFT viscosity matching, IR thermography"),
    ("machines2026meltpool", "10.3390/machines14010122", "Melt pool dynamics / surface topography prediction in laser selective forming of optical glass"),
    ("packaging2026", "10.3390/ma19030506", "Packaging glasses review (containers to encapsulation)"),
    ("pfarr2023", "10.1007/s44150-022-00080-7", "Digitally manufactured thin glass composite facade panels"),
    ("lei2019cleo", "T:Additive Manufacturing of Fused Silica Glass Using Direct Laser Melting", "Paste extrusion + in-situ CO2 laser melting of fused silica (CLEO 2019)"),
    ("khmyrov2014", "T:On the possibility of selective laser melting of quartz glass", "Early SLM of quartz glass (Physics Procedia 2014)"),
    ("rammig2012", "T:Direct Glass Fabrication - New Applications of Glass with Additive Processes", "Torch-based direct glass fabrication of connections (Rammig 2012)"),
]

def http_get(url, **kw):
    for a in range(3):
        try:
            r = S.get(url, timeout=60, **kw)
            if r.status_code == 429: time.sleep(3); continue
            return r
        except requests.RequestException as e:
            log(f"   retry {a} {url}: {e}"); time.sleep(2)
    return None
def by_doi(doi):
    r = http_get(f"https://api.openalex.org/works/https://doi.org/{doi}"); return r.json() if r is not None and r.ok else None
def by_title(title):
    r = http_get("https://api.openalex.org/works", params={"search": title, "per-page": 5})
    if r is None or not r.ok: return None
    best, score = None, 0.0
    for w in r.json().get("results", []):
        s = difflib.SequenceMatcher(None, title.lower(), (w.get("title") or "").lower()).ratio()
        if s > score: best, score = w, s
    return best if score >= 0.80 else None
def bibtex_for(doi):
    r = http_get(f"https://doi.org/{doi}", headers={"Accept": "application/x-bibtex"})
    return r.text if r is not None and r.ok and r.text.strip().startswith("@") else None
def safe(s, n=40): return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")[:n]
def download_pdf(url, dest):
    r = http_get(url, headers={"Accept": "application/pdf,*/*"})
    if r is None or not r.ok or not r.content.startswith(b"%PDF"): return False
    dest.write_bytes(r.content); return True

mf = json.loads((ROOT / "sources" / "manifest.json").read_text(encoding="utf-8"))
have = {p["key"] for p in mf["papers"]}
for key, ident, relevance in SEEDS:
    if key in have and key != "pgm2010": continue
    log(f"[{key}] {ident}")
    w = by_title(ident[2:]) if ident.startswith("T:") else by_doi(ident)
    if not w:
        log("   !! not resolved"); mf["papers"].append({"key": key, "query": ident, "resolved": False, "relevance_summary": relevance}); continue
    doi = (w.get("doi") or "").replace("https://doi.org/", "")
    (DATA / "openalex" / f"{key}.json").write_text(json.dumps(w, indent=1), encoding="utf-8")
    authors = [a["author"]["display_name"] for a in w.get("authorships", [])]
    year = w.get("publication_year"); first = safe(authors[0].split()[-1]) if authors else "Anon"
    src = (w.get("primary_location") or {}).get("source") or {}
    entry = {"key": key, "doi": doi, "url": f"https://doi.org/{doi}" if doi else w.get("id"), "title": w.get("title"), "authors": authors,
             "year": year, "venue": src.get("display_name"), "is_oa": (w.get("open_access") or {}).get("is_oa"),
             "oa_url": (w.get("open_access") or {}).get("oa_url"), "local_path": None, "bibtex_path": None,
             "relevance_summary": relevance, "resolved": True}
    if doi:
        b = bibtex_for(doi)
        if b:
            p = DATA / "bibtex_raw" / f"{key}.bib"; p.write_text(b, encoding="utf-8"); entry["bibtex_path"] = str(p.relative_to(ROOT))
    cands = [l["pdf_url"] for l in [w.get("best_oa_location")] + (w.get("locations") or []) if l and l.get("pdf_url")]
    if entry["oa_url"]: cands.append(entry["oa_url"])
    dest = PAPERS / f"{year}_{first}_{safe(w.get('title') or key)}.pdf"
    for u in dict.fromkeys(cands):
        if download_pdf(u, dest): entry["local_path"] = str(dest.relative_to(ROOT)); log(f"   PDF ok <- {u}"); break
    mf["papers"] = [p for p in mf["papers"] if p["key"] != key] + [entry]
    time.sleep(0.3)

# direct extra downloads (known OA)
for u, name in [("https://www.diva-portal.org/smash/get/diva2:1650507/FULLTEXT03.pdf", "2022_Liu_PhD_thesis_Additive_manufacturing_of_fused_silica_glass_KTH.pdf")]:
    d = PAPERS / name
    if not d.exists() and download_pdf(u, d): log(f"   PDF ok <- {u}")
(ROOT / "sources" / "manifest.json").write_text(json.dumps(mf, indent=1, ensure_ascii=False), encoding="utf-8")
log(f"EXTRA DONE: papers in manifest = {len(mf['papers'])}, resolved = {sum(1 for p in mf['papers'] if p.get('resolved'))}, pdfs = {sum(1 for p in mf['papers'] if p.get('local_path'))}")
