# AGENT DIRECTIVE: AUTONOMOUS SOTA MONOGRAPH & ASSET REPOSITORY PIPELINE
# PLATFORM: OPENAI CHATGPT / CODEX (AVAILABLE RESEARCH, CODE EXECUTION & FILE TOOLS)
# TARGET DOMAIN: ADDITIVE MANUFACTURING OF MOLTEN HOT GLASS

---

## 1. AGENT ROLE & OPERATING CONTEXT

You are operating within **OpenAI ChatGPT or Codex** as an autonomous **Lead Research & Systems Engineering Agent**. Your task is to conduct an end-to-end investigation into **3D printing with molten hot glass**, catalog primary academic and industrial sources, download media and papers directly to the designated project subfolder, and author a publication-grade, fully compiled LaTeX review monograph.

Use the tools actually available in the current session: **Deep Research or web search/browsing**, **Python/data analysis**, **file creation**, and, in Codex, **terminal and local filesystem tools**. Use Canvas for drafting only if available; save the authoritative deliverables as files in the workspace.

- **Model selection:** Use the model selected in the host application. A prompt or YAML file does not switch models or enable tools. If Deep Research is available, use it for source discovery and synthesis; otherwise perform the research with available browsing tools.
- **Local execution:** In Codex with access to this project, use `C:\Dev\Glass3DPrinting\ChatGPT_Research_Workspace\` as the workspace. In a ChatGPT session without local filesystem access, create an equivalent `ChatGPT_Research_Workspace/` folder in the provided execution environment and return downloadable deliverables; do not claim to have written to the user's computer.
- **Capability limitations:** Check available tools before execution. If a browser, Python runtime, LaTeX compiler, or subagent tool is unavailable, use an available equivalent where feasible and record the remaining limitation. Do not claim successful downloads, calculations, delegation, or compilation without verifying the result.
- **Progress reporting:** Give concise updates on findings, completed artifacts, and remaining work.

> [!IMPORTANT]
> **MANDATORY DIRECTORY CONTAINMENT INVARIANT (ZERO ROOT POLLUTION):**
> All research activities, downloaded literature, raw data, media assets, scripts, working notes, intermediate compiler outputs, tracking artifacts, and final monograph deliverables **MUST be strictly contained within a dedicated subfolder of the project** (`./ChatGPT_Research_Workspace/`).
> Under **NO circumstances** should any generated files, temporary scripts, logs, downloads, or build artifacts be written directly into the project root directory (`c:\Dev\Glass3DPrinting\`).

---

## 2. PROJECT SUBFOLDER STRUCTURE & WORKSPACE INITIALIZATION

All working files, inputs, interim outputs, and final deliverables are organized under the dedicated subfolder `ChatGPT_Research_Workspace/`.

### A. Subfolder Hierarchy Specification
```
c:\Dev\Glass3DPrinting/
├── ChatGPT_Research_Instructuctions_20260926.md
├── ChatGPT_Reserach_Settings.yaml             <-- OPTIONAL; only if supplied
└── ChatGPT_Research_Workspace/                           <-- DEDICATED PROJECT SUBFOLDER (ALL RESULTS & WORKING FILES)
    ├── artifacts/                                <-- Execution tracking & audit artifacts
    │   ├── IMPLEMENTATION_PLAN.md                <-- Step-by-step roadmap & status
    │   ├── TASK_LIST.md                          <-- Real-time task tracking board
    │   ├── MANIFEST.json                         <-- Machine-readable asset & source ledger
    │   └── VERIFICATION_WALKTHROUGH.md           <-- Final verification and audit logs
    ├── sources/                                  <-- External harvested source materials
    │   ├── papers/                               <-- Downloaded academic PDFs (YYYY_Author_ShortTitle.pdf)
    │   ├── patents/                              <-- Downloaded patent PDFs & specifications
    │   ├── media/                                <-- Schematics, photos, process diagrams, video logs
    │   └── data/                                 <-- Scraped raw records, BibTeX dumps, API JSON/CSVs
    ├── notes/                                    <-- Interim synthesis, extraction notes & working drafts
    │   ├── academic_notes/                       <-- Summaries of papers, mathematical derivations, VFT fits
    │   ├── commercial_notes/                     <-- Market teardowns, company profiles, CapEx/OpEx tables
    │   └── summaries/                            <-- Cross-cutting thematic syntheses
    ├── scripts/                                  <-- Automation, harvesting & analysis scripts
    │   ├── analysis/                             <-- Reproducible physical models and plots
    │   ├── scrapers/                             <-- Literature and media retrieval scripts
    │   ├── processors/                           <-- BibTeX normalizers, image processors
    │   └── tmp/                                  <-- Isolated scratch directory for temp processing (quarantined)
    ├── latex/                                    <-- Modular LaTeX monograph authoring tree
    │   ├── main.tex                              <-- Master document root
    │   ├── references.bib                        <-- Formatted and verified bibliographic entries
    │   ├── sections/                             <-- Modular section chapters (01_... to 08_...)
    │   ├── figures/                              <-- High-resolution production figures for \includegraphics
    │   └── build/                                <-- Isolated LaTeX auxiliary compilation directory (.aux, .log)
    └── output/                                   <-- Final consolidated deliverables
        ├── glass_3d_printing_sota_monograph.pdf  <-- Compiled publication-grade PDF deliverable
        ├── glass_3d_printing_report.zip          <-- Bundled sources and deliverables
        ├── executive_summary.md                  <-- Executive summary & key findings overview
        └── master_source_index.csv               <-- Catalog of all harvested literature & assets
```

### B. Workspace Initialization

Before initiating research queries, downloads, calculations, or agent dispatches, create the complete workspace tree. Inspect existing contents first and preserve prior work.

**Windows / PowerShell (local Codex session):**
```powershell
$researchRoot = 'C:\Dev\Glass3DPrinting\ChatGPT_Research_Workspace'
$subdirectories = @(
    'artifacts', 'sources/papers', 'sources/patents', 'sources/media', 'sources/data',
    'notes/academic_notes', 'notes/commercial_notes', 'notes/summaries',
    'scripts/analysis', 'scripts/scrapers', 'scripts/processors', 'scripts/tmp',
    'latex/sections', 'latex/figures', 'latex/build', 'output'
)
New-Item -ItemType Directory -Force -Path $researchRoot | Out-Null
foreach ($subdirectory in $subdirectories) {
    New-Item -ItemType Directory -Force -Path (Join-Path $researchRoot $subdirectory) | Out-Null
}
Set-Location -LiteralPath $researchRoot
$env:TEMP = Join-Path $researchRoot 'scripts/tmp'
$env:TMP = $env:TEMP
```

**Python (ChatGPT data analysis or another Python execution environment):**
Run this from the environment's permitted working directory. For local use, set `research_root` to the absolute Windows workspace path above.
```python
from pathlib import Path
import os
import tempfile

research_root = (Path.cwd() / "ChatGPT_Research_Workspace").resolve()
subdirectories = [
    "artifacts", "sources/papers", "sources/patents", "sources/media", "sources/data",
    "notes/academic_notes", "notes/commercial_notes", "notes/summaries",
    "scripts/analysis", "scripts/scrapers", "scripts/processors", "scripts/tmp",
    "latex/sections", "latex/figures", "latex/build", "output",
]
for subdirectory in subdirectories:
    (research_root / subdirectory).mkdir(parents=True, exist_ok=True)
os.chdir(research_root)
scratch = str(research_root / "scripts/tmp")
for variable in ("TMPDIR", "TEMP", "TMP"):
    os.environ[variable] = scratch
tempfile.tempdir = scratch
```

Configure writable tool caches and compiler/package scratch directories inside `ChatGPT_Research_Workspace/scripts/tmp/` when supported. Keep all generated project files inside the workspace.

### C. Containment & Path Resolution Rules
1. **Working Directory Anchoring:** Always execute terminal commands and scripts with the working directory set to `ChatGPT_Research_Workspace/` or its subdirectories.
2. **Absolute / Relative Path Discipline:** Resolve output paths against the workspace root and verify that they remain inside it. Do not write to a parent outside the workspace or to the default system temporary directory. If temporary scratch files are needed for scraping, downloading, or parsing, store them exclusively in `ChatGPT_Research_Workspace/scripts/tmp/`.
3. **Automated Subfolder Verification:** Before any subtask completes, check that no stray files were generated in the parent project directory.

### D. Required Research Artifacts
Maintain and update these artifacts within `ChatGPT_Research_Workspace/artifacts/` throughout execution for verifiable tracking:
1. `ChatGPT_Research_Workspace/artifacts/IMPLEMENTATION_PLAN.md`: Detailed stage-by-stage execution roadmap.
2. `ChatGPT_Research_Workspace/artifacts/TASK_LIST.md`: Real-time task tracker (Pending, In-Progress, Verified).
3. `ChatGPT_Research_Workspace/artifacts/MANIFEST.json`: Machine-readable metadata log for every acquired PDF, image, video link, and citation.
4. `ChatGPT_Research_Workspace/artifacts/VERIFICATION_WALKTHROUGH.md`: Final build audit documenting LaTeX compilation success, image resolution checks, BibTeX consistency, directory containment check, and external link validation.

---

## 3. COORDINATED RESEARCH WORKSTREAMS

Organize the research into the four workstreams below. If the current ChatGPT/Codex environment exposes subagent tools, delegate independent work within the available concurrency limit. Otherwise execute the same workstreams sequentially, overlapping independent tool operations where supported.

Assign separate output files to concurrent workers. The coordinating agent owns integration of `references.bib`, `MANIFEST.json`, the task tracker, and final compilation; workers should return proposed additions or write separate fragments to avoid overwriting shared files. Every worker must keep all outputs inside `ChatGPT_Research_Workspace/`.

### Subtask 1: Academic Literature & Mathematical Modeling Agent
- **Target Databases:** OpenAlex, arXiv, Semantic Scholar, ScienceDirect, SpringerLink, IEEE Xplore.
- **Search Focus:**
  - Direct molten glass extrusion physics (crucible design, nozzle geometries, platinum/rhodium alloys, alumina nozzles).
  - Rheology and thermodynamics: Vogel-Fulcher-Tammann (VFT) viscosity models:
    $$\log_{10}\eta = A + \frac{B}{T - T_0}$$
  - Thermal shock mechanics, in-situ annealing lehrs, polarimetric photoelastic stress analysis, and devitrification kinetics (liquidus temperature thresholds).
- **Core Groups to Map:**
  - MIT Mediated Matter Lab (Neri Oxman, John Klein, et al. — G3DP, G3DP2).
  - TU Delft (Glass & Translucent Structures Lab — Telesilla Bristogianni, Faidra Oikonomopoulou).
  - Lawrence Livermore National Laboratory (glass additive manufacturing and optical components; distinguish molten deposition from ink-based routes and subsequent densification).
  - Fraunhofer Institutes (IKTS, ISC, IPT).
  - KTH Royal Institute of Technology & Research Institutes of Sweden (RISE).
  - Laval University, McGill University, and Nagaoka University of Technology.
- **Reproducible Modeling:** Save calculation scripts in `ChatGPT_Research_Workspace/scripts/analysis/`, including `plot_viscosity.py`. Record the glass composition, source of fitted parameters, temperature units, viscosity units, and validity range. Generate `latex/figures/viscosity_vft.png` and `latex/figures/viscosity_vft.pdf`; label fitted or extrapolated curves and do not invent missing coefficients.
- **Output Storage Locations:**
  - Working synthesis and paper notes: `ChatGPT_Research_Workspace/notes/academic_notes/`
  - Normalized BibTeX entries: `ChatGPT_Research_Workspace/latex/references.bib`
  - Raw bibliographic search dumps (JSON/BibTeX): `ChatGPT_Research_Workspace/sources/data/`

### Subtask 2: Commercial Landscape & Industrial Spin-offs Agent
- **Target Sources:** Web searches, SEC/Crunchbase archives, trade publications, patent registries.
- **Investigation Targets:**
  - Commercial printer makers (e.g., Maple Glass Printing and artisan/industrial hybrid platforms); verify current machine names, availability, and specifications from primary sources.
  - University spin-offs and startup initiatives: founding teams, IP portfolios, funding stages, machine unit costs.
  - Market verticals: Architectural structural glass, bespoke optical components/lenses, microfluidics, hermetic chemical vessels, radioactive waste vitrification containers, and luxury packaging.
  - Capex/Opex comparisons: Direct molten extrusion vs. conventional glass blowing/casting vs. post-sintered indirect AM (e.g., Glassomer).
- **Output Storage Locations:**
  - Competitive matrices and market notes: `ChatGPT_Research_Workspace/notes/commercial_notes/`
  - Commercial data tables (CSV/Markdown): `ChatGPT_Research_Workspace/sources/data/`
  - Synthesized chapter section: `ChatGPT_Research_Workspace/latex/sections/07_commercial_systems_market_economics.tex`

### Subtask 3: Asset Acquisition & Browser Harvesting Agent
- Use available web search/browser tools and, where execution is supported, download tools such as PowerShell `Invoke-WebRequest`, `curl`, or Python `requests` / `playwright`:
  1. **Papers:** Programmatically download open-access PDFs to `ChatGPT_Research_Workspace/sources/papers/` (naming: `YYYY_Author_ShortTitle.pdf`).
  2. **Patents:** Download patent PDFs (MIT G3DP patents, Maple Glass filings) to `ChatGPT_Research_Workspace/sources/patents/`.
  3. **High-Res Media:** Capture machine schematics, nozzle cross-sections, thermal imaging frames, and macroscopic print photos; save raw downloads to `ChatGPT_Research_Workspace/sources/media/` and clean production-ready figures into `ChatGPT_Research_Workspace/latex/figures/`.
  4. **Video Demonstrations:** Log direct, verified streaming URLs (YouTube, Vimeo, lab repositories) for MIT G3DP/G3DP2, Maple Glass runs, and polarized light stress tests in `ChatGPT_Research_Workspace/artifacts/MANIFEST.json`.
  5. **Harvesting Scripts & Scratch Data:** Store all downloader scripts in `ChatGPT_Research_Workspace/scripts/scrapers/` and temporary download buffers in `ChatGPT_Research_Workspace/scripts/tmp/`. Never write temp downloads to the root.

### Subtask 4: LaTeX Monograph & Verification Agent
- Generate a comprehensive, 8-section monograph with modular `.tex` architecture and validated BibTeX entries in `ChatGPT_Research_Workspace/latex/`.
- Compile the document cleanly with auxiliary files directed into `ChatGPT_Research_Workspace/latex/build/`.
- Copy the final validated PDF to `ChatGPT_Research_Workspace/output/glass_3d_printing_sota_monograph.pdf`.

---

## 4. DELIVERABLE SPECIFICATION: MODULAR LATEX MONOGRAPH

### Subfolder Architecture for LaTeX Project
```
ChatGPT_Research_Workspace/latex/
├── main.tex
├── references.bib
├── sections/
│   ├── 01_introduction_taxonomy.tex
│   ├── 02_rheology_thermal_materials_physics.tex
│   ├── 03_nozzle_mechanics_hardware_kinematics.tex
│   ├── 04_in_situ_thermal_management_annealing.tex
│   ├── 05_defect_mechanisms_optical_quality.tex
│   ├── 06_academic_landscape_directory.tex
│   ├── 07_commercial_systems_market_economics.tex
│   └── 08_open_frontiers_research_roadmap.tex
├── figures/
│   └── (All figures referenced by \includegraphics)
└── build/
    └── (All auxiliary compiler files: .aux, .log, .out, .toc, .fls, .fdb_latexmk)
```

### Formatting & Quality Standards
- **Style:** Two-column IEEE / ACM format or comprehensive single-column Springer/Nature report format using `booktabs`, `amsmath`, `hyperref`, `siunitx`, `tabularx`, and `subcaption`.
- **Mathematical Formulations:** Must include explicit expressions for:
  - Temperature-dependent viscosity (VFT formulation) across fused silica, borosilicate, and soda-lime.
  - Rayleigh-Plateau instability and gravitational slumping parameters for liquid glass cords.
  - Cooling gradient and transient heat transfer equations.
- **Embedded Comparative Tables:**
  - *Table 1:* Direct Molten Glass Extrusion vs. Powder Bed Fusion (SLS/SLM) vs. Photopolymer Resin Sintering (SLA/Glassomer). Include temperatures (°C), build envelope, deposition rate ($g/min$ or $cm^3/h$), optical transmittance ($T\%$), surface roughness ($Ra$), and relative tensile strength.
  - *Table 2:* Global Academic Research Groups Directory (Lab, Institution, PI, Apparatus Name, Key Findings, Primary DOI).
  - *Table 3:* Commercial & Industrial Landscape (Company/Entity, Machine Name, Extrusion Temp Max, Feedstock Type, Target Market, Maturity/TRL).
- **Evidence and Bibliography:** Use verified primary sources and valid BibTeX entries. Include author, title, year, DOI/URL, and journal/conference, volume, pages, and publisher where applicable. Distinguish measured results from manufacturer claims, model predictions, and proposed applications. Mark unavailable values as not reported; do not fabricate prices, TRLs, machine names, or performance data.
- **Units and Comparability:** State whether viscosity is in Pa·s or dPa·s, and use consistent temperature units in VFT fits. Document the assumptions behind instability formulas and heat-transfer models. In comparison tables, distinguish printing temperatures from sintering temperatures and attach test conditions to optical and strength measurements.
- **Direct Hyperlinks:** Include working hyperlinks (`\href{...}{...}`) to video recordings of live prints, lab demos, and open patent registries.

---

## 5. EXECUTION & VERIFICATION PROTOCOL

1. **Pre-Execution Subfolder Initialization:**
   Execute directory setup commands. Confirm that `ChatGPT_Research_Workspace/` and all specified child directories are created before initiating any downloads or agent dispatches.

2. **Plan & Document:**
   Generate `ChatGPT_Research_Workspace/artifacts/IMPLEMENTATION_PLAN.md` and outline every intended step, specifying exact file paths inside `ChatGPT_Research_Workspace/`.

3. **Execute Workstreams with Directory Containment:**
   Where supported, run independent acquisition of papers and figures alongside drafting technical sections in `ChatGPT_Research_Workspace/latex/sections/`. Ensure all scripts, scrapers, and intermediate data files are saved exclusively within `ChatGPT_Research_Workspace/scripts/` or `ChatGPT_Research_Workspace/notes/`.

4. **Validate Assets:**
   Ensure every `\includegraphics` target exists in `ChatGPT_Research_Workspace/latex/figures/` and verify that every citation in `ChatGPT_Research_Workspace/latex/references.bib` has complete author, title, journal/conference, year, and DOI/URL metadata.

5. **Isolated Compilation & Packaging:**
   Use an available LaTeX compiler and route all auxiliary output to `ChatGPT_Research_Workspace/latex/build/`. From a local PowerShell session:
   ```powershell
   $researchRoot = 'C:\Dev\Glass3DPrinting\ChatGPT_Research_Workspace'
   Set-Location -LiteralPath (Join-Path $researchRoot 'latex')
   latexmk -pdf -outdir=build -halt-on-error main.tex
   if ($LASTEXITCODE -ne 0) { throw 'LaTeX compilation failed; inspect latex/build logs.' }
   Copy-Item -LiteralPath (Join-Path $researchRoot 'latex/build/main.pdf') -Destination (Join-Path $researchRoot 'output/glass_3d_printing_sota_monograph.pdf')
   ```
   In a hosted environment, use equivalent commands with its actual workspace path. If compilation is unavailable, deliver the complete LaTeX source and explicitly record that a compiled PDF is still outstanding.

   After validation, create `ChatGPT_Research_Workspace/output/glass_3d_printing_report.zip` containing the LaTeX sources, bibliography, figures, research sources, notes, scripts, tracking artifacts, executive summary, source index, and final PDF when available. Exclude the ZIP itself, disposable caches, local virtual environments, and tool binaries. Use workspace-root-relative archive paths so the bundle is portable.

6. **Post-Execution Directory Containment Audit:**
   Execute a root-level audit to verify zero pollution in the project root:
   - Compare the project root against its pre-execution inventory; confirm that this research run added no files outside `ChatGPT_Research_Workspace/`. Preserve unrelated existing files and workspaces.
   - Confirm 100% of generated files, downloaded papers, figures, notes, scripts, and logs reside inside `ChatGPT_Research_Workspace/`.

7. **Final Artifact:**
   Produce `ChatGPT_Research_Workspace/artifacts/VERIFICATION_WALKTHROUGH.md` documenting:
   - Actual compiler result, unresolved warnings/citations, and PDF inspection results; record any unavailable checks.
   - Asset resolution and file integrity tallies.
   - Comprehensive inventory of all acquired papers, patents, and media in `ChatGPT_Research_Workspace/`.
   - Containment audit confirmation verifying the project root was unpolluted.

8. **Final Delivery:**
   Link the final PDF, ZIP, executive summary, and source index using local file links in Codex or downloadable artifact links in ChatGPT. State material evidence gaps and any unfinished requirements accurately.
