# Molten glass additive manufacturing research

Compiled report and source archive from research begun 26 September 2026, with source verification on 29 September and final editorial review on 30 September. This is a scoped technical evidence review, not a certified systematic review or a qualified process design.

## Deliverables

- `output/glass_3d_printing_sota_monograph.pdf`: eight-section report.
- `output/glass_3d_printing_report.zip`: portable sources and deliverables, with temporary tooling excluded.
- `output/executive_summary.md`: principal conclusions and limitations.
- `output/master_source_index.csv`: source/asset records, including distinct records for the same paper where needed for provenance.
- `artifacts/MANIFEST.json`: integrated source ledger and generated-file inventory.
- `artifacts/VERIFICATION_WALKTHROUGH.md`: actual checks, build status and remaining gaps.

## Reproduce

Use Python 3.12 with `scripts/requirements.txt`. Set temporary/cache directories inside `scripts/tmp/`. The scripts resolve output paths from their own location.

1. `python scripts/analysis/plot_viscosity.py`
2. `python scripts/analysis/engineering_models.py`
3. `python scripts/analysis/commercial_economics.py`
4. `python scripts/processors/integrate.py`
5. In PowerShell: `./scripts/build.ps1` (workspace-local Tectonic, or installed latexmk/XeLaTeX).
6. `python scripts/processors/verify.py --links`
7. `python scripts/processors/inspect_pdf.py`; visually inspect the rendered pages in `scripts/tmp/pdf_review/`.
8. Update `artifacts/visual_review.json` to record the reviewed PDF hash and findings, then run `python scripts/processors/finalize_audit.py`.
9. `python scripts/processors/package.py` (after final review). This updates the manifest inventory and verifies the ZIP CRC and every member's SHA-256 against the workspace.

The report uses Unicode fonts and therefore requires XeLaTeX/Tectonic, not plain pdfLaTeX. The helper supports TeX Gyre fonts. An initial Tectonic run fetches its resource bundle; subsequent runs can reuse the workspace cache. Compiler binaries, virtual environments and caches are excluded from the ZIP. Do not rerun acquisition scripts merely to reproduce the report; the archived sources suffice, and some historical acquisition paths may have moved.

Extract the ZIP into its own directory and use that directory as the workspace root. Archive entries are workspace-relative. `artifacts/package_validation.json` sits beside the archive in the original workspace and records the final archive hash; it is excluded from the ZIP to avoid a circular hash. `MANIFEST.json` inventories all other archived files but does not hash itself. Undated sources use `n.d.` in the bibliography; this does not replace unknown dates with the access year.

## Model limitations

Viscosity fits use nominal product-specific manufacturer anchors. Solid plot segments are within the fitting interval, not a guarantee of model validity. Dashed curves are extrapolations. HPFS 7980 uses an approximate Arrhenius limit of VFT and has larger residuals. The extrapolated working point is not a recommended temperature. Flow, stress, thermal and cost calculations are explicitly illustrative, not measured equipment performance.

## Attribution and third-party materials

Downloaded articles and figures retain their original copyrights and individual terms. See `notes/summaries/media_captions.md` and the source ledger. Several figures are CC BY 4.0. The unchanged Chhadeh 2026 article is CC BY-NC-ND 4.0; commercial redistribution or adapted reproductions are not licensed by this archive. Repository availability alone does not establish a blanket redistribution license. Video links are provided rather than copied video binaries; HTTP accessibility is not playback verification.

All generated work is contained in `ChatGPT_Research_Workspace/`. Other project workspaces are separate.
