#!/usr/bin/env python
"""harvest_toolpath_optics.py - supplementary harvest (2026-09-29, search round I):
literature on toolpath / deposition-parameter optimisation of transparent extruded materials for optical
function (transparency, caustics, reflection, translucency). Writes sources/data/bibtex_raw/<key>.bib,
sources/data/openalex/<key>.json, open-access PDFs to sources/papers/, and appends records to sources/manifest.json."""
import json, pathlib, re, time, urllib.request
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "sources" / "data"
PAPERS = ROOT / "sources" / "papers"
UA = {"User-Agent": "Mozilla/5.0 (research harvest; mailto:frist@fs.tum.de)"}


def get(url, headers=None, timeout=60):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


# key, doi, oa_pdf_url (or None), relevance summary
SEEDS = [
    ("weber2020photon", "10.1016/j.buildenv.2020.106957", None,
     "Radiance photon-mapping (forward light simulation) of geometrically complex 3D-printed glass; benchmarked against measurements on G3DP printed columns"),
    ("kassubeck2021caustics", "10.1109/WACV48630.2021.00292",
     "https://openaccess.thecvf.com/content/WACV2021/papers/Kassubeck_Shape_From_Caustics_Reconstruction_of_3D-Printed_Glass_From_Simulated_Caustic_WACV_2021_paper.pdf",
     "Inverse rendering: reconstruct 3D-printed glass shape from its caustic image with differentiable light transport and a deposited-volume regulariser (TU Braunschweig)"),
    ("chhadeh2026toolpath", "10.1038/s44334-026-00072-1", "https://www.nature.com/articles/s44334-026-00072-1.pdf",
     "Effect of toolpath design and layer orientation on bending strength of rod-fed FDM-type soda-lime glass parts (TU Darmstadt); mechanical objective only"),
    ("rettschlag2020microlens", "10.1016/j.procir.2020.09.052", None,
     "Laser glass deposition of fused-silica spheres for micro-lens matrices: deposition parameters set lens geometry (LZH Hannover)"),
    ("kranert2020waveguide", "10.1117/12.2554516", None,
     "Curved, nearly stress-free waveguides by CO2-laser deposition of coreless fused-silica fibres: deposition path defines light guiding (LZH Hannover)"),
    ("hong2023germanate", "10.3390/photonics10040378", "https://www.mdpi.com/2304-6732/10/4/378/pdf",
     "Fiber-fed laser printing of germanate glass spherical/aspherical lenses with temperature feedback; deposition strategy defines optical surface"),
    ("dyllaspears2020grin", "10.1126/sciadv.abc7429", None,
     "LLNL direct-ink-writing GRIN glass optics: refractive-index profile programmed into the toolpath via inline ink mixing (indirect route)"),
    ("sage2026fermat", "10.1016/j.addma.2026.105214", None,
     "LLNL gradient multimaterial toolpath generation (connected Fermat spirals, velocity compensation) for DIW of graded optics such as GRIN glass"),
    ("kumar2022transparency", "10.1080/2374068x.2022.2153518", None,
     "Parametric study of FFF transparent PLA: layer height, temperature, raster angle, orientation, road width, speed vs UV-Vis transmittance"),
    ("kumar2024transparency", "10.1016/j.optlastec.2024.110865", None,
     "Multi-response optimisation of FFF PLA transparency and spatial resolution (layer height, road width, deposition speed)"),
    ("vochozka2024translucency", "10.3390/polym16202862", "https://www.mdpi.com/2073-4360/16/20/2862/pdf",
     "Six FFF parameters (orientation, layer height, temperature, fan, extrusion multiplier, speed) vs translucency of PLA parts"),
    ("quero2021microfluidic", "10.1039/d1lc00518a", None,
     "FDM transparent microfluidics: layer height/width and nozzle geometry vs resolution and ~80% visible transmission"),
    ("hamp2021transmittance", "10.1364/ao.427525", None,
     "Spectral transmittance of FDM samples vs layer height/width, temperature, speed and orientation (Applied Optics)"),
    ("amendola2021diffuse", "10.1371/journal.pone.0253181",
     "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0253181&type=printable",
     "Absorption/scattering coefficients of FDM PLA and ABS parts as a function of printing parameters for diffuse-optics phantoms"),
    ("ren2023anisotropy", "10.1016/j.optmat.2023.113743", None,
     "Optical anisotropy (birefringence) of 3D-printed transparent polymers and its dependence on the printing process"),
    ("blachowicz2021optical", "10.1515/epoly-2021-0061", None,
     "Review of optical elements from 3D-printed polymers incl. FDM lenses whose scattering is tuned by nozzle diameter and raster angle"),
    ("rooney2024lenses", "10.1002/admt.202400043", None,
     "Printing, characterising and assessing transparent 3D-printed lenses for imaging; layer artefacts removed by spin-coated resin"),
    ("gao2023review", "10.1016/j.mattod.2023.06.019", None,
     "Review: 3D printed optics and photonics - processes, materials, applications (Materials Today)"),
    ("heinrich2016optics", "10.1515/aot-2016-0021", None,
     "Review: additive manufacturing of optical components (Advanced Optical Technologies)"),
    ("anisotag2023", "10.1145/3544548.3581024", "https://arxiv.org/pdf/2301.10599",
     "AnisoTag: FDM toolpath direction encodes reflection anisotropy of printed surfaces (CHI 2023)"),
    ("papas2011caustics", "10.1111/j.1467-8659.2011.01876.x", None,
     "Goal-based caustics: micro-facet refractive surface optimised so refracted light forms a target image"),
    ("kiser2013caustics", "10.1007/978-3-7091-1251-9_7", None,
     "Architectural caustics: continuous refractive/reflective surfaces controlling light with geometry"),
    ("yue2014caustics", "10.1145/2580946", None,
     "Poisson-based continuous surface generation for goal-based caustics"),
    ("schwartzburg2014caustics", "10.1145/2601097.2601200", None,
     "High-contrast computational caustic design via optimal transport; fabricated in acrylic/glass by CNC milling"),
    ("pereira2014routing", "10.1145/2602140", None,
     "Computational light routing: automatically designed 3D-printed optical fibres inside multi-material printed objects"),
    ("willis2012printedoptics", "10.1145/2380116.2380190", None,
     "Printed Optics: embedding light pipes, lenses and sensors in 3D-printed clear objects"),
    ("brunton2018translucency", "10.1145/3197517.3201349", None,
     "3D printing spatially varying colour and translucency via multi-material halftoning"),
    ("elek2017scattering", "10.1145/3130800.3130890", None,
     "Scattering-aware texture reproduction: inverse volumetric material assignment for 3D printing"),
    ("dong2010sss", "10.1145/1778765.1778799", None,
     "Fabricating spatially varying subsurface scattering by layered material stacks"),
    ("papas2013translucent", "10.1145/2461912.2461974", None,
     "Fabricating translucent materials using continuous pigment mixtures"),
    ("zhao2016lampshades", "10.1145/2907049", "https://arxiv.org/pdf/1510.03023",
     "Printed perforated lampshades whose hole distribution projects a target continuous image"),
    ("weyrich2009microgeometry", "10.1145/1531326.1531338", None,
     "Fabricating microgeometry (milled microfacets) for custom surface reflectance"),
    ("nagasawa2023translucency", "10.3390/jimaging9050105", "https://www.mdpi.com/2313-433X/9/5/105/pdf",
     "Perceived translucency of 3D-printed objects controlled through surface texture"),
]

mf = json.loads((ROOT / "sources" / "manifest.json").read_text(encoding="utf-8"))
existing = {p["key"] for p in mf["papers"]}
log = []
for key, doi, pdf, summary in SEEDS:
    rec = {"key": key, "doi": doi, "url": f"https://doi.org/{doi}", "title": None, "authors": [], "year": None,
           "venue": None, "is_oa": None, "oa_url": None, "local_path": None, "bibtex_path": None,
           "relevance_summary": summary, "resolved": False,
           "search_round": "I (2026-09-29): toolpath optimisation for optical properties"}
    # OpenAlex metadata
    try:
        w = json.loads(get(f"https://api.openalex.org/works/https://doi.org/{doi}?mailto=frist@fs.tum.de"))
        (DATA / "openalex" / f"{key}.json").write_text(json.dumps(w, indent=1), encoding="utf-8")
        rec.update({"title": w.get("title"),
                    "authors": [a["author"]["display_name"] for a in w.get("authorships", [])],
                    "year": w.get("publication_year"),
                    "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                    "is_oa": (w.get("open_access") or {}).get("is_oa"),
                    "oa_url": (w.get("open_access") or {}).get("oa_url"), "resolved": True})
    except Exception as e:
        log.append(f"{key}: openalex FAIL {e}")
    # BibTeX via doi.org content negotiation
    try:
        bib = get(f"https://doi.org/{doi}", headers={"Accept": "application/x-bibtex"}).decode("utf-8")
        if bib.strip().startswith("@"):
            p = DATA / "bibtex_raw" / f"{key}.bib"
            p.write_text(bib.strip() + "\n", encoding="utf-8")
            rec["bibtex_path"] = str(p.relative_to(ROOT)).replace("\\", "/")
            if not rec["title"]:
                m = re.search(r"title\s*=\s*\{(.+?)\}", bib)
                rec["title"] = m.group(1) if m else None
                rec["resolved"] = True
        else:
            log.append(f"{key}: bibtex response not BibTeX")
    except Exception as e:
        log.append(f"{key}: bibtex FAIL {e}")
    # OA PDF
    url = pdf or rec.get("oa_url")
    if url and "pdf" in url.lower():
        try:
            data = get(url, headers={"Accept": "application/pdf"}, timeout=90)
            if data[:5] == b"%PDF-":
                first = (rec["authors"][0].split()[-1] if rec["authors"] else key)
                short = re.sub(r"[^A-Za-z0-9]+", "_", (rec["title"] or key))[:40].strip("_")
                fn = f"{rec['year'] or 'nd'}_{first}_{short}.pdf"
                (PAPERS / fn).write_bytes(data)
                rec["local_path"] = f"sources/papers/{fn}"
            else:
                log.append(f"{key}: pdf response not PDF ({url})")
        except Exception as e:
            log.append(f"{key}: pdf FAIL {e}")
    if key in existing:
        mf["papers"] = [rec if p["key"] == key else p for p in mf["papers"]]
    else:
        mf["papers"].append(rec)
    print(f"{key:26s} resolved={rec['resolved']} bib={'y' if rec['bibtex_path'] else 'n'} "
          f"pdf={'y' if rec['local_path'] else 'n'} | {(rec['title'] or '')[:60]}")
    time.sleep(0.4)
mf["supplement_round_I"] = time.strftime("%Y-%m-%d %H:%M:%S")
(ROOT / "sources" / "manifest.json").write_text(json.dumps(mf, indent=1, ensure_ascii=False), encoding="utf-8")
with (DATA / "harvest_log.txt").open("a", encoding="utf-8") as fh:
    fh.write("\n# round I " + time.strftime("%Y-%m-%d") + "\n" + "\n".join(log) + "\n")
print("\n".join(log) if log else "no errors")
