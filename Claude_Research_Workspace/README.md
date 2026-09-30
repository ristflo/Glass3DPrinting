# Claude_Research_Workspace — Molten Hot Glass Additive Manufacturing: SOTA review workspace

Generated autonomously on 2026-09-26 following `Claude_Research_Instructuctions_20260926.md.md`.
Everything produced by the run lives in this folder; the project root was not written to.

## Deliverables
| Item | Path |
|---|---|
| Compiled monograph (43 pages, ~13,000 prose words + 3 directory tables, 147 references) | `glass_3d_printing_sota_monograph.pdf` (copy of `latex/build/main.pdf`) |
| LaTeX source (modular) | `latex/main.tex`, `latex/sections/01_…08_*.tex`, `latex/references.bib`, `latex/figures/` |
| Machine-readable source ledger | `sources/manifest.json` (papers, patents, media, figures, deliverables) |
| Hyperlink validation | `sources/data/link_check.csv` |
| Reconstructed abstracts of all resolved works | `sources/data/abstracts_dump.md` |
| Search-round log incl. negative findings | `notes/search_log.md` |
| Literature note, round I (2026-09-29): toolpath optimisation of transparent deposited materials for optical properties — feeds Problem 9 of Section 5 | `notes/toolpath_optics_literature.md` |
| Cross-workspace synthesis (30 September 2026): consolidated summary of the Claude, ChatGPT and Antigravity results as Markdown, LaTeX and PDF, with redrawn figures | `synthesis/` (see `synthesis/README.md`) |

## Harvested assets
| Category | Count | Location |
|---|---|---|
| Peer-reviewed / scholarly works resolved via OpenAlex + Crossref (DOI-validated BibTeX) | 66 of 68 seeds (rounds A–H) + 33 of 33 (round I) | `sources/data/openalex/*.json`, `sources/data/bibtex_raw/*.bib` |
| Open-access paper PDFs on disk | 23 | `sources/papers/YYYY_Author_ShortTitle.pdf` |
| Patent PDFs (USPTO) | 4 (US 9,919,510; US 10,464,305; US 10,266,442; US 2021/0101818 A1) | `sources/patents/` |
| Licensed media (CC BY / CC BY-SA) | 9 KTH figures + 1 MIT G3DP photograph (+ licence log) | `sources/media/` |
| Generated analytical figures | 7 (VFT curves, Rayleigh–Plateau/Tomotika, cord cooling, taxonomy, two machine schematics, timeline) | `latex/figures/` |
| Extracted text of PDFs (for quantitative mining) | 20 | `sources/data/text/` |

## Reproduction
```
scripts/harvest_literature.py    # OpenAlex/Crossref harvest, PDFs, BibTeX  (python + requests)
scripts/harvest_extra.py         # supplementary seed batch
scripts/harvest_toolpath_optics.py  # round I (2026-09-29): toolpath-for-optics literature; set PYTHONIOENCODING=utf-8 on Windows
scripts/fetch_repositories.py    # DSpace-API and Commons downloads
scripts/extract_pdf_text.py      # pypdf text extraction
scripts/make_figures.py          # matplotlib/scipy figures  (scripts/tmp/venv)
scripts/build_bib.py             # references.bib from raw BibTeX + curated entries; citation check
scripts/sanitize_bib.py          # HTML entities / Unicode / underscores -> LaTeX
scripts/check_links.py           # URL + DOI validation
cd latex && ../scripts/tmp/tectonic/tectonic.exe -X compile --outdir build main.tex
```
No system-wide LaTeX was installed: the self-contained Tectonic 0.17 engine lives in `scripts/tmp/tectonic/`
(its package cache in `scripts/tmp/tectonic_cache/`). Python packages were installed into `scripts/tmp/venv/` only.

## Known limitations
- 56 DOI/URL targets return HTTP 403 to automated checkers (Wiley, Liebert, Royal Society, ASME, Science, ACM, Crunchbase, Monash, ResearchGate, ScienceDirect). They resolve in a browser; see `link_check.csv`.
- Maple Glass Printing's website returned 404 on the run date; the company reference was replaced by a news article.
- Two seeds could not be resolved in OpenAlex (`dgf2026control` was added manually from Crossref; the molten-regolith preprint is cited by its ResearchGate listing).
- No molten-glass AM publications were found for Nagaoka University of Technology, McGill, Fraunhofer IKTS/ISC/IPT or RISE; the monograph states these negative findings explicitly.
