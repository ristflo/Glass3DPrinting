# Toolpath optimisation of transparent deposited materials for optical properties — literature note

**Created:** 2026-09-29T22:05:15+03:00
**Updated:** 2026-09-30T12:41:59+03:00
**Generator:** Claude Code (Model: Claude Fable 5.1, claude-fable-5-1)

**Original prompt:**
> research if there is any published research on the optimization the printing toolpath of glas or other transparent exrtuded and deposited materials used in 3d printing to achieve certain optical properties, while maintaining the global shape of the object to be fabricated, to for example achiave high transparentcy or low transparency or certain optical effects like caustics or reflections, etc. add the findings to your resreach in the claude reserach workschop folder and add a paragraph to the list of problemes in the latex file about transparent material 3d printing tool path optimization for optical properties

**Context:**
- Literature note for the Claude monograph on molten-glass 3D printing; it feeds Problem 9 of the open-problems section.
- Finding: no published work optimises a glass or transparent-extrusion toolpath for an optical target under a fixed shape; the adjacent work is catalogued.

Search round I, 2026-09-29. Question: *is there published research that optimises the printing toolpath of
glass (or other transparent extruded / deposited materials) to achieve specified optical properties —
high or low transparency, caustics, reflections, other light effects — while maintaining the global shape
of the object?*

Engines: web search (Google-indexed scholarly and industry pages), OpenAlex API (`search=` full text),
Crossref (`query.bibliographic`), doi.org content negotiation for BibTeX, CVF / arXiv / npj open-access PDFs.
All 33 DOI-bearing works below are resolved in OpenAlex and have BibTeX in `sources/data/bibtex_raw/`;
records are in `sources/manifest.json` (field `search_round = "I …"`). Harvest script:
`scripts/harvest_toolpath_optics.py`.

## 1. Short answer

**No publication was found that treats the toolpath of a molten-glass (or any transparent extrusion) process as
the design variable for a specified optical target while holding the global shape fixed.** The problem is
surrounded on all sides by adjacent work, which is why it is worth stating as an open problem:

| Ingredient | Exists? | Where |
|---|---|---|
| Printed-glass optics documented qualitatively (caustics, "columns as lenses") | yes | Klein 2015, Inamura 2018, Brun 2017, Glass II (Inglessis/Oxman 2017) |
| Forward light simulation of printed glass validated by measurement | yes | Weber, Reinhart, Oxman 2020 (Radiance photon mapping) |
| Inverse problem: *shape from caustic* for printed glass (process feedback) | yes | Kassubeck et al., WACV 2021 |
| Inverse problem: *caustic from shape* (computational caustic design) | yes, but for milled/polished surfaces | Papas 2011, Kiser 2013, Yue 2014, Schwartzburg 2014, Zhou 2025 |
| Toolpath optimisation for glass extrusion | yes, but for **strength**, not optics | Chhadeh, Nowak, Vlahopoulos, Seel, Birbilis 2026 |
| Deposition parameters as optical design variables (laser filament routes) | yes, per element (lens, waveguide) | Liu 2024 microlens arrays, Rettschlag 2020, Kranert 2020, Hong 2023 |
| Toolpath encodes an optical property field (composition → refractive index) | yes, indirect DIW route | Dylla-Spears 2020, Destino 2018, Sage 2026 (gradient toolpaths) |
| Process parameters vs transmittance / haze / birefringence, extrusion polymers | yes (scalar objective, DOE style) | Kumar 2022/2024, Vochozka 2024, Hamp 2021, Quero 2021, Amendola 2021, Ren 2023 |
| Toolpath direction → reflection anisotropy (FDM) | yes | AnisoTag, CHI 2023 |
| Volumetric appearance / translucency fabrication (multi-material inkjet) | yes | Dong 2010, Papas 2013, Elek 2017, Brunton 2018, Nagasawa 2023 |
| Light routing / printed optics inside printed objects | yes | Willis 2012, Pereira 2014 |
| **Toolpath ↔ optical target ↔ fixed global shape, for glass or transparent extrusion** | **no** | — |

## 2. Findings by cluster

### 2.1 Molten / laser-deposited glass (direct routes)

- **Klein et al. 2015** (`klein2015`, 3D Print. Addit. Manuf. 2:92) and **Klein's S.M. thesis** (`klein2015thesis`,
  hdl 1721.1/101831). Caustic patterns were created by projecting light through G3DP prints; the thesis notes
  that the print texture (striations and bulges) offers "a high degree of control over the reflection,
  redirection and shading of light". Control is asserted, not designed or optimised.
- **Inamura et al. 2018** (`inamura2018`). G3DP2 columns "act as architecturally scaled lenses"; the geometric
  and optical variation "can drive, limit or control light transmission, reflection and refraction". The
  column geometry was designed for structure (branching lobes, topology optimisation under the viscoelastic
  filament constraints); the caustics were an outcome, animated by a travelling internal light.
- **Glass 2.0 / Glass II, Inglessis & Oxman 2016–17** (`inglessis2017glass2`, project page, not peer-reviewed).
  "Double-sided lenticular surfaces unique to this fabrication process" template light; the explicitly stated
  *future* goal was to "reverse-engineer geometry based on designed light patterns" for solar-transmittance
  control. No follow-up publication found.
- **Brun et al. 2017** (`brun2017`, Phil. Trans. R. Soc. A). The molten-glass "sewing machine": the coiling /
  meander / translated-coil patterns selected by the ratio of travel speed to extrusion speed are a
  catalogue of periodic surface reliefs that could be used as programmable optical texture. Not exploited
  optically in the paper.
- **Weber, Reinhart & Oxman 2020** (`weber2020photon`, Build. Environ. 180:106957). Photon mapping in
  Radiance for geometrically complex glass; 3D-printed transparent glass components used to benchmark
  simulation against measurement. This is the *forward* model needed for any optical toolpath optimisation.
- **Kassubeck, Bürgel, Castillo, Stiller & Magnor 2021** (`kassubeck2021caustics`, WACV 2021, pp. 2877–2886).
  Differentiable multi-spectral caustic renderer plus sparsity regularisation using the *known deposited
  glass volume* to reconstruct printed-glass shape from its caustic image. Explicitly motivated by LGD
  (laser glass deposition) process control, where surface shape depends non-linearly on process parameters
  and in-situ shape measurement does not exist. The authors contrast their goal with caustic *design*
  ("caustic design usually asks to find a producible, low-curvature shape; we measure the caustic to
  reconstruct the real shape"). Code released. This supplies the differentiable optics half of the missing
  problem and is also the most concrete proposal for optical *geometric feedback* (cf. Problem 5).
- **Chhadeh, Nowak, Vlahopoulos, Seel & Birbilis 2026** (`chhadeh2026toolpath`, npj Adv. Manuf. 3:16).
  Rod-fed FDM-type soda-lime glass (TU Darmstadt / Deakin University); four-point bending shows layer orientation and
  toolpath control strength, and "toolpath optimisation can improve strength by controlling heat retention
  during deposition". The only paper found that optimises a *glass* toolpath — objective is mechanical.
  Same heat-retention mechanism governs seam healing and hence optical relief, so the study is the natural
  template for an optical counterpart.
- **Liu, Oriekhov, Lee, Harvey & Fokine 2024** (`kth2024microlens`, already in corpus). Nobula filament
  printer: focal length of each microlens set by number of printed layers and radius — deposition parameters
  *are* the optical design variables, but per lens, not for a shaped object.
- **Rettschlag et al. 2020** (`rettschlag2020microlens`, Procedia CIRP 94:276) — LGD deposition of
  400 µm fused-silica fibre spheres for planar micro-lens matrices; **Kranert et al. 2020**
  (`kranert2020waveguide`, SPIE 11349) — curved, nearly stress-free waveguides where the deposition path
  is the light path; **Hong et al. 2023** (`hong2023germanate`, Photonics 10:378) — fibre-fed laser printing
  of mm–cm germanate spherical and aspherical lenses with temperature feedback. All: deposition strategy ⇒
  optical surface, single-element scale.

### 2.2 Indirect glass routes where the toolpath encodes an optical field

- **Dylla-Spears et al. 2020** (`dyllaspears2020grin`, Sci. Adv. 6:eabc7429) and **Destino et al. 2018**
  (`destino2018`): DIW with inline micromixing of silica/silica-titania inks; the refractive-index profile
  is "programmed into the toolpath" through relative flow rates. Δn up to 0.008, T > 74 %.
- **Sage et al. 2026** (`sage2026fermat`, Addit. Manuf. 123:105214, LLNL): parametric gradient multimaterial
  toolpath generator (connected Fermat spirals, image-driven composition, velocity compensation from local
  curvature, Euclidean distance filter) explicitly for graded optics such as GRIN glass. The closest existing
  "optical toolpath optimisation", but the variable is composition, not cord geometry, and the part is
  sintered and polished afterwards.

### 2.3 Transparent polymer extrusion (FFF/FDM) — quantified parameter → optics relations

- **Kumar & Kumar 2022** (`kumar2022transparency`, Adv. Mater. Process. Technol. 10:1093): layer height,
  temperature, raster angle, build orientation, road width, speed vs UV-Vis transmittance of PLA.
- **Kumar & Kumar 2024** (`kumar2024transparency`, Opt. Laser Technol. 175:110865): multi-response
  optimisation of transmittance *and* spatial resolution over layer height, road width, deposition speed.
- **Vochozka et al. 2024** (`vochozka2024translucency`, Polymers 16:2862): orientation, layer height, nozzle
  temperature, fan, extrusion multiplier, speed vs translucency.
- **Hamp et al. 2021** (`hamp2021transmittance`, Appl. Opt. 60:6573): spectral transmittance vs layer
  height/width, temperature, speed, orientation; ~50 % at 50 µm layers.
- **Quero et al. 2021** (`quero2021microfluidic`, Lab Chip 21:3715): ~80 % visible transmission at 640 µm by
  thin layers and a 0.2 mm airbrush-tip nozzle.
- **Amendola et al. 2021** (`amendola2021diffuse`, PLOS ONE 16:e0253181): absorption and reduced scattering
  coefficients of FDM PLA/ABS as a function of print parameters (diffuse-optics phantoms) — i.e. *low*
  transparency as a controlled target.
- **Ren et al. 2023** (`ren2023anisotropy`, Opt. Mater. 138:113743): optical anisotropy (birefringence) of
  printed transparent polymers depends on the printing process — the polymer analogue of the stress
  birefringence problem in printed glass.
- **Blachowicz et al. 2021** (`blachowicz2021optical`, e-Polymers 21:549): review; FDM lenses whose
  transmission/scattering is adjusted through nozzle diameter and raster angle.
- **Rooney et al. 2024** (`rooney2024lenses`, Adv. Mater. Technol. 9:2400043): printed imaging lenses made
  transparent by spin-coating resin over layer artefacts.
- **Ma, Zhou & Zhang 2023** (`anisotag2023`, CHI 2023): G-code tool that lays smooth cylindrical-surface
  microstructures at chosen angles so the FDM surface reflects distinct patterns under a collimated laser —
  the toolpath direction as an *engineered reflection* property.
- Reviews: **Heinrich et al. 2016** (`heinrich2016optics`, Adv. Opt. Technol. 5:293), **Gao et al. 2023**
  (`gao2023review`, Mater. Today 69:107).
- Community practice (CNC Kitchen, Prusa/Eryone guides; not peer-reviewed): transparency in PETG needs
  aligned rectilinear infill at 0°, no top/bottom layers, single perimeter, ≥100 % flow, slow speed, no
  cooling — i.e. a *toolpath recipe* for transparency exists empirically but not as an optimisation.

### 2.4 Computational design and fabrication of optical appearance (graphics community)

- Caustic design: **Papas 2011** (micro-facets), **Kiser 2013** (continuous architectural surfaces),
  **Yue 2014** (Poisson-based continuous surface), **Schwartzburg 2014** (optimal transport, high contrast,
  CNC-milled acrylic/glass), **Zhou 2025** (surface light sources, differentiable rendering, physically
  validated). All assume the fabrication process reproduces a computed freeform surface.
- **Zhao et al. 2016** perforated lampshades (hole distribution ⇒ projected image).
- Light routing in printed objects: **Willis 2012** Printed Optics; **Pereira 2014** computational light
  routing (fibre paths optimised for curvature and separation).
- Translucency / subsurface scattering: **Dong 2010**, **Papas 2013**, **Elek 2017**, **Brunton 2018**,
  **Nagasawa 2023** (surface texture ⇒ perceived translucency) — voxel/material assignment, not toolpath.
- Reflectance: **Weyrich 2009** milled microfacet arrays for custom BRDFs.

## 3. Gap statement (for the monograph, Problem 9)

Given a target global shape and a target optical response (transmittance/haze map, caustic image,
reflection or scattering signature, lens or waveguide function), compute the deposition toolpath —
cord layout, layer height, bead width, coiling pattern, speed/temperature schedule, surface relief —
of a molten-glass or other transparent extrusion process such that the printed part realises the optical
target within the shape tolerance. Ingredients that exist: a validated forward light model of printed glass
(Weber 2020), a differentiable caustic renderer with process-aware regularisation (Kassubeck 2021),
computational caustic design methods (Papas/Kiser/Yue/Schwartzburg/Zhou), a demonstration that glass
toolpaths change heat retention and hence interlayer physics (Chhadeh 2026), per-element optical control
of deposition parameters (Liu 2024, Rettschlag 2020, Kranert 2020, Hong 2023), gradient toolpath generators
for optical fields (Sage 2026), and DOE-type parameter maps for polymer transparency and scattering
(Kumar, Vochozka, Hamp, Quero, Amendola). Missing: the coupling — a model of cord cross-section relief and
its visco-capillary healing as a function of toolpath variables, embedded in a differentiable optical
objective, optimised under the process constraints of molten glass (continuous single path, slump, thermal
history, nozzle-set layer height).

## 4. Negative findings

- No OpenAlex/Crossref hit for combinations of {toolpath, tool path, print path} × {caustic, optical,
  transparency} × {glass} other than Chhadeh 2026 (mechanical) and Kassubeck 2021 (reconstruction).
- No publication from Evenline, Maple Glass Printing, Nobula or Micron3DP on optical toolpath design; the
  lighting/art products rely on the default layer-seam caustics.
- Inglessis/Oxman "reverse-engineer geometry from designed light patterns" (2017) has no published follow-up.
- No paper found on intentionally controlled devitrification or opalescence gradients as an opacity
  design variable in direct glass deposition.
