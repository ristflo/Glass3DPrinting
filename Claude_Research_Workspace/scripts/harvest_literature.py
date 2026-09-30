#!/usr/bin/env python
"""
harvest_literature.py - OpenAlex/Crossref harvester for the molten-glass AM SOTA review.

For every seed item:
  * resolve metadata via OpenAlex (by DOI, or by title search with fuzzy match)
  * fetch validated BibTeX via DOI content negotiation (doi.org)
  * download an open-access PDF when OpenAlex exposes one
  * download patent PDFs from USPTO ppubs / Google patentimages
Writes: sources/manifest.json, sources/data/openalex/*.json, sources/data/bibtex_raw/*.bib,
        sources/data/harvest_log.txt
All paths are relative to the Claude_Research_Workspace/ root (parent of scripts/).
"""
import json, re, time, difflib, pathlib
import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAPERS = ROOT / "sources" / "papers"
PATENTS = ROOT / "sources" / "patents"
DATA = ROOT / "sources" / "data"
(DATA / "openalex").mkdir(parents=True, exist_ok=True)
(DATA / "bibtex_raw").mkdir(parents=True, exist_ok=True)
PAPERS.mkdir(parents=True, exist_ok=True)
PATENTS.mkdir(parents=True, exist_ok=True)
LOG = open(DATA / "harvest_log.txt", "a", encoding="utf-8")
S = requests.Session()
S.headers["User-Agent"] = "glass-am-sota-harvester/1.0 (academic literature review; python-requests)"


def log(msg):
    print(msg)
    LOG.write(msg + "\n")
    LOG.flush()


# ---------------------------------------------------------------- seed list
# (key, DOI or "T:<title>", relevance summary)
SEEDS = [
    # --- Direct molten extrusion (MIT lineage)
    ("klein2015", "10.1089/3dp.2015.0021", "G3DP: first molten soda-lime glass material-extrusion printer; kiln cartridge ~1040 C, AZS nozzle, annealing chamber"),
    ("inamura2018", "10.1089/3dp.2018.0157", "G3DP2: industrial-scale molten glass AM, 3-zone thermal control, 4-axis motion, 3 m columns Milan 2017"),
    ("mit2024masonry", "10.1007/s40940-024-00279-8", "Evenline G3DP3 recycled-glass interlocking masonry units; compressive strength data 3.6-118 MPa"),
    ("brun2017", "10.1098/rsta.2016.0156", "Molten glass sewing machine: viscous thread coiling instability applied to molten glass deposition"),
    ("tomotika1935", "10.1098/rspa.1935.0104", "Tomotika 1935 instability of a viscous thread in a viscous medium (viscous Rayleigh-Plateau)"),
    ("rayleigh1878", "10.1112/plms/s1-10.1.4", "Rayleigh 1878 On the instability of jets: classical capillary breakup, lambda_opt = 4.51 d"),
    # --- Filament / fiber-fed laser deposition (Missouri S&T / Notre Dame)
    ("luo2017sodalime", "T:Additive Manufacturing of Transparent Soda-Lime Glass Using a Filament-Fed Process", "Filament-fed CO2-laser AM of transparent soda-lime glass; optical quality vs furnace cast"),
    ("luo2018quartz", "T:Additive manufacturing of transparent fused quartz", "Filament-fed CO2 laser AM of fused quartz (Optical Engineering 2018)"),
    ("luo2017heat", "T:Heat Transfer in Additive Manufacturing of Glass", "Heat-transfer model of laser-heated glass filament deposition, temperature field and cooling gradients"),
    ("hostetler2018fiber", "T:Fiber-fed laser-heated process for printing transparent glass from single mode optical fiber", "Fiber-fed laser-heated glass printing from single-mode optical fiber (SPIE 2018)"),
    ("kinzel2025dgf", "T:Digital glass forming using direct heating techniques", "Review of digital glass forming via direct (laser/torch) heating, Kinzel group"),
    ("dgf2026control", "T:Temperature control of digital glass forming processes", "RT-Linux closed-loop temperature control of laser glass forming with thermal imaging"),
    # --- Laser glass deposition (LZH / Hannover)
    ("witzendorff2018", "T:Additive manufacturing of glass: CO2-Laser glass deposition printing", "LGD: CO2-laser melting of fused silica fibre; feed rate / power / velocity window"),
    ("lgd2021coaxial", "10.1117/12.2577205", "Coaxial laser glass deposition of fused silica: experiment and simulation"),
    ("lgd2022fibers", "10.1007/978-3-031-05918-6_18", "LGD of fused silica fibres for structural components"),
    ("lgd2024homog", "T:Experimental investigation on the surface and volume homogeneity of additive manufactured fused silica components in the Laser Glass Deposition process", "Surface/volume homogeneity (bubbles, striae) of LGD fused silica parts"),
    ("lgd2025tempctrl", "T:Temperature Control of Quartz-Glass Melting Areas in Laser Additive Manufacturing", "Pyrometric temperature control of quartz-glass melt zones in laser AM"),
    ("froehlich2022", "10.1007/978-3-030-95463-5_10", "Rod-fed CO2 laser AM with borosilicate and soda-lime glass (TU Ilmenau)"),
    # --- KTH / Nobula
    ("kth2022bonding", "10.3389/fmats.2022.978861", "Filament-based CO2 laser glass 3D printing: interlayer bonding and multilayer deposition, 196 um fused silica filament"),
    ("kth2024microlens", "T:Rapid Fabrication of Silica Microlens Arrays via Glass 3D Printing", "Direct glass laser deposition of silica microlens arrays (KTH/Nobula)"),
    # --- Powder-bed / DED alternatives
    ("fateri2015", "10.1111/ijac.12338", "SLM of soda-lime glass powder, 93% relative density"),
    ("khmyrov2016", "T:Crack-free selective laser melting of silica glass: single beads and monolayers on the substrate of the same material", "Crack-free SLM of silica glass single beads/monolayers"),
    ("datsiou2019", "10.1111/jace.16440", "LPBF of soda-lime glass in commercial system, processing window"),
    ("datsiou2021", "T:Laser powder bed fusion of soda lime silica glass: Optimisation of processing parameters and evaluation of part properties", "LPBF soda-lime glass parameter optimisation, density, roughness, strength"),
    ("spirrett2023", "10.1111/jace.18638", "Powder-fed DED of soda-lime silica glass on glass substrates"),
    ("lang2024", "10.1089/3dp.2022.0137", "Coaxial powder-fed laser AM of quartz glass"),
    ("paste2024", "T:Direct additive manufacturing of transparent fused silica glasses using an integrated paste printing and laser in-situ melting technology", "Hybrid paste printing + laser in-situ melting of fused silica"),
    ("boro2025laser", "10.3390/jmmp9090305", "Laser-based AM of alkali borosilicate glass powder: laser-beam properties vs quality"),
    ("slmsim2024", "10.1007/s00170-024-13076-y", "Simulation model of SLM of silica glass monolayer"),
    ("slmirregular2023", "T:Selective laser melting of glass with irregular shaped powder", "SLM of glass with irregular powder morphology"),
    ("ieee2019dlm", "T:Additive Manufacturing of Fused Silica Glass Using Direct Laser Melting", "Direct laser melting of fused silica (IEEE 2019)"),
    # --- Indirect routes (for the comparison matrix)
    ("kotz2017", "10.1038/nature22061", "Indirect: stereolithography of silica nanocomposite -> sintered transparent fused silica (Glassomer origin)"),
    ("mader2021", "10.1002/advs.202103180", "Indirect: melt-extrusion (FDM/FFD) of silica nanocomposite -> transparent fused silica"),
    ("nguyen2017", "T:3D-Printed Transparent Glass", "LLNL direct ink writing of silica sol inks -> transparent glass"),
    ("destino2018", "T:3D Printed Optical Quality Silica and Silica-Titania Glasses from Sol-Gel Feedstocks", "LLNL DIW gradient-index silica-titania optics"),
    ("toombs2022", "10.1126/science.abm6459", "Volumetric computed axial lithography of silica glass"),
    ("baudet2019", "10.1364/OME.9.002307", "Laval COPL: filament-fed FDM of chalcogenide glass (direct low-Tg melt extrusion)"),
    ("laval2023preform", "T:3D soft glass printing of preforms for microstructured optical fibers", "Direct soft-glass printing of fibre preforms"),
    # --- Reviews / books
    ("zhang2021review", "10.1007/s12200-020-1009-z", "Review: 3D printing of glass by AM techniques (FDM, SLS/SLM, SLA, DIW)"),
    ("critical2025", "10.3390/app15063414", "2025 critical review of glass AM incl. semi-solid/molten processing, architecture & art"),
    ("jmmp2026review", "10.3390/jmmp10080289", "2026 review: glass AM technologies, approaches, applications, challenges"),
    ("matdes2023review", "T:A comprehensive review on additive manufacturing of glass: Recent progress and future outlook", "Comprehensive review of glass AM 2023"),
    ("micromachines2022", "T:Overview of 3D-Printed Silica Glass", "Overview of 3D-printed silica glass routes"),
    ("solgel2025", "10.1007/s10971-025-06664-1", "Sol-gel technologies for AM of glass"),
    # --- Physics / materials background
    ("fluegel2007", "T:Glass viscosity calculation based on a global statistical modelling approach", "VFT-based global viscosity model for silicate glasses (basis for viscosity curves)"),
    ("aben2008", "T:Modern photoelasticity for residual stress measurement in glass", "Photoelastic residual stress measurement in glass (Aben et al.)"),
    ("pgm2010", "10.1595/147106710X508966", "Platinum-group metals (Pt-Rh) in glass making: bushings, nozzles, corrosion"),
    ("zircorr2025", "10.1111/ijac.15064", "Corrosion of zirconium-based refractories in glass-contact areas"),
    # --- Applications
    ("microfluidics2019", "10.1039/c8ay01934g", "Chemical analysis using 3D-printed glass microfluidics"),
    ("vti2022", "10.1145/3559400.3565596", "Applied viscous thread instability for 3D-printed foams (VTP model)"),
]

PATENT_SEEDS = [
    ("US9919510B2", "9919510", "MIT (Inamura, Lizardo, Stern, Houk, Achituv, Oxman): AM with molten glass, 4-axis bed, kiln temps, alumina nozzle"),
    ("US10464305B2", "10464305", "MIT continuation: Methods and apparatus for AM with molten glass"),
    ("US10266442B2", "10266442", "MIT (Klein, Stern, Oxman et al.): Methods and apparatus for additive manufacturing of glass (G3DP)"),
    ("US20210101818A1", "20210101818", "Corning Inc. application (abandoned): induction-heated Pt-Rh crucible/nozzle rod-fed glass extrusion"),
]


# ---------------------------------------------------------------- helpers
def http_get(url, **kw):
    for attempt in range(3):
        try:
            r = S.get(url, timeout=60, **kw)
            if r.status_code == 429:
                time.sleep(3)
                continue
            return r
        except requests.RequestException as e:
            log(f"   retry {attempt} {url}: {e}")
            time.sleep(2)
    return None


def openalex_by_doi(doi):
    r = http_get(f"https://api.openalex.org/works/https://doi.org/{doi}")
    return r.json() if r is not None and r.ok else None


def openalex_by_title(title):
    r = http_get("https://api.openalex.org/works", params={"search": title, "per-page": 5})
    if r is None or not r.ok:
        return None
    best, score = None, 0.0
    for w in r.json().get("results", []):
        s = difflib.SequenceMatcher(None, title.lower(), (w.get("title") or "").lower()).ratio()
        if s > score:
            best, score = w, s
    return best if score >= 0.80 else None


def bibtex_for(doi):
    r = http_get(f"https://doi.org/{doi}", headers={"Accept": "application/x-bibtex"})
    if r is not None and r.ok and r.text.strip().startswith("@"):
        return r.text
    return None


def safe(s, n=40):
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return s[:n]


def download_pdf(url, dest):
    r = http_get(url, headers={"Accept": "application/pdf,*/*"})
    if r is None or not r.ok:
        return False
    data = r.content
    if not data.startswith(b"%PDF"):
        return False
    dest.write_bytes(data)
    return True


# ---------------------------------------------------------------- run
manifest = {"generated": time.strftime("%Y-%m-%d %H:%M:%S"), "papers": [], "patents": []}
for key, ident, relevance in SEEDS:
    log(f"[{key}] {ident}")
    w = openalex_by_title(ident[2:]) if ident.startswith("T:") else openalex_by_doi(ident)
    if not w:
        log("   !! not resolved in OpenAlex")
        manifest["papers"].append({"key": key, "query": ident, "resolved": False, "relevance_summary": relevance})
        continue
    doi = (w.get("doi") or "").replace("https://doi.org/", "")
    (DATA / "openalex" / f"{key}.json").write_text(json.dumps(w, indent=1), encoding="utf-8")
    authors = [a["author"]["display_name"] for a in w.get("authorships", [])]
    year = w.get("publication_year")
    first = safe(authors[0].split()[-1]) if authors else "Anon"
    src = (w.get("primary_location") or {}).get("source") or {}
    entry = {
        "key": key,
        "doi": doi,
        "url": f"https://doi.org/{doi}" if doi else w.get("id"),
        "title": w.get("title"),
        "authors": authors,
        "year": year,
        "venue": src.get("display_name"),
        "is_oa": (w.get("open_access") or {}).get("is_oa"),
        "oa_url": (w.get("open_access") or {}).get("oa_url"),
        "local_path": None,
        "bibtex_path": None,
        "relevance_summary": relevance,
        "resolved": True,
    }
    if doi:
        bib = bibtex_for(doi)
        if bib:
            p = DATA / "bibtex_raw" / f"{key}.bib"
            p.write_text(bib, encoding="utf-8")
            entry["bibtex_path"] = str(p.relative_to(ROOT))
    cands = []
    for loc in [w.get("best_oa_location")] + (w.get("locations") or []):
        if loc and loc.get("pdf_url"):
            cands.append(loc["pdf_url"])
    if entry["oa_url"]:
        cands.append(entry["oa_url"])
    dest = PAPERS / f"{year}_{first}_{safe(w.get('title') or key)}.pdf"
    for u in dict.fromkeys(cands):
        if download_pdf(u, dest):
            entry["local_path"] = str(dest.relative_to(ROOT))
            log(f"   PDF ok <- {u}")
            break
    if not entry["local_path"]:
        log("   no OA PDF via OpenAlex")
    manifest["papers"].append(entry)
    time.sleep(0.3)

for pub, num, relevance in PATENT_SEEDS:
    log(f"[patent {pub}]")
    dest = PATENTS / f"{pub}.pdf"
    ok = download_pdf(f"https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/{num}", dest)
    if ok:
        log("   PDF ok <- USPTO ppubs")
    else:
        r = http_get(f"https://patents.google.com/patent/{pub}/en")
        m = re.search(r"https://patentimages\.storage\.googleapis\.com/[^\"']+\.pdf", r.text if r else "")
        if m and download_pdf(m.group(0), dest):
            ok = True
            log(f"   PDF ok <- {m.group(0)}")
    manifest["patents"].append({
        "key": pub,
        "url": f"https://patents.google.com/patent/{pub}/en",
        "local_path": str(dest.relative_to(ROOT)) if ok else None,
        "relevance_summary": relevance,
    })

(ROOT / "sources" / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
n_ok = sum(1 for p in manifest["papers"] if p.get("resolved"))
n_pdf = sum(1 for p in manifest["papers"] if p.get("local_path"))
n_pat = sum(1 for p in manifest["patents"] if p["local_path"])
log(f"DONE: {n_ok}/{len(SEEDS)} resolved, {n_pdf} paper PDFs, {n_pat}/{len(PATENT_SEEDS)} patent PDFs")
