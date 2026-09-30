# Search log — systematic rounds (2026-09-26)

**Created:** 2026-09-26T17:31:40+03:00
**Updated:** 2026-09-29T22:05:15+03:00
**Generator:** Claude Code (Model: Claude Fable 5.1, claude-fable-5-1)

**Original prompt:**
> start over and read Claude_Research_Instructuctions_20260926.md and follow the instructions.

**Context:**
- Log of the search rounds behind the molten-glass additive manufacturing monograph, including negative findings.
- Round I, added on 29 September, covers toolpath optimisation for optical properties and found no direct prior work.

Engines used: web search (Google-indexed scholarly/industry pages), OpenAlex API, Crossref/doi.org content negotiation, Google Patents, USPTO ppubs.

| Round | Query focus | Key hits |
|---|---|---|
| A | MIT G3DP / G3DP2 | Klein 2015 (10.1089/3dp.2015.0021); Inamura 2018 (10.1089/3dp.2018.0157); DSpace OA copies; patents US9919510 / US10464305 / US10266442; Oxman platform page; Vimeo "GLASS" video |
| B | Filament/fiber-fed laser | Luo/Kinzel Missouri S&T 2016-2018 (soda-lime JMSE 2017, fused quartz Opt. Eng. 2018, heat transfer); Hostetler SFF 2018; Notre Dame digital glass forming; LZH Hannover LGD (von Witzendorff 2018 Procedia CIRP 74:272; coaxial LGD SPIE 2021; LGD fibres 2022; homogeneity Procedia CIRP 2024); KTH filament CO2 (Frontiers Mater. 2022); Fröhlich/Ilmenau rod-fed boro/soda-lime 2022 |
| C | Commercial melt extrusion | Maple Glass Printing (Melbourne; Maple 2/3; cane feed; 170x200x300 mm; ~USD 45k; nozzle 900-1000 C; 1.5 mm nozzle); Micron3DP (Israel, 2015; soda-lime 850 C and borosilicate ~1640 C claim; 200 mm cube; 100 um layers); Evenline (Rochester NY; G3DP2/G3DP3; 32.5x32.5x38 cm; recycled bottle glass); Nobula3D (KTH spin-off 2021; DGLD CO2 laser >2000 C, 10 um-0.5 mm resolution) |
| D | Indirect (contrast) | Glassomer (KIT/Freiburg 2018; Kotz Nature 2017; Mader Adv. Sci. 2021); LLNL DIW (Nguyen 2017; Destino 2018; optics); CAL (Toombs Science 2022) |
| E | Powder bed / DED | Fateri & Gebhardt 2015 (93 % density); Khmyrov 2016; Datsiou 2019 JACerS 102:4410 & 2021 Addit. Manuf.; Spirrett 2023 powder-fed DED; Lang 2024 coaxial powder quartz; 2025 JMMP alkali-borosilicate laser |
| F | Monitoring / stress / devitrification / nozzle | RT-Linux thermal-camera control of digital glass forming (Addit. Manuf. 2026); quartz melt-zone temperature control (2025); LGD homogeneity (bubbles, striae); cristobalite devitrification >1100 C; AZS/zirconia refractory corrosion (IJACT 2025); Pt-Rh bushings (Platinum Metals Rev 2010); photoelasticity (Aben) |
| G | Applications / economics | Glass microfluidics (Anal. Methods 2019); microreactors; MIT/Evenline masonry (Glass Struct. Eng. 2024, 3.6-118 MPa); Josh Owen spiral vessels; RIT hosts glass printer; no dedicated glass-AM market-size report found (AM market ~USD 30.6 B 2025; glass manufacturing ~USD 127 B) |
| H | Named groups | TU Delft (Oikonomopoulou, Bristogianni: cast-glass, 3D-printed sand moulds, topology-optimised megaliths — casting-adjacent, not molten deposition); Laval COPL (Messaddeq: chalcogenide FDM 2019; soft-glass preforms 2023); RISE (Stefan Karlsson, glass AM editorial role; AM Application Centre Mölndal); McGill (ADML/P2AM2 — general AM, no molten-glass output found); Nagaoka Univ. Tech. (no molten-glass AM publication surfaced in any query); Fraunhofer IKTS/IPT/ILT (ceramic L-PBF, glass listed as processable material; no molten-glass deposition paper surfaced) |

Negative findings are recorded explicitly so the monograph does not fabricate group activity.

## Supplementary round I (2026-09-29): toolpath optimisation of transparent deposited materials for optical properties

Engines: web search, OpenAlex API (`search=`), Crossref `query.bibliographic`, doi.org BibTeX, CVF/arXiv/npj OA PDFs. Full note: `notes/toolpath_optics_literature.md`; harvest script `scripts/harvest_toolpath_optics.py` (33 DOI works + 3 manual sources added to `sources/manifest.json`, 5 new PDFs).

| Sub-round | Query focus | Key hits |
|---|---|---|
| I-1 | 3D printed glass + caustics / optical design | Klein 2015 + S.M. thesis (caustic projection; striations control light); Inamura 2018 (columns as architectural lenses); Glass II / Inglessis-Oxman 2017 (templating light, reverse-engineering geometry stated as future work); Weber-Reinhart-Oxman 2020 Build. Environ. 180:106957 (Radiance photon mapping benchmarked on printed glass); Kassubeck et al. WACV 2021 (shape-from-caustics for LGD process control, differentiable renderer) |
| I-2 | Toolpath + glass 3D printing | Chhadeh, Nowak, Vlahopoulos, Seel, Birbilis 2026 npj Adv. Manuf. 3:16 (toolpath vs bending strength via heat retention; mechanical only); Sage et al. 2026 Addit. Manuf. 123:105214 (LLNL gradient DIW toolpaths, connected Fermat spirals, for GRIN optics) |
| I-3 | Deposition parameters -> optical elements (laser filament) | Liu 2024 microlens arrays (layers/radius -> focal length); Rettschlag 2020 Procedia CIRP 94:276 (LGD spheres for micro-lenses); Kranert 2020 SPIE 11349 (curved waveguides); Hong 2023 Photonics 10:378 (germanate lenses, fibre-fed); Dylla-Spears 2020 Sci. Adv. (GRIN profile programmed into toolpath) |
| I-4 | FFF/FDM process parameters vs transmittance / haze / birefringence | Kumar 2022 AMPT 10:1093; Kumar 2024 Opt. Laser Technol. 175:110865; Vochozka 2024 Polymers 16:2862; Hamp 2021 Appl. Opt. 60:6573; Quero 2021 Lab Chip 21:3715; Amendola 2021 PLOS ONE (scattering coefficients); Ren 2023 Opt. Mater. 138:113743 (optical anisotropy); Blachowicz 2021 e-Polymers; Rooney 2024 AMT; AnisoTag CHI 2023 (toolpath direction -> reflection anisotropy); reviews Heinrich 2016, Gao 2023 |
| I-5 | Computational caustic / appearance fabrication | Papas 2011; Kiser 2013; Yue 2014; Schwartzburg 2014; Zhou 2025 arXiv 2511.09361; Zhao 2016 lampshades; Willis 2012; Pereira 2014; Dong 2010; Papas 2013; Elek 2017; Brunton 2018; Weyrich 2009; Nagasawa 2023 |
| I-neg | Negative findings | No work optimises a glass (or transparent extrusion) toolpath for an optical target under a fixed global shape; no optical toolpath publication from Evenline / Maple / Nobula / Micron3DP; no follow-up to the Inglessis-Oxman reverse-engineering goal; no controlled-devitrification opacity design in direct deposition |
