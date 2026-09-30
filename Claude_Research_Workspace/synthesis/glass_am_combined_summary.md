# Additive Manufacturing of Molten Glass

**Created:** 2026-09-30T12:37:33+03:00  
**Updated:** 2026-09-30T14:25:31+03:00  
**Generator:** Claude Code (Model: Claude Fable 5.1, claude-fable-5-1)  
**Updated by:** Codex (Model: gpt-6-astra)

**Original prompt:**
> analyse the research results in all workspaces and create a comprehensive summary, remove irrelevant information if there is any. create a md and a latex file, if you use figures from the other workspaces reevaluate and improve the figures.

**Context:**

- Merges the molten-glass 3D printing research of the Claude, ChatGPT and Antigravity workspaces into one account, with corrections and redrawn figures.
- Two direct routes work and do not overlap; optical and mechanical data are thin; toolpath design for optical targets is an open problem.

**Consolidated summary of the Claude, ChatGPT and Antigravity research workspaces**

Analysis, figures and text by Claude (Anthropic), 30 September 2026

## Contents

- [Purpose and method](#purpose-and-method)
- [Principal findings](#principal-findings)
- [Process taxonomy and history](#process-taxonomy-and-history)
- [Physics that sets the process window](#physics-that-sets-the-process-window)
- [Machines](#machines)
- [Thermal management, sensing and control](#thermal-management-sensing-and-control)
- [Properties of printed glass](#properties-of-printed-glass)
- [Open problems](#open-problems)
- [Research groups](#research-groups)
- [Companies](#companies)
- [Roadmap](#roadmap)
- [Corrections and removals](#corrections-and-removals)
- [Figure provenance](#figure-provenance)
- [References](#references)

## Purpose and method

Three AI-assisted research workflows addressed the same brief on 3D printing with molten glass between 26 and 30 September 2026: Claude[^claude], ChatGPT (Codex)[^chatgpt] and Antigravity[^antigravity]. Each produced LaTeX report sources in its own workspace. Here, ChatGPT denotes the Codex workflow that produced the ChatGPT_Research_Workspace report. This summary was originally written by Claude[^summary], which is also the author of one of the three reports it compares. Codex checked and corrected the account of its own workflow in this section on 30 September; this was not an independent review of the entire synthesis. The summary merges the results into one account, keeps what is supported by a primary source, corrects what the workspaces got wrong, and leaves out what does not bear on molten-glass printing.

[^claude]: Claude Fable 5.1 from Anthropic, model ID `claude-fable-5-1` with the 1M-token context option, reasoning effort high, permission mode auto. It ran in the Claude Code extension for VS Code, version 2.1.283 for the main research on 26 September and 2.1.284 for the toolpath search on 29 September. Read from the session logs.

[^chatgpt]: Local session records identify OpenAI model `gpt-6-astra`, with high reasoning effort for the research turns; the initial model-selection question used low effort. Recorded settings were reasoning summaries off, approval policy never and sandbox `danger-full-access`. The recorded client was Codex for VS Code, with CLI 0.155.0-alpha.16.3; the extension build number was not independently established from these records. The parent thread began on 26 September and continued through 30 September, including a status turn on 27 September. It spawned academic, commercial and asset agents on 26 September, source-review and asset-completion agents on 29 September, and a final-review agent on 30 September. These form one coordinated workflow, not independent research replications. Repeated or inherited turn-context records were not counted as separate turns. The output directory is `ChatGPT_Research_Workspace`.

[^antigravity]: Gemini 3.1 Pro from Google, in Antigravity IDE 2.5.5 with language server 2.17.0. Terminal commands were set to run automatically, artifact review was set to turbo, and the terminal sandbox was off. The model was read on 30 September from the saved model selection of the IDE, last written on 26 September, and the other settings from its configuration file. The user states these are unchanged since the research. The session itself keeps no readable model record.

[^summary]: Claude Fable 5.1, model ID `claude-fable-5-1` with the 1M-token context option, reasoning effort high, permission mode auto, in Claude Code 2.1.284 for VS Code, on 30 September 2026. It continued the session that ran the toolpath search.

Every statement below was traced to the section text, notes and source files of at least one workspace. Where two workspaces disagreed, the primary paper or the archived datasheet decided. Numerical claims that rested only on a third-party listing are marked as such. All analytical figures were redrawn from one script; the section “Figure provenance” records what was changed.

**Table 1.** What each workspace contributed.

|  | Claude | ChatGPT (Codex) | Antigravity |
|---|---|---|---|
| Model and tool | Claude Fable 5.1, effort high, in Claude Code | gpt-6-astra, research effort high, in Codex for VS Code | Gemini 3.1 Pro, in Antigravity IDE |
| Size of the report | 43 pages, about 16 000 words, 147 references | 27 pages, about 8 500 body words, 43 references | 8 short sections, about 800 words, 5 references, never compiled |
| Sources on disk | 23 papers, 4 patents, 105 catalogued works | 13 papers, 3 datasheets, 3 patents | none |
| Strongest content | Breadth of the literature, quantitative machine data, open problems, group and company directories | Source qualification, unit handling, reproducible viscosity/flow/thermal and cost models, provenance of company facts | none that the other two lack |
| Main weakness | Some vendor figures taken from third-party listings; one wrong sensitivity figure; two unreadable figures | Smaller literature corpus; limited matched performance data; some requested media were not acquired | Three of five references are wrong; several factual errors |

The Codex counts were checked against the final PDF and source inventory: 27 pages, 43 cited bibliography entries, 13 research/review PDFs, three manufacturer datasheets and three patent PDFs. The approximate body count is 8 500 whitespace-delimited words extracted from PDF pages 3--23, including tables and captions; the whole PDF, including front matter and references, contains about 10 700. Its photoelasticity figure deliberately illustrates a measurement method using conventional tempered glass and is explicitly captioned as not a printed specimen. It is not presented as evidence of measured stress in printed glass. The comparison of strengths and weaknesses above is an editorial assessment, not a controlled model benchmark.

## Principal findings

1. **Two direct routes work and they do not overlap.** Crucible-fed extrusion deposits kilograms per hour of transparent soda-lime glass in centimetre-wide cords [[1](#ref-klein2015), [2](#ref-inamura2018), [3](#ref-mit2024masonry)]. Laser filament deposition lays down fused silica at sub-millimetre scale and cubic millimetres per minute with nanometre roughness [[4](#ref-kth2022bonding), [5](#ref-lgd2024homog), [6](#ref-kth2024microlens)]. Rod-fed hot-nozzle printers sit between them in scale [[7](#ref-chhadeh2026toolpath)]. No process yet prints transparent glass at sub-millimetre resolution and a useful volume rate (Figure 10).
2. **Viscosity is the governing material property.** Every process can be placed on the viscosity curve of its glass. Melt extrusion leaves the nozzle at $10^{3}$ to $10^{4.5}$ dPa·s, which soda-lime reaches near 1000 °C, borosilicate near 1270 °C and fused silica only above 2000 °C (Figure 3). That is why fused silica is printed with lasers and not through nozzles.
3. **Thermal history controls geometry, bonding, stress and strength at once.** The heat that fuses a new cord to the layer below also lets the wall slump. A chamber held just below the annealing point is what made crack-free soda-lime prints possible [[1](#ref-klein2015)]. The 2026 toolpath study showed that the path alone changes bending strength by about 40 % through the heat retained between passes [[7](#ref-chhadeh2026toolpath)].
4. **Transparent is not the same as optical.** No crucible-fed part has a published transmission spectrum, wavefront error or three-dimensional stress map. Laser-filament and indirect routes have such data for small parts [[8](#ref-luo2018quartz), [5](#ref-lgd2024homog), [9](#ref-destino2018)].
5. **Mechanical data are thin.** Reported bending strengths span 6 MPa for powder-bed parts to about 72 MPa for laser-deposited quartz (Figure 12). Sample counts are small, test set-ups differ, and no Weibull distribution has been published for any printed glass.
6. **The contact materials limit melt extrusion.** Alumina nozzles dissolve in the melt and set campaign lengths of two to three weeks [[2](#ref-inamura2018)]. Borosilicate and aluminosilicate extrusion needs 1250 to 1450 °C and a nozzle material that survives it.
7. **Closed-loop control exists only for temperature in laser processes.** Pyrometer and thermal-camera feedback to laser power are demonstrated [[10](#ref-lgd2025tempctrl), [11](#ref-dgf2026control)]. No printer of any kind measures bead geometry and corrects it during the layer.
8. **Commercial activity is small and only partly verifiable.** Evenline sells printed objects and services, Maple Glass Printing and Nobula sell or prepare machines, and Glassomer sells materials for the competing indirect route. Current prices, yields and rated temperature limits could not be verified from primary sources.
9. **Nobody has optimised a glass toolpath for an optical target.** The forward simulation, the inverse caustic renderer and the caustic-design mathematics all exist separately [[12](#ref-weber2020photon), [13](#ref-kassubeck2021caustics), [14](#ref-schwartzburg2014caustics)]. Their combination for a viscous glass cord is an open problem.

## Process taxonomy and history

The useful first split is whether the glass is molten when it is deposited (direct) or shaped cold and converted to glass in a furnace (indirect). Both detailed workspaces adopt it; Figure 1 shows the merged version. The indirect routes share the material but not the process science. They are governed by colloid chemistry, debinding and sintering shrinkage, and appear here only as the benchmark for resolution and optical quality [[15](#ref-kotz2017), [16](#ref-nguyen2017), [17](#ref-toombs2022)].

![Figure 1](figures/fig_taxonomy.png)

*Figure 1. Taxonomy of glass additive manufacturing. The left branch is the subject of this summary. Glass-fibre-filled polymers, sugar glass, metallic glass and printed metal moulds for glass are outside both branches.*

The four direct families differ in feedstock and heat source.

- **Crucible-fed melt extrusion.** A charge of 2 to 25 kg is held molten in a kiln at 1040 to 1200 °C and drains by gravity through a heated ceramic nozzle into a chamber near the annealing point. This is the G3DP line from MIT, continued by Evenline [[1](#ref-klein2015), [2](#ref-inamura2018), [3](#ref-mit2024masonry), [18](#ref-stern2024cgc)].
- **Rod-fed hot-nozzle extrusion.** A solid rod is pushed into a small nozzle at 900 to 1000 °C, as in polymer filament printing. Only a few millimetres of glass are molten. Maple Glass Printing, the earlier Micron3DP machines and the TU Darmstadt rod-on-float work belong here [[7](#ref-chhadeh2026toolpath), [19](#ref-seel2018), [20](#ref-micron3dp_acers)].
- **Laser filament or fibre deposition.** A fibre of 0.1 to 0.2 mm or a rod of 1 to 3 mm is fed into a CO₂ laser focus and wets the substrate. There is no nozzle in contact with the melt. Three groups developed it under three names: digital glass forming at Missouri S&T and Notre Dame [[21](#ref-luo2017sodalime), [22](#ref-kinzel2025dgf)], laser glass deposition in Hannover [[23](#ref-witzendorff2018), [24](#ref-lgd2021coaxial)], and direct glass laser deposition at KTH and Nobula [[4](#ref-kth2022bonding)].
- **Laser melting of powder or paste.** Powder-bed fusion and blown-powder deposition melt glass locally but leave 5 to 12 % porosity and opaque parts in most reports [[25](#ref-fateri2015), [26](#ref-datsiou2019), [27](#ref-datsiou2021), [28](#ref-spirrett2023)]. Coaxial powder-fed quartz and paste with in-situ laser melting reach dense glass [[29](#ref-lang2024), [30](#ref-paste2024)].

![Figure 2](figures/fig_timeline.png)

*Figure 2. Milestones by process family, 2014 to 2026. Only first reports and first machine releases are shown.*

The field moved through three phases (Figure 2). From 2014 to 2018 the routes were demonstrated: rod-fed CO₂ laser printing at Missouri S&T, G3DP and G3DP2 at MIT, and quartz-fibre deposition in Hannover [[31](#ref-luo2014jmse), [1](#ref-klein2015), [2](#ref-inamura2018), [23](#ref-witzendorff2018)]. From 2019 to 2022 process windows were mapped and the first desktop machines appeared [[26](#ref-datsiou2019), [4](#ref-kth2022bonding)]. Since 2023 the work has turned to application and control: recycled-glass masonry, optical surfaces of 21 nm roughness, real-time temperature control, and the first systematic strength study of a rod-fed printer [[3](#ref-mit2024masonry), [5](#ref-lgd2024homog), [11](#ref-dgf2026control), [7](#ref-chhadeh2026toolpath)].

## Physics that sets the process window

### Viscosity

Viscosity over the whole forming range follows the Vogel–Fulcher–Tammann form

$$
\log_{10}\eta = A + \frac{B}{T - T_0}
$$

with $\eta$ in dPa·s. Four reference points locate a process on the curve: the strain point at $10^{14.5}$, the annealing point at $10^{13}$, the softening point at $10^{7.6}$ and the working point at $10^{4}$ dPa·s. One dPa·s is 0.1 Pa·s, so a curve quoted in Pa·s sits one decade lower; the two workspaces used different units and the constants must not be mixed.

![Figure 3](figures/fig_vft_viscosity.png)

*Figure 3. Viscosity of four glass families fitted to manufacturer fixed points. Curves are solid inside the fixed points and dashed where extrapolated. The hollow markers are the fixed points of a second silica grade and show how much a family name leaves open. The black diamond is the measured G3DP nozzle-exit state [[1](#ref-klein2015)].*

**Table 2.** Fitted constants for $\eta$ in dPa·s and temperature in °C. A dagger marks fits with $A$ fixed at the universal high-temperature limit [[32](#ref-mauro2009)] because only three fixed points are published.

| Glass | $A$ | $B$ (K) | $T_0$ (°C) | Temperature at $10^{4}$ dPa·s |
|---|---|---|---|---|
| Soda-lime float [[33](#ref-valleydesign_sls)] | −2.39 | 5210 | 206 | 1023 °C |
| BOROFLOAT 33 borosilicate [[34](#ref-schott_borofloat)] | −1.68 | 6578 | 112 | 1270 °C |
| EAGLE XG boro-aluminosilicate† [[35](#ref-corning_eaglexg)] | −1.93 | 6947 | 250 | about 1420 °C, extrapolated |
| Lamp-grade fused quartz† [[36](#ref-heraeus_quartz)] | −1.93 | 13351 | 317 | above 2000 °C, extrapolated |

Three points follow from Figure 3 and Table 2.

- The two workspaces fitted BOROFLOAT 33 independently and obtained the same constants. Their soda-lime fits use different products, float glass and SCHOTT AR-GLAS tubing [[37](#ref-schott_arglas)], and agree to within 20 °C at the working point.
- A family name is not a material law. Lamp-grade fused quartz and the synthetic high-hydroxyl grade HPFS 7980 differ by 125 to 230 °C at the same viscosity [[36](#ref-heraeus_quartz), [38](#ref-silica_hpfs)].
- Any silica working point is an extrapolation of more than 300 °C beyond the last published fixed point. It shows that a nozzle process is out of reach. It is not an operating temperature.

Evenline recalibrates its machine for a new soda-lime source by setting two fitted curves equal and solving for the temperature that gives the proven viscosity. This predicted a set point of 1037 °C for float glass from 1023 °C for studio glass, and the first print came within 3.2 % of the predicted mass [[18](#ref-stern2024cgc)]. The working range of six soda-lime compositions was nearly constant at about 295 °C.

### Flow through the nozzle

The melt moves at a Reynolds number near $10^{-4}$, so the Hagen–Poiseuille law applies:

$$
Q = \frac{\pi r^{4}}{8\,\eta L}\,\Delta p, \qquad \Delta p = \rho g H .
$$

Flow scales with the fourth power of bore radius and inversely with viscosity. More than half the resistance of the G3DP crucible and nozzle sat in the last 10 mm of bore [[1](#ref-klein2015)]. Flow also falls as the crucible empties, which is why G3DP2 raised the ratio of reservoir to print volume from 4.6 % to 29 % [[2](#ref-inamura2018)]. Rod-fed and filament-fed machines avoid the drift because a motor sets the volume rate.

![Figure 4](figures/fig_flow_vs_temperature.png)

*Figure 4. Sensitivity of gravity-fed flow to a temperature error at the nozzle, from the fits of Table 2. The ratio needs no assumption about nozzle geometry because flow is inversely proportional to viscosity.*

A 10 °C error at the soda-lime working point changes the flow by about 19 % (Figure 4). The Claude monograph stated 30 %, which its own fit does not support. The conclusion stands: nozzle temperature has to be held within a few degrees. A heater set point is not the glass temperature. G3DP measured 920 °C at the exit against a nozzle-kiln set point of 1010 °C [[1](#ref-klein2015)].

### Capillary instability, slump and coiling

A water jet breaks into drops spaced 4.5 diameters apart. Molten glass is in the opposite limit: the Ohnesorge number of a 10 mm soda-lime cord is of order $10^{3}$, inertia is irrelevant, and the growth rate is set by the visco-capillary time $\eta a/\sigma$ (Figure 5). For a G3DP cord this is about 16 s at the nozzle and rises by five orders of magnitude within a few layers, so the cord never breaks up. The same time scale governs how far surface tension smooths the seam between layers. In laser fibre printing the time is about 10 s at full temperature, and a fibre held hot for that long necks and detaches [[11](#ref-dgf2026control)].

![Figure 5](figures/fig_capillary_instability.png)

*Figure 5. Growth rate of the capillary instability of a liquid cylinder in the inviscid limit and in the viscous limit that applies to molten glass [[39](#ref-rayleigh1878), [40](#ref-tomotika1935)].*

Slump is a race between gravity and cooling. The sag velocity scales as $\rho g h a^{2}/\eta$: millimetres per second at the nozzle and micrometres per second once the glass has cooled by 350 °C. This explains the empirical limits of the G3DP machines: overhangs of 30 to 35°, turning radii of 6 to 15 mm and layer heights up to 5 mm [[1](#ref-klein2015), [3](#ref-mit2024masonry)]. If the nozzle is lifted well above the part, the falling cord coils like a rope. The pattern is selected by fall height and travel speed and can be programmed [[41](#ref-brun2017)].

Marangoni flow is negligible in the large cord of a crucible-fed printer and significant in laser melt pools, where surface temperature gradients reach thousands of kelvin per millimetre [[42](#ref-machines2026meltpool)]. In nozzle printing the dominant interfacial effect is glass wetting the nozzle face and pulling the cord sideways [[2](#ref-inamura2018)].

### Cooling and residual stress

A lumped model of radiation and convection shows how cord diameter and surroundings set the cooling rate (Figure 6).

![Figure 6](figures/fig_cord_cooling.png)

*Figure 6. Cooling of soda-lime cords of four diameters released at 1050 °C. In a heated chamber the cord stays above the annealing point until the programmed anneal. In room air a 2 mm bead is rigid within seconds and carries stress that has to be annealed out afterwards.*

The heated-chamber case reproduces the measured drop of about 350 °C across five layers in G3DP [[1](#ref-klein2015)]. It also shows why thin beads allow bridges and overhangs but need a heated enclosure. The Maple 4 used in the 2026 study prints into a 500 °C chamber for this reason [[7](#ref-chhadeh2026toolpath)].

The stress frozen in by a temperature difference $\Delta T$ across a wall is of order

$$
\sigma \approx \frac{E\,\alpha\,\Delta T}{2(1-\nu)} ,
$$

about 40 MPa per 100 °C for soda-lime, which is comparable to its practical strength. The expression is a scale and not a prediction for a free three-dimensional part. Fused silica, with an expansion coefficient eighteen times smaller, tolerates the gradients of laser deposition. Stress relaxes in about 15 minutes at the annealing point and in hours at the strain point. Thermal diffusion time grows with the square of thickness, about 40 s for 5 mm and 10 minutes for 20 mm, so the thickest section sets the schedule.

## Machines

### Crucible-fed extrusion

Three separately heated zones sit above a moving build plate (Figure 7). The melter conditions the glass, the nozzle meters it, and the chamber keeps the growing part rigid but close to stress-free.

![Figure 7](figures/fig_crucible_printer.png)

*Figure 7. Thermal zones of a crucible-fed printer of the G3DP type and the process chain around it. Temperatures and dimensions from the G3DP and G3DP2 papers [[1](#ref-klein2015), [2](#ref-inamura2018)].*

**Table 3.** The three generations of the crucible-fed platform.

|  | G3DP (2015) | G3DP2 (2018) | G3DP3, Evenline (2024) |
|---|---|---|---|
| Glass charge | 2.1 kg | 25.5 kg | not reported |
| Melter temperature | 1040–1165 °C | 1090 °C | up to 1200 °C |
| Nozzle | alumina, 10 mm bore | alumina, 11.5 mm bore | ceramic, redesigned |
| Chamber | heated, near the annealing point | 480 °C, 12 kW | heated, with infrared camera |
| Build volume (mm) | 250 × 250 × 300 | 320 × 320 × 350 | 325 × 325 × 380 |
| Deposition rate | about 2.2 kg/h | 5.2 kg/h, 570 mm³/s | feed 6–20 mm/s |
| Motion | kiln on X–Y, bed on Z | fixed kiln, four-axis bed | not reported |

G3DP2 moved the bed and kept the thermal module still, held ten 200 mm cylinders within 0.7 mm of diameter, and printed the 3 m columns shown in Milan in 2017 as stacked segments [[2](#ref-inamura2018)]. Its thermal module draws 15 kW while printing. G3DP3 prints studio, container and float glass, including recycled cullet, with beads 9 to 16 mm wide and 3 to 6 mm high [[3](#ref-mit2024masonry), [18](#ref-stern2024cgc)]. Neither machine can interrupt the flow, so every part is one continuous path. That constraint shaped the figure-eight masonry unit in Figure 8.

![Figure 8](figures/fig_g3dp3_photos.png)

*Figure 8. Left: the G3DP3 printer with the build chamber below the furnace. Right: interlocking masonry units printed on it. Both from Massimino et al. [[3](#ref-mit2024masonry)], CC BY 4.0, scaled to a common height and placed side by side.*

### Rod-fed hot-nozzle extrusion

The best-documented operating point is the Maple 4 in the 2026 strength study: 3.5 mm soda-lime rod, nozzle tip at 940 °C, 1.5 mm outlet, lines 2 mm wide and 1 mm high at 4 mm/s, chamber at 500 °C [[7](#ref-chhadeh2026toolpath)]. That is about 8 mm³/s. The company also builds a machine that draws rod from cullet. Micron3DP showed a similar concept in 2015 and claimed borosilicate printing at 1640 °C; the claim was never documented and no activity was found after 2021 [[20](#ref-micron3dp_acers)]. Corning filed and abandoned an application for an induction-heated platinum–rhodium version [[43](#ref-patent_corning2021)].

### Laser filament deposition

A laser head replaces the nozzle with a focused beam, so nothing touches the melt (Figure 9). Three groups developed the hardware.

![Figure 9](figures/fig_laser_filament_head.png)

*Figure 9. A laser filament deposition head. Parameter ranges from the Missouri S&T, Hannover and KTH studies [[21](#ref-luo2017sodalime), [23](#ref-witzendorff2018), [4](#ref-kth2022bonding)].*

- **Missouri S&T and Notre Dame.** Rod, filament and stripped telecom fibre as feedstock; a melt-temperature model validated by spectroscopy; a narrow window between incomplete fusion and bubble formation; side-injected heating of the interface; thermal-camera feedback on a real-time platform in 2026 [[21](#ref-luo2017sodalime), [44](#ref-luo2017heat), [45](#ref-hostetler2018fiber), [46](#ref-capps2021interface), [11](#ref-dgf2026control)].
- **Hannover.** Quartz fibre at 120 W up to 300 mm/min; a coaxial head that heats the fibre symmetrically to lower stress; fully dense silica with 21 nm roughness at 90 mm/min, rising to 220 nm at 180 mm/min [[23](#ref-witzendorff2018), [24](#ref-lgd2021coaxial), [5](#ref-lgd2024homog)].
- **KTH and Nobula.** Four beams from a 25 W laser, 196 µm fibre fed at 150 % of the geometric rate, 200 µm layers; bonding width mapped against power, speed and feed; a 105-layer wall without stress birefringence; microlens arrays printed in under ten seconds per lens [[4](#ref-kth2022bonding), [6](#ref-kth2024microlens)].

### Powder and paste routes

Laser powder-bed fusion of soda-lime in a commercial machine gave about 12 % porosity and 6 to 7 MPa bending strength; a heat treatment at 650 °C improved translucency [[26](#ref-datsiou2019), [27](#ref-datsiou2021)]. Milled powder reached 95 % density [[47](#ref-slmirregular2023)] and borosilicate powder 94 % [[48](#ref-boro2025laser)]. Powder blown onto bottles is proposed for decoration [[28](#ref-spirrett2023)]. Coaxial powder-fed quartz reached 72 MPa, 95 % of conventional quartz [[29](#ref-lang2024)].

### Comparison

**Table 4.** Reported envelope of each direct route, with the two main indirect routes for contrast. "n.r." means not reported in a primary source.

| Route | Glass and temperature | Feature size | Deposition rate | Optical state | Bending strength |
|---|---|---|---|---|---|
| Crucible-fed extrusion | soda-lime; melter 1040–1200 °C, chamber 480–525 °C | bead 9–16 mm wide | 240–570 mm³/s | transparent, dense, ribbed surface; spectrum n.r. | 41–56 MPa annealed |
| Rod-fed hot nozzle | soda-lime; nozzle 940–1000 °C | bead 1.5–2 mm | about 8 mm³/s | transparent to translucent; n.r. | 40–56 MPa by orientation |
| Laser filament | fused silica at 1700–2200 °C; also soda-lime, borosilicate | 0.1–1 mm | about 0.01–0.25 mm³/s | dense, 21 nm roughness; 0.12 nm on lenses | n.r. |
| Laser powder-bed | soda-lime, borosilicate, silica | about 0.1 mm tracks | n.r. | opaque as built | 6–7 MPa |
| Powder-fed laser deposition | quartz, soda-lime | millimetre tracks | n.r. | semi-transparent to transparent | 72 MPa (quartz) |
| Indirect: photopolymer and sintering | fused silica; sinter 1300 °C | tens of micrometres | n.r. | transparent; 6–60 nm roughness | n.r. |
| Indirect: direct ink writing | silica, silica–titania | sub-millimetre | n.r. | optical grade after polishing | n.r. |

![Figure 10](figures/fig_rate_vs_feature.png)

*Figure 10. Deposition rate against deposited feature width for the three routes that print transparent glass directly. Ranges from Table 4.*

Rates are deposition rates. None includes annealing, finishing or rejected parts, and they must not be read as production rates.

## Thermal management, sensing and control

Three thermal architectures are in use. Crucible-fed and heated-chamber rod-fed printers keep the whole part just below the annealing point. Laser and powder processes use a build plate at 250 to 600 °C and anneal afterwards, which suits fused silica and is marginal for soda-lime [[26](#ref-datsiou2019), [28](#ref-spirrett2023)]. Torches and secondary beams serve as local auxiliaries. A heated chamber is not an anneal: G3DP2 soaks the part at 525 °C and then moves it to a separate oven [[2](#ref-inamura2018)].

Sensing has four layers.

- **Thermocouples** control every kiln zone but read the refractory and not the glass.
- **Thermal cameras** at 7.9 µm read the cord surface because glass is opaque there. G3DP3 records peak cord temperatures of 969 to 1059 °C depending on the glass and corrects set points between prints from the difference between printed and predicted mass [[18](#ref-stern2024cgc)]. Readings depend on assumed emissivity, viewing angle and reflections from hot walls.
- **Pyrometers and spectrometers** on laser melt pools detect the onset of bubble formation and feed back to laser power [[44](#ref-luo2017heat), [10](#ref-lgd2025tempctrl)].
- **Cameras** are used for observation. The Hannover platform images the transmitted wavefront of the finished part to find bubbles and striae [[5](#ref-lgd2024homog)].

The 2026 controller for digital glass forming put a thermal camera into a deterministic control loop and showed that multilayer walls fail at constant laser power and succeed under feedback [[11](#ref-dgf2026control)]. On crucible-fed machines the flow cannot be changed within a layer, so geometry is controlled through travel speed. G3DP ran the bed 7 % faster than the natural exit speed for the most uniform cord [[1](#ref-klein2015)]. Bead cross-section follows from mass conservation, so a slowdown at a corner thickens the wall unless the flow changes with it.

Residual stress is checked with a polariscope. The published readings are qualitative [[1](#ref-klein2015), [4](#ref-kth2022bonding)]. Quantitative methods for complex glass shapes exist and have not been applied to printed glass [[49](#ref-aben2008)].

## Properties of printed glass

### Optical

Optical quality has four separate parts: bulk transmission, scattering, wavefront error and surface form. A ribbed wall can transmit most of the light and still distort every image (Figure 11). The evidence is uneven.

![Figure 11](figures/commons_caustics.jpg)

*Figure 11. Lamps printed on the G3DP platform and lit from above. Each cord acts as a cylindrical lens and the wall projects caustics. Photograph by Neri Oxman, Wikimedia Commons, CC BY-SA 4.0 [[50](#ref-commons_caustics)].*

- Crucible-fed parts are documented by photographs and caustic projection. Cut faces were polished for testing [[1](#ref-klein2015), [3](#ref-mit2024masonry)].
- Laser-filament parts have measured transmission and index homogeneity for fused quartz, a wavefront free of bubbles and striae, and lens surfaces of 0.12 nm roughness [[8](#ref-luo2018quartz), [5](#ref-lgd2024homog), [6](#ref-kth2024microlens)].
- Index homogeneity against commercial optical glass is published only for the indirect ink-writing route, on polished parts [[9](#ref-destino2018)].

Bubbles come from gas released when the melt is reheated, from air trapped where a filament fails to wet the layer below, and from the pores between powder particles [[44](#ref-luo2017heat), [4](#ref-kth2022bonding), [27](#ref-datsiou2021)]. Devitrification has not been reported in crucible-fed prints, but those papers also report no diffraction measurement, so the absence is not established.

### Mechanical

The published strength values come from five studies with different tests (Figure 12).

![Figure 12](figures/fig_bending_strength.png)

*Figure 12. Bending strength reported for printed glass. The tests differ in geometry, surface state and sample count, so the chart shows what has been measured and is not a ranking [[7](#ref-chhadeh2026toolpath), [29](#ref-lang2024), [2](#ref-inamura2018), [27](#ref-datsiou2021)].*

- G3DP samples differed by about 40 % in strength between the two test orientations, and samples printed cold had one fifth of the strength of those printed into the heated chamber [[1](#ref-klein2015)].
- Eight annealed G3DP2 cylinders gave 41 to 56 MPa. The Milan columns were designed with a safety factor of ten [[2](#ref-inamura2018)].
- Printed masonry units failed first at 3.6 to 42 MPa and carried 64 to 118 MPa before collapse in compression. The strongest units combined a printed body with a separately made interlocking base [[3](#ref-mit2024masonry)].
- In the rod-fed study, specimens with the infill at 90° to the beam axis averaged 56 MPa and those at 0° averaged 40 MPa, against 73.5 MPa for the unprinted rod. The authors attribute the difference to the shorter path of the 90° pattern, which keeps the previous bead warmer. Their four-point set-up deviates from the standard in dimensions and loading rate [[7](#ref-chhadeh2026toolpath)].

The orientation result is a within-study comparison. It should not be turned into a design factor.

## Open problems

**Table 5.** Open problems, the evidence behind each, and what a solution would have to show.

| Problem | Evidence | Needed |
|---|---|---|
| 1. Devitrification | Glass is held for weeks at working temperature and every layer reheats the one below; crucible-fed papers report no diffraction data | Time–temperature–transformation data per composition; in-line detection; nozzles without stagnant films |
| 2. Optical quality | No transmission spectrum, haze or wavefront value for a crucible-fed part | Standard coupon measurements; a model of seam relief from temperature, surface tension and dwell time |
| 3. Residual stress | Only qualitative polariscope readings; 100 °C of gradient leaves 40 MPa in soda-lime | Viscoelastic simulation of a multilayer build checked against scattered-light polarimetry |
| 4. Nozzle and crucible life | Alumina campaigns last two to three weeks; borosilicate needs 1250–1450 °C | Life tests of platinum alloys and dense zirconia in the actual glass; quick-change nozzle |
| 5. Geometric closed loop | Temperature feedback exists for lasers; bead width and slump are not measured anywhere | Bead-geometry sensing at the layer time scale and travel-speed control |
| 6. Mechanical qualification | Small samples, mixed test set-ups, no Weibull statistics | Four-point bending on large populations in two orientations with fractography |
| 7. Feedstock range | Recycled container and float glass print after viscosity matching; contaminated cullet untested | Contamination tolerance; borosilicate and aluminosilicate extrusion |
| 8. Economics | 3 kWh/kg for G3DP2 before annealing; no matched-part cost comparison | Cost per accepted part against casting and pressing; crossover batch size |
| 9. Toolpath design for optical targets | Forward and inverse light simulation exist separately; glass toolpaths optimised only for strength | A cord-relief model coupled to a differentiable optical model, optimised under the process constraints |

Problem 9 was added on 29 September after a dedicated search. No publication was found that computes a toolpath of molten glass, or of any transparent extruded material, to meet an optical target within a fixed shape. The nearest work is as follows.

- **Glass optics recorded but not designed.** Caustics of G3DP prints and the columns of the Milan installation were outcomes of geometry chosen for other reasons. Reverse design from a light pattern was named as future work and not published [[1](#ref-klein2015), [2](#ref-inamura2018), [51](#ref-inglessis2017glass2)].
- **Simulation in both directions.** Photon mapping of printed glass was validated against measurement [[12](#ref-weber2020photon)]. A differentiable caustic renderer reconstructs the shape of laser-deposited glass from its caustic image, as a process-control signal [[13](#ref-kassubeck2021caustics)].
- **Caustic design for milled surfaces.** The mathematics is mature for surfaces that a machine reproduces exactly [[52](#ref-papas2011caustics), [53](#ref-yue2014caustics), [14](#ref-schwartzburg2014caustics)].
- **Deposition parameters as optical variables.** Layer count sets the focal length of printed silica microlenses, and a deposited fibre path is a waveguide [[6](#ref-kth2024microlens), [54](#ref-kranert2020waveguide)]. In the indirect ink-writing route the toolpath carries a refractive-index profile [[55](#ref-dyllaspears2020grin), [56](#ref-sage2026fermat)].
- **Transparent polymers.** Layer height, line width, raster angle and speed have been mapped against transmittance, scattering and birefringence, as experiments with a single number as the target [[57](#ref-kumar2024transparency), [58](#ref-vochozka2024translucency), [59](#ref-hamp2021transmittance), [60](#ref-ren2023anisotropy)].

## Research groups

**Table 6.** Groups with published work on direct glass deposition, and adjacent groups that set the benchmarks.

| Group | Process | Contribution |
|---|---|---|
| MIT Mediated Matter, then MIT Mechanical Engineering with Evenline | Crucible-fed extrusion | G3DP, G3DP2, G3DP3; columns, masonry, recycled glass [[1](#ref-klein2015), [2](#ref-inamura2018), [3](#ref-mit2024masonry)] |
| Missouri S&T and University of Notre Dame (Kinzel, Landers, Bristow) | Laser filament and fibre | Melt-temperature model, fused-quartz optics, thermal-camera control [[21](#ref-luo2017sodalime), [8](#ref-luo2018quartz), [11](#ref-dgf2026control)] |
| Laser Zentrum Hannover and Leibniz University Hannover | Laser fibre deposition, lateral and coaxial | Quartz structures, 21 nm surfaces, micro-lenses and waveguides [[23](#ref-witzendorff2018), [5](#ref-lgd2024homog), [61](#ref-rettschlag2020microlens)] |
| KTH Stockholm (Fokine, Liu, Oriekhov), spin-off Nobula | Four-beam laser filament | Bonding-width map, microlens arrays [[4](#ref-kth2022bonding), [6](#ref-kth2024microlens)] |
| TU Darmstadt with Deakin University (Seel, Birbilis) | Rod-fed hot nozzle | Rod on float glass, point fixings, toolpath and strength [[19](#ref-seel2018), [62](#ref-pointfixings2024), [7](#ref-chhadeh2026toolpath)] |
| University of Nottingham (Goodridge, Datsiou, Spirrett) | Powder-bed and powder-fed laser | Process window, porosity and strength, bottle decoration [[26](#ref-datsiou2019), [27](#ref-datsiou2021), [28](#ref-spirrett2023)] |
| TU Ilmenau and Carl Zeiss Jena | Rod-fed laser; powder-bed borosilicate | Borosilicate and soda-lime rod deposition; density map [[63](#ref-froehlich2022), [48](#ref-boro2025laser)] |
| Institute of Optics and Electronics, Chengdu | Coaxial powder and wire laser deposition of quartz | 72 MPa quartz; closed-loop melt temperature [[29](#ref-lang2024), [10](#ref-lgd2025tempctrl)] |
| Université Laval; Łukasiewicz Network and University of Warsaw | Extrusion of low-temperature glasses | Chalcogenide glass on a modified polymer printer; printed fibre preforms [[64](#ref-baudet2019), [65](#ref-laval2023preform)] |
| Freiburg and Karlsruhe (Rapp, Kotz-Helmer); LLNL (Dylla-Spears) | Indirect routes | Photopolymer and ink routes to fused silica and gradient-index glass [[15](#ref-kotz2017), [16](#ref-nguyen2017), [55](#ref-dyllaspears2020grin)] |
| TU Delft (Oikonomopoulou, Bristogianni) | Cast glass | Interlocking masonry designs that MIT adapted for printing |

Both detailed workspaces searched for the institutions named in the brief and agree on the negative results. No molten-glass printing publication was found for McGill University, Nagaoka University of Technology or the Fraunhofer institutes IKTS, ISC and IPT. Their related work concerns sintered glass-filled filament, hybrid polymers and printed metal moulds for glass pressing. TU Delft works on cast structural glass. LLNL's glass printing is direct ink writing followed by sintering, which is an indirect route despite the name. RISE appears in a KTH project record as a collaborator on laser glass processing, but no RISE printer is documented.

## Companies

**Table 7.** Companies and what could be verified.

| Company | Offer | Verified from primary sources | Not verified |
|---|---|---|---|
| Evenline, Rochester NY | Printed objects and services on G3DP3; does not sell machines | Founder Michael Stern; build volume 325 × 325 × 380 mm; studio, container and float glass; operation near 1093 °C and up to 1200 °C in the masonry study [[66](#ref-evenline_web), [3](#ref-mit2024masonry)] | Prices, yield, funding |
| Maple Glass Printing, Melbourne | Rod-fed desktop printers and a rod-drawing machine | Patent application naming Birbilis, Feenstra and Koutsonikolas; Maple 4 used in a 2026 study at 940 °C [[67](#ref-maple_patent), [7](#ref-chhadeh2026toolpath)] | Current sales status; the price of about USD 45 000 comes from a third-party listing [[68](#ref-maple_aniwaa)] |
| Nobula3D, Stockholm | Laser filament printer for fused silica, with filament | KTH spin-off of 2021; investment by KTH Holding; EU grant of EUR 2.5 million on a project cost of EUR 3.6 million, ending April 2026 [[69](#ref-nobula_kthventures), [70](#ref-nobula_cordis), [6](#ref-kth2024microlens)] | Rated specifications; a resolution of 10 µm quoted by distributors conflicts with the 200 µm filament and is discarded |
| Micron3DP, Israel | Hot-nozzle printer shown 2015 to 2017 | Public demonstrations [[20](#ref-micron3dp_acers)] | Borosilicate claim; any activity after 2021 |
| Glassomer, Freiburg | Silica composites for the indirect route, parts service | Founded 2018; binder removal at 600 °C, sintering at 1300 °C, about 30 % shrinkage in the two-photon variant with UpNano [[71](#ref-upnano2024)] | Production yield |

Applications follow the two capabilities. Large cords suit art, lighting and architectural elements where the ribbed surface is wanted. The masonry work is the strongest case and is a prototype; a building product would need tests of joints, impact, fire and long-term load [[3](#ref-mit2024masonry)]. Laser filament printing suits micro-optics, fibre components and small silica parts. Printed glass microfluidic chips have been used for chemical analysis in a study co-authored by Micron3DP staff [[72](#ref-microfluidics2019)], and hollow tubes have been printed by laser filament deposition [[73](#ref-dgf2023tubes)]. Sealed, pressure-tested channels have not been reported for a direct route. No printed glass has been qualified for pressure vessels, and no work on printed containers for nuclear waste exists.

### Economics

The measured data are few. G3DP2 uses 15 kW at 5.2 kg/h, about 3 kWh/kg before annealing, against roughly 1 kWh/kg for a container-glass furnace [[2](#ref-inamura2018)]. Crucibles and nozzles are consumables on a cycle of weeks. One machine yields on the order of a thousand masonry units a year. Printing wins where each unit differs or where a mould cannot be amortised [[3](#ref-mit2024masonry)].

The ChatGPT workspace supplies a transparent cost model in place of missing data:

$$
C = \frac{K/Y + F}{N\,y} + \frac{c_{v}}{y}
$$

with capital $K$ over $Y$ years, annual fixed cost $F$, $N$ attempted parts a year, yield $y$ and variable cost $c_{v}$ per attempt. With assumed inputs for a studio cell (USD 100 000 over five years, USD 10 000 fixed cost, 1000 attempts, 80 % yield, USD 52 variable cost) the result is about USD 103 per accepted part. It rises to USD 137 at 60 % yield and to USD 215 at 250 attempts, while doubling the electricity price adds under USD 4. These inputs are assumptions and not vendor data. The model shows that utilisation and yield matter far more than energy.

## Roadmap

The two detailed workspaces reach the same priorities from different directions. One lists milestones and the other a staged qualification sequence.

1. **Measure before building another demonstrator.** Print a standard coupon set with every part: spectral transmission on polished faces, transmitted wavefront, scattered-light polarimetry, and four-point bending with Weibull statistics in two orientations.
2. **Map one glass on one machine completely.** Record deposited mass and bead geometry over temperature, head or feed, travel speed and layer return time, and keep the failed runs so that the boundaries of the window are known.
3. **Close the geometric loop.** Extract bead width from the thermal image that G3DP3 already records and control travel speed within the layer.
4. **Attack the nozzle.** Run life tests of platinum-alloy and zirconia nozzles in soda-lime, borosilicate and aluminosilicate melts. Rhodium can colour optical glass, so the alloy has to be chosen for the glass and the purity required [[74](#ref-heraeus_pgm), [75](#ref-pgm2010)].
5. **Scale fused silica.** Coaxial beams, side-injected heating and thicker rods are the identified ways to raise the rate without losing the surface [[24](#ref-lgd2021coaxial), [46](#ref-capps2021interface)].
6. **Join the two communities.** A CO₂ laser that follows an extrusion nozzle could fire-polish the seam and reheat the previous layer.
7. **Compute the anneal.** Couple a layer-by-layer thermal model to structural relaxation and check it against measured stress.
8. **Design the toolpath for light.** Problem 9 has all its ingredients and a clear first experiment: predict and measure the caustic of a printed wall as bead spacing and layer height are varied.

## Corrections and removals

**Table 8.** Statements corrected during consolidation.

| Source | Statement in the workspace | Corrected |
|---|---|---|
| Claude | A 10 °C nozzle error changes soda-lime flow by about 30 % | About 19 % from the same fit (Figure 4) |
| Claude | Taxonomy figure lists Micron3DP under crucible-fed extrusion | It is a hot-nozzle machine, as the Claude text itself says |
| Claude | Nobula resolves 10 µm; Maple 3 costs USD 45 000 | Both come from distributor listings; the first is discarded, the second marked as unverified |
| Claude | RISE is involved only through a journal editor | A KTH project record shows RISE as a project partner, without a printer |
| Claude | Birbilis listed under Deakin, ANU and RMIT for a review | The 2026 paper gives TU Darmstadt and Deakin University |
| Claude | Glass microfluidics for mass spectrometry were printed by the indirect route | The authors are from Micron3DP, a hot-nozzle company; the record on file does not state the process, so no route is asserted |
| ChatGPT | Figure of photoelastic fringes used in the optics chapter | The specimen is tempered architectural glass and was not printed; removed |
| ChatGPT | Working band drawn from $10^{4}$ to $10^{7}$ dPa·s | That is the forming range; nozzle-exit viscosity in the G3DP papers is $10^{3}$ to $10^{4.5}$ dPa·s |
| Antigravity | G3DP2 uses an industrial robot arm | A four-axis bed under a fixed kiln |
| Antigravity | Melting at up to 1900 °C | The press figure is 1900 °F, about 1040 °C |
| Antigravity | LLNL does direct molten deposition; TU Delft and Fraunhofer print molten glass | LLNL uses ink writing and sintering; no molten printing found at the others |
| Antigravity | Reference list | Wrong author list for the 2015 paper, an invented title for the 2018 paper, wrong title and pages for the 2014 laser-melting paper; none reused |

The following material was left out because it does not inform molten-glass printing.

- From the Antigravity workspace: everything. Its correct statements are general and are covered in more detail by the other two. Its notes file is empty and its build was never run.
- From the ChatGPT workspace: the photoelasticity image and polariscope video of conventional glass; the fit-residual plot, whose one message is given here in a sentence; the packaging, hashing and link-audit records; carbohydrate-glass bioprinting at McGill; and the general advice on procurement and qualification, which is reduced to the roadmap above.
- From the Claude workspace: the profiles of Vitriform3D, Mo-Sci, MIT Lincoln Laboratory and the Utah femtosecond project, which are indirect or unpublished; lunar regolith extrusion; the paragraph on nuclear-waste vitrification, for which no glass printing work exists; and the statement on total disclosed funding, which cannot be verified.

## Figure provenance

**Table 9.** What happened to each figure of the source workspaces.

| Figure here | Origin | Problem found and change made |
|---|---|---|
| Figure 1 | Claude | Connectors ran through the boxes and one company was misfiled. Redrawn with side connectors and corrected entries. |
| Figure 2 | Claude | Twelve overlapping labels on one axis, unreadable. Rebuilt as one lane per process family. |
| Figure 3 | Claude and ChatGPT | One hid extrapolation; the other marked it but used a redundant second panel. Merged: solid inside fixed points, dashed outside, both silica grades, measured G3DP point. |
| Figure 4 | ChatGPT | Flow was plotted against abstract viscosity for an invented nozzle. Replaced by the flow ratio against temperature error, which needs no geometry. |
| Figure 5 | Claude | Both plots were squeezed into a strip with the annotation off the axes. Rebuilt. |
| Figure 6 | Claude | Duplicate legends and rainbow colours for an ordered quantity. One blue ramp, direct labels, reference temperatures on the axis. |
| Figure 7 | Claude and ChatGPT | Labels overlapped the drawing in one; a title collided with a box and a box was unlabelled in the other. Merged into one drawing with callouts and the process chain. |
| Figure 9 | Claude | Caption text inside the canvas, labels touching the beams. Redrawn with callouts. It replaces the 498-pixel raster of the KTH set-up that both workspaces reproduced. |
| Figure 8 | ChatGPT (third-party) | Two separate images at different scales. Combined at a common height without enlargement. |
| Figure 11 | Claude (third-party) | Unchanged. |
| Figure 10, Figure 12 | new | Built from the consolidated tables. |
| not used | ChatGPT | Fit residuals, photoelastic fringes of tempered glass, deposited-line cross-sections. |

All colours come from a palette checked for colour-vision deficiency, and the script that draws the figures is kept with this summary.

## References

1. <a id="ref-klein2015"></a>John Klein et al. *Additive Manufacturing of Optically Transparent Glass*. 3D Printing and Additive Manufacturing 2, 92–105. 2015. [doi:10.1089/3dp.2015.0021](https://doi.org/10.1089/3dp.2015.0021)
2. <a id="ref-inamura2018"></a>Chikara Inamura et al. *Additive Manufacturing of Transparent Glass Structures*. 3D Printing and Additive Manufacturing 5, 269–283. 2018. [doi:10.1089/3dp.2018.0157](https://doi.org/10.1089/3dp.2018.0157)
3. <a id="ref-mit2024masonry"></a>Daniel Massimino et al. *Additive manufacturing of interlocking glass masonry units*. Glass Structures & Engineering 9, 397–417. 2024. [doi:10.1007/s40940-024-00279-8](https://doi.org/10.1007/s40940-024-00279-8)
4. <a id="ref-kth2022bonding"></a>Chunxin Liu, Taras Oriekhov and Michael Fokine. *Investigation of glass bonding and multi-layer deposition during filament-based glass 3D printing*. Frontiers in Materials 9. 2022. [doi:10.3389/fmats.2022.978861](https://doi.org/10.3389/fmats.2022.978861)
5. <a id="ref-lgd2024homog"></a>Khodor Sleiman, Katharina Rettschlag, Peter Jäschke and Stefan Kaierle. *Experimental investigation on the surface and volume homogeneity of additive manufactured fused silica components in the Laser Glass Deposition process*. Procedia CIRP 124, 275–278. 2024. [doi:10.1016/j.procir.2024.08.116](https://doi.org/10.1016/j.procir.2024.08.116)
6. <a id="ref-kth2024microlens"></a>Chunxin Liu et al. *Rapid Fabrication of Silica Microlens Arrays via Glass 3D Printing*. 3D Printing and Additive Manufacturing 11, 460–466. 2024. [doi:10.1089/3dp.2022.0112](https://doi.org/10.1089/3dp.2022.0112)
7. <a id="ref-chhadeh2026toolpath"></a>Philipp Amir Chhadeh et al. *The effect of toolpath design on the mechanical strength of additively manufactured glass components*. npj Advanced Manufacturing 3. 2026. [doi:10.1038/s44334-026-00072-1](https://doi.org/10.1038/s44334-026-00072-1)
8. <a id="ref-luo2018quartz"></a>Junjie Luo et al. *Additive manufacturing of transparent fused quartz*. Optical Engineering 57, 1–8. 2018. [doi:10.1117/1.oe.57.4.041408](https://doi.org/10.1117/1.oe.57.4.041408)
9. <a id="ref-destino2018"></a>Joel F. Destino et al. *3D Printed Optical Quality Silica and Silica–Titania Glasses from Sol–Gel Feedstocks*. Advanced Materials Technologies 3. 2018. [doi:10.1002/admt.201700323](https://doi.org/10.1002/admt.201700323)
10. <a id="ref-lgd2025tempctrl"></a>Jing Chen et al. *Temperature Control of Quartz-Glass Melting Areas in Laser Additive Manufacturing*. Micromachines 16, 29. 2024. [doi:10.3390/mi16010029](https://doi.org/10.3390/mi16010029)
11. <a id="ref-dgf2026control"></a>Balark Tiwari et al. *Temperature control of digital glass forming processes*. Additive Manufacturing 127, 105306. 2026. [doi:10.1016/j.addma.2026.105306](https://doi.org/10.1016/j.addma.2026.105306)
12. <a id="ref-weber2020photon"></a>Ramon E. Weber, Christoph Reinhart and Neri Oxman. *Photon mapping of geometrically complex glass structures: Methods and experimental evaluation*. Building and Environment 180, 106957. 2020. [doi:10.1016/j.buildenv.2020.106957](https://doi.org/10.1016/j.buildenv.2020.106957)
13. <a id="ref-kassubeck2021caustics"></a>Marc Kassubeck et al. *Shape from Caustics: Reconstruction of 3D-Printed Glass from Simulated Caustic Images*. 2021 IEEE Winter Conference on Applications of Computer Vision (WACV), 2876–2885. 2021. [doi:10.1109/wacv48630.2021.00292](https://doi.org/10.1109/wacv48630.2021.00292)
14. <a id="ref-schwartzburg2014caustics"></a>Yuliy Schwartzburg, Romain Testuz, Andrea Tagliasacchi and Mark Pauly. *High-contrast computational caustic design*. ACM Transactions on Graphics 33, 1–11. 2014. [doi:10.1145/2601097.2601200](https://doi.org/10.1145/2601097.2601200)
15. <a id="ref-kotz2017"></a>Frederik Kotz et al. *Three-dimensional printing of transparent fused silica glass*. Nature 544, 337–339. 2017. [doi:10.1038/nature22061](https://doi.org/10.1038/nature22061)
16. <a id="ref-nguyen2017"></a>Du T. Nguyen et al. *3D-Printed Transparent Glass*. Advanced Materials 29. 2017. [doi:10.1002/adma.201701181](https://doi.org/10.1002/adma.201701181)
17. <a id="ref-toombs2022"></a>Joseph T. Toombs et al. *Volumetric additive manufacturing of silica glass with microscale computed axial lithography*. Science 376, 308–312. 2022. [doi:10.1126/science.abm6459](https://doi.org/10.1126/science.abm6459)
18. <a id="ref-stern2024cgc"></a>Michael Stern, Ethan Townsend, Daniel Massimino and Kaitlyn Becker. *Advancing Sustainable 3D Printing: The Feasibility of Recycled Glass as a Building Material With Additive Manufacturing*. Challenging Glass Conference Proceedings 9. 2024. [doi:10.47982/cgc.9.583](https://doi.org/10.47982/cgc.9.583)
19. <a id="ref-seel2018"></a>M. Seel et al. *Fused glass deposition modelling for applications in the built environment: <b>Schmelzschichten aus Glas für Anwendungen im Bauwesen</b>*. Materialwissenschaft und Werkstofftechnik 49, 870–880. 2018. [doi:10.1002/mawe.201800075](https://doi.org/10.1002/mawe.201800075)
20. <a id="ref-micron3dp_acers"></a>American Ceramic Society. *3D printing reaches the final materials frontier – Micron3DP innovates in glass*. Ceramic Tech Today. 2015. <https://ceramics.org/ceramic-tech-today/3d-printing-reaches-the-final-materials-frontier-micron3dp-innovates-in-glass/>
21. <a id="ref-luo2017sodalime"></a>Junjie Luo et al. *Additive Manufacturing of Transparent Soda-Lime Glass Using a Filament-Fed Process*. Journal of Manufacturing Science and Engineering 139. 2017. [doi:10.1115/1.4035182](https://doi.org/10.1115/1.4035182)
22. <a id="ref-kinzel2025dgf"></a>E.C. Kinzel. *Digital glass forming using direct heating techniques*. Additive Manufacturing of Glass, 15–55. 2025. [doi:10.1016/b978-0-323-85488-7.00010-6](https://doi.org/10.1016/b978-0-323-85488-7.00010-6)
23. <a id="ref-witzendorff2018"></a>Philipp von Witzendorff et al. *Additive manufacturing of glass: CO2-Laser glass deposition printing*. Procedia CIRP 74, 272–275. 2018. [doi:10.1016/j.procir.2018.08.109](https://doi.org/10.1016/j.procir.2018.08.109)
24. <a id="ref-lgd2021coaxial"></a>Tobias Grabe et al. *Additive anufacturing of fused silica using coaxial laser glass deposition: experiment, simulation and discussion*. Laser 3D Manufacturing VIII, 32. 2021. [doi:10.1117/12.2577205](https://doi.org/10.1117/12.2577205)
25. <a id="ref-fateri2015"></a>Miranda Fateri and Andreas Gebhardt. *Selective Laser Melting of Soda-Lime Glass Powder*. International Journal of Applied Ceramic Technology 12, 53–61. 2014. [doi:10.1111/ijac.12338](https://doi.org/10.1111/ijac.12338)
26. <a id="ref-datsiou2019"></a>Kyriaki Corinna Datsiou et al. *Additive manufacturing of glass with laser powder bed fusion*. Journal of the American Ceramic Society 102, 4410–4414. 2019. [doi:10.1111/jace.16440](https://doi.org/10.1111/jace.16440)
27. <a id="ref-datsiou2021"></a>K.C. Datsiou et al. *Laser powder bed fusion of soda lime silica glass: Optimisation of processing parameters and evaluation of part properties*. Additive Manufacturing 39, 101880. 2021. [doi:10.1016/j.addma.2021.101880](https://doi.org/10.1016/j.addma.2021.101880)
28. <a id="ref-spirrett2023"></a>Fiona Spirrett et al. *Powder-fed directed energy deposition of soda lime silica glass on glass substrates*. Journal of the American Ceramic Society 106, 227–240. 2022. [doi:10.1111/jace.18638](https://doi.org/10.1111/jace.18638)
29. <a id="ref-lang2024"></a>Ming Lang et al. *Efficient Fabrication of Quartz Glass Using Laser Coaxial Powder-Fed Additive Manufacturing Approach*. 3D Printing and Additive Manufacturing 11, 655–665. 2024. [doi:10.1089/3dp.2022.0137](https://doi.org/10.1089/3dp.2022.0137)
30. <a id="ref-paste2024"></a>Haobo Zhang et al. *Direct additive manufacturing of transparent fused silica glasses using an integrated paste printing and laser in-situ melting technology*. Additive Manufacturing 84, 104135. 2024. [doi:10.1016/j.addma.2024.104135](https://doi.org/10.1016/j.addma.2024.104135)
31. <a id="ref-luo2014jmse"></a>Junjie Luo, Heng Pan and Edward C. Kinzel. *Additive Manufacturing of Glass*. Journal of Manufacturing Science and Engineering 136, 061024. 2014. [doi:10.1115/1.4028531](https://doi.org/10.1115/1.4028531)
32. <a id="ref-mauro2009"></a>John C. Mauro et al. *Viscosity of glass-forming liquids*. Proceedings of the National Academy of Sciences 106, 19780–19784. 2009. [doi:10.1073/pnas.0911705106](https://doi.org/10.1073/pnas.0911705106)
33. <a id="ref-valleydesign_sls"></a>Valley Design Corp.. *Soda-lime float glass properties*. Valley Design Corp.. 2023. <https://valleydesign.com/sodalime/>
34. <a id="ref-schott_borofloat"></a>SCHOTT AG. *BOROFLOAT 33 – Thermal Properties (technical data sheet)*. SCHOTT AG, Mainz. 2024. <https://www.schott.com/en-cz/products/borofloat/-/media/project/onex/products/b/borofloat/downloads/borofloat33_therm_eng_web.pdf>
35. <a id="ref-corning_eaglexg"></a>Corning Incorporated. *Corning EAGLE XG Glass – Product Information Sheet*. Corning Incorporated, Corning NY. 2019. <https://www.corning.com/media/worldwide/cdt/documents/EAGLE_XG_Glass_PI_Sheet.pdf>
36. <a id="ref-heraeus_quartz"></a>Heraeus Covantics. *Quartz materials and fused silica for lamp applications (technical brochure)*. Heraeus, Hanau. 2023. <https://www.heraeus-covantics.com/media/Media/Documents/Products_and_Solutions/LAMP/EN/Quartz_lamp_materials_EN.pdf>
37. <a id="ref-schott_arglas"></a>SCHOTT AG. *AR-GLAS: Tubing and Rod of Special Glass*. SCHOTT. <https://media.schott.com/api/public/content/79a671737b4a4833aa91c99f68c4b5a3?v=eb1ee445>
38. <a id="ref-silica_hpfs"></a>Corning Incorporated. *HPFS 7979, 7980, 8655 Fused Silica: Optical Materials Product Information*. Corning. 2025. <https://www.corning.com/media/worldwide/csm/documents/HPFS_Product_Brochure_All_Grades_2025_11.pdf>
39. <a id="ref-rayleigh1878"></a>Lord Rayleigh. *On The Instability Of Jets*. Proceedings of the London Mathematical Society s1-10, 4–13. 1878. [doi:10.1112/plms/s1-10.1.4](https://doi.org/10.1112/plms/s1-10.1.4)
40. <a id="ref-tomotika1935"></a>S. Tomotika. *On the instability of a cylindrical thread of a viscous liquid surrounded by another viscous fluid*. Proceedings of the Royal Society of London. Series A - Mathematical and Physical Sciences 150, 322–337. 1935. [doi:10.1098/rspa.1935.0104](https://doi.org/10.1098/rspa.1935.0104)
41. <a id="ref-brun2017"></a>P.-T. Brun et al. *The molten glass sewing machine*. Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences 375, 20160156. 2017. [doi:10.1098/rsta.2016.0156](https://doi.org/10.1098/rsta.2016.0156)
42. <a id="ref-machines2026meltpool"></a>Lianshuang Ning, Weijie Fu and Xinming Zhang. *Melt Pool Dynamics and Quantitative Prediction of Surface Topography in Laser Selective Forming of Optical Glass*. Machines 14, 122. 2026. [doi:10.3390/machines14010122](https://doi.org/10.3390/machines14010122)
43. <a id="ref-patent_corning2021"></a>Christopher W. Drewnowski et al. *Additive manufacturing systems and method for making glass articles*. United States Patent and Trademark Office. 2021. <https://patents.google.com/patent/US20210101818A1/en>
44. <a id="ref-luo2017heat"></a>Junjie Luo et al. *Heat Transfer in Additive Manufacturing of Glass*. Volume 2: Heat Transfer Equipment; Heat Transfer in Multiphase Systems; Heat Transfer Under Extreme Conditions; Nanoscale Transport Phenomena; Theory and Fundamental Research in Heat Transfer; Thermophysical Properties; Transport Phenomena in Materials Processing and Manufacturing. 2017. [doi:10.1115/ht2017-5100](https://doi.org/10.1115/ht2017-5100)
45. <a id="ref-hostetler2018fiber"></a>Edward C. Kinzel et al. *Fiber-fed laser-heated process for printing transparent glass from single mode optical fiber*. Laser 3D Manufacturing V, 6. 2018. [doi:10.1117/12.2291443](https://doi.org/10.1117/12.2291443)
46. <a id="ref-capps2021interface"></a>Nicholas E. Capps et al. *Direct laser heating of the filament/substrate interface in digital glass forming*. Manufacturing Letters 31, 106–109. 2022. [doi:10.1016/j.mfglet.2021.08.005](https://doi.org/10.1016/j.mfglet.2021.08.005)
47. <a id="ref-slmirregular2023"></a>Tian Yang et al. *Selective laser melting of glass with irregular shaped powder*. Journal of Materials Research and Technology 26, 7259–7272. 2023. [doi:10.1016/j.jmrt.2023.09.011](https://doi.org/10.1016/j.jmrt.2023.09.011)
48. <a id="ref-boro2025laser"></a>Anne-Marie Layher et al. *Laser-Based Additive Manufacturing of Alkali Borosilicate Glass Powder: Influence of Laser-Beam Properties on Component Quality*. Journal of Manufacturing and Materials Processing 9, 305. 2025. [doi:10.3390/jmmp9090305](https://doi.org/10.3390/jmmp9090305)
49. <a id="ref-aben2008"></a>H. Aben, J. Anton and A. Errapart. *Modern Photoelasticity for Residual Stress Measurement in Glass*. Strain 44, 40–48. 2008. [doi:10.1111/j.1475-1305.2008.00422.x](https://doi.org/10.1111/j.1475-1305.2008.00422.x)
50. <a id="ref-commons_caustics"></a>Neri Oxman. *Caustic patterns of a 3D printed glass structure (photograph, CC BY-SA 4.0)*. Wikimedia Commons. 2015. <https://commons.wikimedia.org/wiki/File:Caustic_patterns_of_a_3D_printed_glass_structure.jpg>
51. <a id="ref-inglessis2017glass2"></a>Nassia Inglessis and Neri Oxman. *Glass 2.0: Templating Light in 3D Printed Glass Architecture*. Project documentation, STUDIO INI / Mediated Matter Group, MIT Media Lab (Members Week 2016; exhibited as GLASS II, La Triennale di Milano, April 2017). 2017. <https://www.nassia-inglessis.com/6813836-gl1>
52. <a id="ref-papas2011caustics"></a>Marios Papas et al. *Goal-based Caustics*. Computer Graphics Forum 30, 503–511. 2011. [doi:10.1111/j.1467-8659.2011.01876.x](https://doi.org/10.1111/j.1467-8659.2011.01876.x)
53. <a id="ref-yue2014caustics"></a>Yonghao Yue et al. *Poisson-Based Continuous Surface Generation for Goal-Based Caustics*. ACM Transactions on Graphics 33, 1–7. 2014. [doi:10.1145/2580946](https://doi.org/10.1145/2580946)
54. <a id="ref-kranert2020waveguide"></a>Fabian Kranert et al. *Generation of functional curved waveguides by CO2-laser based deposition of coreless fused silica fibers*. 3D Printed Optics and Additive Photonic Manufacturing II, 11. 2020. [doi:10.1117/12.2554516](https://doi.org/10.1117/12.2554516)
55. <a id="ref-dyllaspears2020grin"></a>Rebecca Dylla-Spears et al. *3D printed gradient index glass optics*. Science Advances 6. 2020. [doi:10.1126/sciadv.abc7429](https://doi.org/10.1126/sciadv.abc7429)
56. <a id="ref-sage2026fermat"></a>M.R. Sage et al. *Towards gradient multimaterial toolpath generation for direct ink writing with connected fermat spirals*. Additive Manufacturing 123, 105214. 2026. [doi:10.1016/j.addma.2026.105214](https://doi.org/10.1016/j.addma.2026.105214)
57. <a id="ref-kumar2024transparency"></a>Atish Kumar and Narendra Kumar. *Enhancing optical transparency of 3D printed PLA parts via multi-response optimization*. Optics & Laser Technology 175, 110865. 2024. [doi:10.1016/j.optlastec.2024.110865](https://doi.org/10.1016/j.optlastec.2024.110865)
58. <a id="ref-vochozka2024translucency"></a>Vladimír Vochozka et al. *Fused Filament Fabrication 3D Printing Parameters Affecting the Translucency of Polylactic Acid Parts*. Polymers 16, 2862. 2024. [doi:10.3390/polym16202862](https://doi.org/10.3390/polym16202862)
59. <a id="ref-hamp2021transmittance"></a>Shannon M. Hamp, Riley D. Logan and Joseph A. Shaw. *Optical transmittance of 3D printing materials*. Applied Optics 60, 6573. 2021. [doi:10.1364/ao.427525](https://doi.org/10.1364/ao.427525)
60. <a id="ref-ren2023anisotropy"></a>Zhangyu Ren and Yang Ju. *Optical anisotropy of transparent polymer materials fabricated via 3D printing and their application in photoelasticity*. Optical Materials 138, 113743. 2023. [doi:10.1016/j.optmat.2023.113743](https://doi.org/10.1016/j.optmat.2023.113743)
61. <a id="ref-rettschlag2020microlens"></a>K. Rettschlag et al. *Laser glass deposition of spheres for printing micro lenses*. Procedia CIRP 94, 276–280. 2020. [doi:10.1016/j.procir.2020.09.052](https://doi.org/10.1016/j.procir.2020.09.052)
62. <a id="ref-pointfixings2024"></a>Philipp Amir Chhadeh et al. *Design of additively manufactured glass components for glass point fixings*. Glass Structures & Engineering 10. 2025. [doi:10.1007/s40940-024-00290-z](https://doi.org/10.1007/s40940-024-00290-z)
63. <a id="ref-froehlich2022"></a>F. Fröhlich, J. Hildebrand and J. P. Bergmann. *Additive Manufacturing with Borosilicate Glass and Soda-Lime Glass*. 2nd International Conference on Advanced Joining Processes (AJP 2021), 151–164. 2022. [doi:10.1007/978-3-030-95463-5_10](https://doi.org/10.1007/978-3-030-95463-5_10)
64. <a id="ref-baudet2019"></a>E. Baudet et al. *3D-printing of arsenic sulfide chalcogenide glasses*. Optical Materials Express 9, 2307. 2019. [doi:10.1364/ome.9.002307](https://doi.org/10.1364/ome.9.002307)
65. <a id="ref-laval2023preform"></a>Przemysław Gołębiewski et al. *3D soft glass printing of preforms for microstructured optical fibers*. Additive Manufacturing 79, 103899. 2024. [doi:10.1016/j.addma.2023.103899](https://doi.org/10.1016/j.addma.2023.103899)
66. <a id="ref-evenline_web"></a>Evenline Inc.. *Molten Glass 3D Printer – Technology*. Evenline Inc., Rochester NY. 2025. <https://www.evenline.co/technology>
67. <a id="ref-maple_patent"></a>Nick Birbilis, Darren Robert Feenstra and Tony Koutsonikolas. *Three-dimensional printing system*. Australian patent application AU2021289614A1, applicant Maple Glass Printing Pty Ltd. 2023. <https://patents.google.com/patent/AU2021289614A1/en>
68. <a id="ref-maple_aniwaa"></a>Aniwaa. *Maple Glass Printing Maple 3 overview – an industrial 3D printer*. Aniwaa Pte. Ltd.. 2024. <https://www.aniwaa.com/product/3d-printers/maple-glass-printing-maple-3/>
69. <a id="ref-nobula_kthventures"></a>KTH Ventures. *Nobula 3D – portfolio company*. KTH Holding AB. 2024. <https://kthventures.se/en/portfolio/nobula-3d>
70. <a id="ref-nobula_cordis"></a>European Commission. *Nobula: Breaking the glass ceiling in Additive Manufacturing through laser-assisted glass 3D printing*. CORDIS project record 190122644. 2025. [doi:10.3030/190122644](https://doi.org/10.3030/190122644)
71. <a id="ref-upnano2024"></a>UpNano GmbH. *Novel Process for 3D-Printing Macro-sized Fused Silica Parts with Hi-Res Features*. UpNano GmbH. 2024. <https://www.upnano.com/novel-process-for-3d-printing-macro-sized-fused-silica-parts-with-hi-res-features/>
72. <a id="ref-microfluidics2019"></a>Eran Gal-Or et al. *Chemical analysis using 3D printed glass microfluidics*. Analytical Methods 11, 1802–1810. 2019. [doi:10.1039/c8ay01934g](https://doi.org/10.1039/c8ay01934g)
73. <a id="ref-dgf2023tubes"></a>Nicholas Capps, Kiva Ford, Jonathan Goldstein and Edward Kinzel. *Printing Hollow Tubes Using Digital Glass Forming*. Journal of Manufacturing Science and Engineering 145. 2022. [doi:10.1115/1.4056200](https://doi.org/10.1115/1.4056200)
74. <a id="ref-heraeus_pgm"></a>Heraeus Precious Metals. *Glass Manufacturing Equipment: Precious Metal Components*. Heraeus. <https://www.heraeus-precious-metals.com/en/products-solutions/category/precious-metal-components/glass-manufacturing-equipment/>
75. <a id="ref-pgm2010"></a>Christophe Couderc. *Platinum Group Metals in Glass Making: An overview of the role of the pgms in the glass industry*. Platinum Metals Review 54, 186–191. 2010. [doi:10.1595/147106710x514012](https://doi.org/10.1595/147106710x514012)
