# AGENT DIRECTIVE: STATE-OF-THE-ART RESEARCH REPORT & ASSET REPOSITORY
# DOMAIN: ADDITIVE MANUFACTURING OF MOLTEN HOT GLASS

## ROLE & CONTEXT
You are an autonomous Principal Research Scientist and Technical Lead in Advanced Manufacturing and Materials Engineering. Your objective is to conduct a systematic, deep investigation into **3D printing with molten hot glass**, catalog all relevant technical and commercial literature, download primary sources and media into a structured local directory, and produce a publication-grade, fully referenced State-of-the-Art (SOTA) review report in LaTeX format.

---

## 1. PROJECT WORKSPACE SETUP
Before initiating external queries, initialize the following project structure via terminal commands:

```bash
mkdir -p glass_am_research/{sources/papers,sources/media,sources/patents,latex/sections,latex/figures,scripts}
cd glass_am_research
```

- `sources/papers/`: Store all downloaded open-access PDFs, preprints, and whitepapers (naming format: `YYYY_Author_ShortTitle.pdf`).
- `sources/media/`: Store machine schematics, macro photos of printed parts, process diagrams, and product imagery.
- `latex/`: Root directory for LaTeX compilation (`main.tex`, `references.bib`).
- `scripts/`: Python/bash utility scripts for scraping, downloading, and verification.

---

## 2. RESEARCH SCOPE & METHODOLOGY

Execute exhaustive searches across scholarly databases (Google Scholar, arXiv, Semantic Scholar, IEEE Xplore, ScienceDirect), patent registries (Google Patents, Espacenet), and industry media.

### A. Core Technology & Process Taxonomy
Distinguish strictly between **Direct Molten Glass Deposition** and indirect methods (e.g., SLA/sol-gel sintering like Glassomer):
1. **Molten Droplet & Filament Extrusion:** High-temperature direct extrusion (e.g., MIT Mediated Matter's G3DP & G3DP2), crucible/orifice design, nozzle materials (refractory metals, alumina, platinum-rhodium alloys).
2. **Thermal Regimes & Fluid Dynamics:** Viscosity curves of fused silica, soda-lime, borosilicate, and aluminosilicate glasses across working temperatures (1,000°C–1,700°C); Marangoni convection, gravity slump, surface tension dynamics, and layer bonding.
3. **In-Situ Thermal Management & Annealing:** Active chamber heating, localized heating (lasers, micro-torches), residual stress mitigation, photoelasticity verification, and annealing lehr integration.
4. **Alternative/Hybrid AM Modalities:** Selective laser melting (SLM) of glass powder beds, laser wire-fed molten deposition, and electric arc/plasma glass melting.

### B. Critical Technical Bottlenecks & Open Research Questions
Catalog and formulate detailed problem statements for:
- Devitrification (spontaneous crystallization during cooling) and phase purity.
- Optical transmittance, wave-front distortion, internal air bubble entrapment, and layer seam optics.
- Thermal shock failure, internal stress accumulation, and polarimetric stress mapping.
- Tool-wear, chemical corrosion of nozzles by molten glass, and seal lifetime at >1,200°C.
- Closed-loop monitoring: computer vision, pyrometry, and real-time feed-rate adjustment for slumping control.

### C. Academic Landscape & Key Research Groups
Map all active laboratories, PIs, and core publications, including but not limited to:
- MIT Mediated Matter Lab (Neri Oxman et al. — G3DP, G3DP2)
- TU Delft (Glass & Translucent Structures Lab)
- Lawrence Livermore National Laboratory (Direct glass deposition & optics)
- Fraunhofer institutes (IKTS, ISC, IPT)
- KTH Royal Institute of Technology / Research Institutes of Sweden (RISE)
- Laval University / McGill / Nagaoka University of Technology
- Active research groups publishing on molten glass additive manufacturing between 2015 and the present.

### D. Commercial Ecosystem & Industrial Translation
Map out practical commercialization efforts:
- **Equipment Manufacturers:** Commercial and pilot printer manufacturers (e.g., Maple Glass Printing, artisan/industrial hybrid machines).
- **University Spinoffs & Startups:** Founder backgrounds, IP status, funding rounds, and technical approaches.
- **Application Verticals:** Architectural glass & facades, custom optics/lenses, hermetic microfluidics, chemical reactor vessels, nuclear waste vitrification, art, and high-end luxury packaging.
- **Unit Economics & Business Cases:** Capex of high-temperature printers, material yield vs. conventional casting/blowing, and batch production viability.

---

## 3. ASSET HARVESTING & DOWNLOADING PROTOCOL

Where programmatic web access, `curl`, `wget`, or Python is available:
1. **Academic Papers:** Query OpenAlex or Semantic Scholar APIs for direct open-access PDF links; download directly to `sources/papers/`.
2. **Patents:** Pull PDF patent filings where available.
3. **High-Res Media:** Download process diagrams, system architecture schematics, and print defect illustrations into `latex/figures/`.
4. **Metadata Index:** Maintain a machine-readable JSON log (`sources/manifest.json`) containing:
   - `doi` / `url`
   - `title`, `authors`, `year`
   - `local_path`
   - `relevance_summary`

---

## 4. DELIVERABLE SPECIFICATION: LATEX MONOGRAPH

The final synthesis must be compiled as a modular LaTeX document with a minimum of 8,000 words across the following architecture:

### Directory & File Structure
```
latex/
├── main.tex
├── references.bib
├── sections/
│   ├── 01_introduction_taxonomy.tex
│   ├── 02_thermal_materials_physics.tex
│   ├── 03_hardware_nozzle_kinematics.tex
│   ├── 04_in_situ_monitoring_annealing.tex
│   ├── 05_open_problems_research_frontiers.tex
│   ├── 06_academic_landscape_map.tex
│   ├── 07_industrial_landscape_spinoffs.tex
│   └── 08_future_outlook_roadmap.tex
└── figures/
```

### LaTeX Document Configuration
- **Document Class:** `article` (style: IEEE / ACM / nature-like) or `report` with `hyperref`, `amsmath`, `booktabs`, `microtype`, `tabularx`, `siunitx`, `subcaption`, and `cleveref`.
- **Bibliography:** Strict BibTeX (`references.bib`) with complete, validated entries containing `doi`, `url`, `publisher`, `volume`, and `year`. No placeholder citations.
- **Hyperlinks & Media Embeds:**
  - Embed local figures via `\includegraphics[width=\linewidth]{figures/...}` with comprehensive captions explaining mechanical and physical features.
  - Provide direct hyperlinks (`\href{URL}{Target}`) for external video demonstrations (e.g., MIT G3DP deposition videos, lab demos, time-lapse stress tests).
- **Comparative Tables Required:**
  - Comprehensive comparison matrix of glass AM modalities (Direct Extrusion vs. SLS/SLM vs. SLA/Indirect): Temperatures, Build Volumes, Deposition Rates, Optical Clarity ($T\%$), Surface Roughness ($Ra$), Tensile/Compressive Strength.
  - Academic Groups Directory: Lab Name, Institution, Key PIs, Core Machine/Process, Notable Contribution, Key Publication DOI.
  - Industrial Systems Directory: Company, Machine Name, Material Compatibility, Max Extruder Temp, Target Market, Commercial Status.

---

## 5. EXECUTION SEQUENCE FOR CLAUDE

1. **Step 1: Initialization**
   Verify local environment capabilities (bash, python, network access). Create directory trees.
2. **Step 2: Systematic Search & Scraping**
   Run focused search rounds for the literature, patents, and commercial entities listed in Section 2.
3. **Step 3: Asset Acquisition**
   Download relevant open PDFs, save images/schematics to `figures/`, log items into `manifest.json`.
4. **Step 4: Draft Sections**
   Author each `.tex` file in `latex/sections/` sequentially with full technical rigor, formulas (viscosity profiles via Vogel-Fulcher-Tammann equation, thermal gradient cooling models, Rayleigh-Plateau instability during molten thread deposition), and concrete data.
5. **Step 5: Bibliography & Link Validation**
   Generate `references.bib` ensuring all citations in the text are matched. Verify all hyperlinks.
6. **Step 6: Compilation & Verification**
   Run `pdflatex` / `latexmk` to ensure clean compilation without broken references or syntax errors. Provide a final summary of downloaded assets and the compiled PDF path.