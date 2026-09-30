# AGENT DIRECTIVE: AUTONOMOUS SOTA MONOGRAPH & ASSET REPOSITORY PIPELINE
# PLATFORM: GOOGLE ANTIGRAVITY (AGENT-FIRST IDE / MANAGER SURFACE)
# TARGET DOMAIN: ADDITIVE MANUFACTURING OF MOLTEN HOT GLASS

---

## 1. AGENT ROLE & OPERATING CONTEXT

You are operating within **Google Antigravity** as an autonomous **Lead Research & Systems Engineering Agent**. Your task is to conduct an end-to-end investigation into **3D printing with molten hot glass**, catalog primary academic and industrial sources, download media and papers directly to the designated project subfolder, and author a publication-grade, fully compiled LaTeX review monograph.

Take full advantage of Antigravity's **Manager Surface**, **Terminal**, **Browser Tools**, and **Artifact Generation** capabilities to execute asynchronous, verifiable workflows.

> [!IMPORTANT]
> **MANDATORY DIRECTORY CONTAINMENT INVARIANT (ZERO ROOT POLLUTION):**
> All research activities, downloaded literature, raw data, media assets, scripts, working notes, intermediate compiler outputs, tracking artifacts, and final monograph deliverables **MUST be strictly contained within a dedicated subfolder of the project** (`./Antigravity_Research_Workspace/`).
> Under **NO circumstances** should any generated files, temporary scripts, logs, downloads, or build artifacts be written directly into the project root directory (`c:\Dev\Glass3DPrinting\`).

---

## 2. PROJECT SUBFOLDER STRUCTURE & WORKSPACE INITIALIZATION

All working files, inputs, interim outputs, and final deliverables are organized under the dedicated subfolder `Antigravity_Research_Workspace/`.

### A. Subfolder Hierarchy Specification
```
c:\Dev\Glass3DPrinting/
├── Antigravity_Research_Instructuctions_20260926.md
├── Antigravity_Reserach_Settings.yaml
└── Antigravity_Antigravity_Research_Workspace/                           <-- DEDICATED PROJECT SUBFOLDER (ALL RESULTS & WORKING FILES)
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
        ├── executive_summary.md                  <-- Executive summary & key findings overview
        └── master_source_index.csv               <-- Catalog of all harvested literature & assets
```

### B. Terminal Environment Setup
Before executing any external query, search, or script, initialize the complete subfolder structure via the terminal:

```bash
# Initialize complete subfolder architecture inside the project
mkdir -p Antigravity_Antigravity_Research_Workspace/{artifacts,sources/papers,sources/patents,sources/media,sources/data,notes/academic_notes,notes/commercial_notes,notes/summaries,scripts/scrapers,scripts/processors,scripts/tmp,latex/sections,latex/figures,latex/build,output}

# Navigate into the subfolder for all subsequent terminal operations
cd Antigravity_Research_Workspace
```

### C. Containment & Path Resolution Rules
1. **Working Directory Anchoring:** Always execute terminal commands and scripts with the working directory set to `Antigravity_Research_Workspace/` or its subdirectories.
2. **Absolute / Relative Path Discipline:** Never reference relative paths that write to `..` or system temp folders (`/tmp` or `%TEMP%`). If temporary scratch files are needed for scraping, downloading, or parsing, store them exclusively in `Antigravity_Research_Workspace/scripts/tmp/`.
3. **Automated Subfolder Verification:** Before any subtask completes, check that no stray files were generated in the parent project directory.

### D. Required Antigravity Artifacts
Maintain and update these artifacts within `Antigravity_Research_Workspace/artifacts/` throughout execution for verifiable tracking:
1. `Antigravity_Research_Workspace/artifacts/IMPLEMENTATION_PLAN.md`: Detailed stage-by-stage execution roadmap.
2. `Antigravity_Research_Workspace/artifacts/TASK_LIST.md`: Real-time task tracker (Pending, In-Progress, Verified).
3. `Antigravity_Research_Workspace/artifacts/MANIFEST.json`: Machine-readable metadata log for every acquired PDF, image, video link, and citation.
4. `Antigravity_Research_Workspace/artifacts/VERIFICATION_WALKTHROUGH.md`: Final build audit documenting LaTeX compilation success, image resolution checks, BibTeX consistency, directory containment check, and external link validation.

---

## 3. MULTI-AGENT SUBTASK DECOMPOSITION (MANAGER SURFACE)

Orchestrate the research across four coordinated subtasks, ensuring each subagent writes its information, raw findings, and outputs strictly into its designated subdirectory within `Antigravity_Research_Workspace/`:

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
  - Lawrence Livermore National Laboratory (Direct glass deposition & optical components).
  - Fraunhofer Institutes (IKTS, ISC, IPT).
  - KTH Royal Institute of Technology & Research Institutes of Sweden (RISE).
  - Laval University, McGill University, and Nagaoka University of Technology.
- **Output Storage Locations:**
  - Working synthesis and paper notes: `Antigravity_Research_Workspace/notes/academic_notes/`
  - Normalized BibTeX entries: `Antigravity_Research_Workspace/latex/references.bib`
  - Raw bibliographic search dumps (JSON/BibTeX): `Antigravity_Research_Workspace/sources/data/`

### Subtask 2: Commercial Landscape & Industrial Spin-offs Agent
- **Target Sources:** Web searches, SEC/Crunchbase archives, trade publications, patent registries.
- **Investigation Targets:**
  - Commercial printer makers (e.g., Maple Glass Printing / V4 printer, artisan/industrial hybrid platforms).
  - University spin-offs and startup initiatives: founding teams, IP portfolios, funding stages, machine unit costs.
  - Market verticals: Architectural structural glass, bespoke optical components/lenses, microfluidics, hermetic chemical vessels, radioactive waste vitrification containers, and luxury packaging.
  - Capex/Opex comparisons: Direct molten extrusion vs. conventional glass blowing/casting vs. post-sintered indirect AM (e.g., Glassomer).
- **Output Storage Locations:**
  - Competitive matrices and market notes: `Antigravity_Research_Workspace/notes/commercial_notes/`
  - Commercial data tables (CSV/Markdown): `Antigravity_Research_Workspace/sources/data/`
  - Synthesized chapter section: `Antigravity_Research_Workspace/latex/sections/07_commercial_systems_market_economics.tex`

### Subtask 3: Asset Acquisition & Browser Harvesting Agent
- Use Antigravity's integrated browser and terminal scraping tools (`curl`, `wget`, Python `requests` / `playwright`):
  1. **Papers:** Programmatically download open-access PDFs to `Antigravity_Research_Workspace/sources/papers/` (naming: `YYYY_Author_ShortTitle.pdf`).
  2. **Patents:** Download patent PDFs (MIT G3DP patents, Maple Glass filings) to `Antigravity_Research_Workspace/sources/patents/`.
  3. **High-Res Media:** Capture machine schematics, nozzle cross-sections, thermal imaging frames, and macroscopic print photos; save raw downloads to `Antigravity_Research_Workspace/sources/media/` and clean production-ready figures into `Antigravity_Research_Workspace/latex/figures/`.
  4. **Video Demonstrations:** Log direct, verified streaming URLs (YouTube, Vimeo, lab repositories) for MIT G3DP/G3DP2, Maple Glass runs, and polarized light stress tests in `Antigravity_Research_Workspace/artifacts/MANIFEST.json`.
  5. **Harvesting Scripts & Scratch Data:** Store all downloader scripts in `Antigravity_Research_Workspace/scripts/scrapers/` and temporary download buffers in `Antigravity_Research_Workspace/scripts/tmp/`. Never write temp downloads to the root.

### Subtask 4: LaTeX Monograph & Verification Agent
- Generate a comprehensive, 8-section monograph with modular `.tex` architecture and validated BibTeX entries in `Antigravity_Research_Workspace/latex/`.
- Compile the document cleanly with auxiliary files directed into `Antigravity_Research_Workspace/latex/build/`.
- Copy the final validated PDF to `Antigravity_Research_Workspace/output/glass_3d_printing_sota_monograph.pdf`.

---

## 4. DELIVERABLE SPECIFICATION: MODULAR LATEX MONOGRAPH

### Subfolder Architecture for LaTeX Project
```
Antigravity_Research_Workspace/latex/
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
- **Direct Hyperlinks:** Include working hyperlinks (`\href{...}{...}`) to video recordings of live prints, lab demos, and open patent registries.

---

## 5. EXECUTION & VERIFICATION PROTOCOL

1. **Pre-Execution Subfolder Initialization:**
   Execute directory setup commands. Confirm that `Antigravity_Research_Workspace/` and all specified child directories are created before initiating any downloads or agent dispatches.

2. **Plan & Document:**
   Generate `Antigravity_Research_Workspace/artifacts/IMPLEMENTATION_PLAN.md` and outline every intended step, specifying exact file paths inside `Antigravity_Research_Workspace/`.

3. **Execute In Parallel with Directory Containment:**
   Run background acquisition of papers and figures while drafting technical sections in `Antigravity_Research_Workspace/latex/sections/`. Ensure all scripts, scrapers, and intermediate data files are saved exclusively within `Antigravity_Research_Workspace/scripts/` or `Antigravity_Research_Workspace/notes/`.

4. **Validate Assets:**
   Ensure every `\includegraphics` target exists in `Antigravity_Research_Workspace/latex/figures/` and verify that every citation in `Antigravity_Research_Workspace/latex/references.bib` has complete author, title, journal/conference, year, and DOI/URL metadata.

5. **Isolated Compilation:**
   Compile the LaTeX monograph with auxiliary output routed to the `build/` folder to prevent directory pollution:
   ```bash
   cd Antigravity_Research_Workspace/latex
   latexmk -pdf -outdir=build -halt-on-error main.tex
   cp build/main.pdf ../output/glass_3d_printing_sota_monograph.pdf
   ```

6. **Post-Execution Directory Containment Audit:**
   Execute a root-level audit to verify zero pollution in the project root:
   - Check that `c:\Dev\Glass3DPrinting\` contains only the root configuration/directive files.
   - Confirm 100% of generated files, downloaded papers, figures, notes, scripts, and logs reside inside `Antigravity_Research_Workspace/`.

7. **Final Artifact:**
   Produce `Antigravity_Research_Workspace/artifacts/VERIFICATION_WALKTHROUGH.md` documenting:
   - Compiler output confirmation and zero-error build verification.
   - Asset resolution and file integrity tallies.
   - Comprehensive inventory of all acquired papers, patents, and media in `Antigravity_Research_Workspace/`.
   - Containment audit confirmation verifying the project root was unpolluted.
