#!/usr/bin/env python
"""tidy_sources.py - remove duplicate / off-topic PDFs and link directly downloaded PDFs to manifest entries."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "sources" / "papers"
mf = json.loads((ROOT / "sources" / "manifest.json").read_text(encoding="utf-8"))
by_key = {p["key"]: p for p in mf["papers"]}

# duplicates and off-topic
for name in ["2024_ChallengingGlass_Advancing_sustainable_3D_printing_feasibility.pdf",  # duplicate of 2024_Stern_... (stern2024cgc)
             "2018_SFF_Precision_enhancement_in_situ_metrology.pdf"]:                     # UCLA polymer metrology paper, not glass
    f = P / name
    if f.exists():
        f.unlink(); print("removed", name)

# link direct downloads
links = {
    "klein2015": "2015_Klein_Additive_Manufacturing_of_Optically_Transparent_Glass.pdf",
    "inamura2018": "2018_Inamura_Additive_Manufacturing_of_Transparent_Glass_Structures.pdf",
    "fluegel2007": "2007_Fluegel_Glass_viscosity_calculation_global_statistical_model.pdf",
}
for k, name in links.items():
    if k in by_key and (P / name).exists():
        by_key[k]["local_path"] = f"sources/papers/{name}"; print("linked", k)

extra = [
    {"key": "liu2022thesis", "doi": "", "url": "https://www.diva-portal.org/smash/get/diva2:1650507/FULLTEXT03.pdf",
     "title": "Additive manufacturing of fused silica glass (Doctoral thesis, KTH)", "authors": ["Chunxin Liu"], "year": 2022,
     "venue": "KTH Royal Institute of Technology (DiVA)", "is_oa": True,
     "local_path": "sources/papers/2022_Liu_PhD_thesis_Additive_manufacturing_of_fused_silica_glass_KTH.pdf",
     "relevance_summary": "Doctoral thesis underpinning the KTH/Nobula direct glass laser deposition process", "resolved": True},
    {"key": "arxiv2001_03589", "doi": "", "url": "https://arxiv.org/abs/2001.03589",
     "title": "Freeform microfluidic networks encapsulated in laser printed three-dimensional macro-scale glass objects (arXiv preprint)",
     "authors": ["(see arXiv listing)"], "year": 2020, "venue": "arXiv", "is_oa": True,
     "local_path": "sources/papers/2020_Freeform_microfluidic_networks_laser_printed_glass_arxiv.pdf",
     "relevance_summary": "Laser-printed glass with embedded microfluidic channels (application vertical: microfluidics)", "resolved": True},
]
for e in extra:
    if e["key"] not in by_key and (ROOT / e["local_path"]).exists():
        mf["papers"].append(e); print("added", e["key"])

(ROOT / "sources" / "manifest.json").write_text(json.dumps(mf, indent=1, ensure_ascii=False), encoding="utf-8")
pdfs = sorted(P.glob("*.pdf"))
linked = {p.get("local_path") for p in mf["papers"] if p.get("local_path")}
print("PDFs on disk:", len(pdfs), "| manifest entries with local PDF:", len(linked))
for f in pdfs:
    if f"sources/papers/{f.name}" not in linked: print("  unlinked:", f.name)
