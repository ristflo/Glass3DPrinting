# Cross-workspace synthesis

Consolidated summary of the three research workspaces in `C:\Dev\Glass3DPrinting`
(Claude, ChatGPT, Antigravity), written on 30 September 2026.

## Deliverables

| File | Content |
|---|---|
| `glass_am_combined_summary.md` | The summary in Markdown, with numbered figures, tables and references |
| `glass_am_combined_summary.tex` | The same content as a LaTeX article (natbib, `references.bib`) |
| `glass_am_combined_summary.pdf` | Compiled from the LaTeX file, 24 pages |
| `figures/` | Twelve figures as PDF and PNG, plus two third-party images |

## How it is built

Both deliverables are generated from one source so that they cannot drift apart.

```text
summary_master.md                    the text, in a small Markdown subset
scripts/make_figures.py              redraws every analytical figure into figures/
scripts/build_summary.py             writes the .md and .tex deliverables, checks citations and references
references.bib                       ../latex/references.bib plus references_extra.bib
```

```bash
# from Claude_Research_Workspace/synthesis, with PYTHONIOENCODING=utf-8 on Windows
../scripts/tmp/venv/Scripts/python.exe scripts/make_figures.py
python scripts/build_summary.py
../scripts/tmp/tectonic/tectonic.exe -X compile --keep-logs --outdir build glass_am_combined_summary.tex
```

Edit `summary_master.md`, not the generated files. `references_extra.bib` holds six sources that only the
ChatGPT workspace had; rerun `cat ../latex/references.bib references_extra.bib > references.bib` if the
monograph bibliography changes.

## Third-party images

- `figures/fig_g3dp3_photos.png`: Figures 1 and 2 of Massimino et al. 2024 (doi:10.1007/s40940-024-00279-8),
  CC BY 4.0, scaled to a common height and placed side by side. Source files are in the ChatGPT workspace.
- `figures/commons_caustics.jpg`: photograph by Neri Oxman, Wikimedia Commons, CC BY-SA 4.0, unchanged.

The other workspaces were read but not modified.
