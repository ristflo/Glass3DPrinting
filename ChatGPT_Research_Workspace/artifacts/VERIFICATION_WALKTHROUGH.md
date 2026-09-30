# Verification walkthrough

Generated from saved checks at 2026-09-30T09:18:08.295933+00:00.

## Delivery status

The eight-section technical review, executive summary, source index, bibliography, analysis scripts and source repository are assembled. This is a completed scoped review with the evidence and acquisition limits below; it is not an exhaustive literature search or an experimentally validated process specification. Run `package.py` after this audit; its external `package_validation.json` records the actual final ZIP result and hash.

## Compilation and PDF review

- Compiler: workspace-local Tectonic (XeTeX); successful exit status 0. Logs and intermediates are retained in `latex/build/` and `artifacts/compile_output.txt`.
- PDF: 27 pages, 37 bookmarks, 224 link annotations; SHA-256 `2bb29674f6ca9e6d90daf61050c8a959b9f8f12505e39ba9eb0cfc9fe7925303`.
- Final TeX log: 5 warnings. Remaining warnings are underfull text boxes, with no overfull boxes, missing glyphs or undefined citations/references detected.
- BibTeX warnings: 0. Undated web/datasheet entries use n.d.; publication dates are not inferred from access dates.
- Visual review: All 27 pages visually checked at contact-sheet scale. Selected tables and bibliography inspected at larger scale. No clipped text, overlapping cells, missing figures or blank unintended pages observed. Five small underfull spacing warnings remain; some tables are dense and a source schematic has limited native resolution. This is layout inspection, not full typographic proofreading.
- Review evidence: `pdf_inspection.json`, `visual_review.json`; rendered pages are scratch files and are intentionally excluded from the portable archive.

## Citations, assets and calculations

- 43 bibliography entries; 43 unique cited keys; 80 source/asset ledger records (not 80 distinct publications).
- No missing citation keys, required article metadata, referenced figures, asset parse errors or original-ledger hash mismatches.
- 16 PDFs in papers/ (13 research/review PDFs and 3 manufacturer datasheets); 3 patent PDFs; 5 files in media/.
- WO2020118157A1 is a 91-page image-based PDF: it opens successfully but has no extractable text. Full-text search of that local file requires OCR, not supplied here.
- Nominal viscosity fits, units, inverse thresholds and flow-scaling checks passed on 29 September. The engineering script reran successfully on 30 September after correcting the BOROFLOAT property temperature labels; numerical results are unchanged.
- Final source review corrected Toombs roughness profile lengths, BOROFLOAT conductivity/heat-capacity reference ranges, the November 2025 Corning publication date, and the reported G3DP2 build envelope. See `notes/academic_notes/final_review_20260930.md`.

## External links

- Saved check dates: 2026-09-29. 74 unique links checked; 62 returned HTTP <400; 12 returned access failures.
- A response is an accessibility check, not proof of video playback or content validity. 403/405 responses may reflect blocking; they are not silently classified as valid or dead.

| HTTP status | URL |
|---|---|
| 403 | https://doi.org/10.1002/adma.201701181 |
| 403 | https://doi.org/10.1002/admt.201700323 |
| 403 | https://doi.org/10.1089/3dp.2015.0021 |
| 403 | https://doi.org/10.1089/3dp.2018.0157 |
| 403 | https://doi.org/10.1089/3dp.2022.0112 |
| 403 | https://doi.org/10.1098/rspa.1935.0104 |
| 403 | https://doi.org/10.1111/jace.16440 |
| 403 | https://doi.org/10.1112/plms/s1-10.1.4 |
| 403 | https://doi.org/10.1126/science.abm6459 |
| 403 | https://doi.org/10.3390/mi16010029 |
| 405 | https://dspace.mit.edu/bitstreams/7dbd523f-a0c1-4274-94e1-a370ca822c2c/download |
| 403 | https://www.monash.edu/monash-innovation/impact/generator-founders/maple-glass-printing |

## Containment

- All commands that created or modified deliverables in this finishing pass targeted `ChatGPT_Research_Workspace/`. Claude and Antigravity workspaces were not edited.
- Project-root file changes since the 30 September resume snapshot: [].
- The original 26 September baseline differs for `Antigravity_Research_Instructuctions_20260926.md`; that difference already existed when this finishing pass began. The audit does not establish who changed it, and does not claim that the entire project root has been unchanged since 26 September.
- Root inventories compare immediate root files, not a recursive historical audit of unrelated workspaces. Original and resume snapshots are retained.

## Acquisition and evidence limits

- No separately catalogued nozzle cross-section or thermal-camera frame was acquired. The archive includes apparatus, laser-heating, deposited-track, printed-part and photoelasticity images. The photoelasticity specimen is conventional tempered glass.
- Not all downloaded raster figures meet 300 dpi at their placed size. In particular the Liu schematic is only 498 x 352 pixels. It was not upscaled and relabeled high resolution. Original analytical plots also have vector PDF versions.
- Video streaming links are logged; playback was not verified and binaries were not copied.
- Matched-route tensile and optical datasets, current verified printer prices and yields, material-specific refractory lifetime, and grade-specific liquidus/kinetics remain gaps. Conventional forming costs are discussed qualitatively; numerical costs are hypothetical scenarios, not sourced matched-part quotations.
- Direct molten-inorganic-glass apparatus attribution remains unverified for some requested institutions. No machine names, numerical TRLs or missing performance values were invented.
- Third-party PDFs and figures retain their individual rights. The archive is a local research collection, not a blanket permission to redistribute every source. Media credits and the Chhadeh CC BY-NC-ND limitation are retained in README and media notes.

## Acquired PDF inventory

| Workspace path | Pages | Extractable characters |
|---|---:|---:|
| `sources/papers/2015_Klein_Additive_Manufacturing_of_Optically_Transparent_Glass.pdf` | 18 | 51516 |
| `sources/papers/2018_Inamura_Additive_Manufacturing_of_Transparent_Glass_Structures.pdf` | 16 | 60317 |
| `sources/papers/2018_Witzendorff_Additive_manufacturing_of_glass_CO2_Lase.pdf` | 4 | 12413 |
| `sources/papers/2019_Datsiou_Additive_manufacturing_of_glass_with_las.pdf` | 5 | 23152 |
| `sources/papers/2021_Datsiou_Laser_powder_bed_fusion_of_soda_lime_sil.pdf` | 10 | 46688 |
| `sources/papers/2022_Liu_Investigation_of_glass_bonding_and_multi.pdf` | 10 | 36525 |
| `sources/papers/2022_Spirrett_Powder_fed_directed_energy_deposition_of.pdf` | 14 | 56335 |
| `sources/papers/2022_Toombs_Volumetric_additive_manufacturing_of_sil.pdf` | 42 | 51143 |
| `sources/papers/2024_Massimino_Additive_manufacturing_of_interlocking_g.pdf` | 21 | 77549 |
| `sources/papers/2024_Sleiman_Experimental_investigation_on_the_surfac.pdf` | 4 | 17594 |
| `sources/papers/2024_Zhang_A_simulation_model_of_selective_laser_me.pdf` | 11 | 34252 |
| `sources/papers/2025_Murthi_Sol_gel_technologies_for_additive_manufa.pdf` | 15 | 70571 |
| `sources/papers/2026_Chhadeh_Toolpath_Design_Mechanical_Strength.pdf` | 11 | 45609 |
| `sources/papers/phys_ar.pdf` | 16 | 10157 |
| `sources/papers/phys_boro.pdf` | 1 | 2222 |
| `sources/papers/phys_silica.pdf` | 8 | 11687 |
| `sources/patents/AU2021289614A1.pdf` | 60 | 99452 |
| `sources/patents/US10266442B2.pdf` | 34 | 119077 |
| `sources/patents/WO2020118157A1.pdf` | 91 | 0 |

## Production raster resolution

| Workspace path | Width (px) | Height (px) |
|---|---:|---:|
| `latex/figures/Efferz2024_Figure2.png` | 873 | 640 |
| `latex/figures/flow_sensitivity.png` | 2190 | 1320 |
| `latex/figures/Liu2022_Figure1.jpg` | 498 | 352 |
| `latex/figures/Liu2022_Figure6.jpg` | 941 | 920 |
| `latex/figures/Massimino2024_Figure1.png` | 874 | 1213 |
| `latex/figures/Massimino2024_Figure2.png` | 1371 | 772 |
| `latex/figures/process_architecture.png` | 2700 | 1320 |
| `latex/figures/viscosity_residuals.png` | 2100 | 990 |
| `latex/figures/viscosity_vft.png` | 3450 | 1440 |

## Original media inventory

- `sources/media/Efferz2024_Figure2.png` (68,277 bytes)
- `sources/media/Liu2022_Figure1.jpg` (30,917 bytes)
- `sources/media/Liu2022_Figure6.jpg` (130,050 bytes)
- `sources/media/Massimino2024_Figure1.png` (1,355,836 bytes)
- `sources/media/Massimino2024_Figure2.png` (1,738,417 bytes)

The master CSV and MANIFEST source records provide URLs, source identities and download provenance. Packaging adds a SHA-256 inventory of every archived file except the manifest itself. The adjacent package receipt verifies the archive CRC and every member against the corresponding workspace bytes.
