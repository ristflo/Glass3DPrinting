# Molten-glass additive manufacturing: executive summary

Research began 26 September 2026; targeted source verification continued on 29 September, with final editorial review on 30 September 2026. This is a scoped primary-source technical review, not an exhaustive systematic review or a certified engineering design.

## Principal findings

**Choose the route by the finished part's function.** Reservoir-fed molten extrusion is well suited to investigating large continuous forms, architectural demonstrators, and intentionally textured lighting or art. Laser filament deposition supports localized heating and smaller silica features. Photopolymer/ink routes shape a precursor before densification and provide a different route to fine glass structures. Their temperatures and production rates must not be compared without the downstream thermal and finishing steps.

**Thermal history controls more than printability.** The same heat that improves contact between layers also promotes deformation. Chamber temperature, bead temperature, nozzle temperature, and internal part temperature are different quantities. A heated chamber does not itself establish that a part is annealed. Toolpath, layer-return time, corners, and starts/stops change both geometry and thermal history.

**Recent evidence strengthens the mechanical case without creating universal design values.** Chhadeh et al. (2026), DOI [10.1038/s44334-026-00072-1](https://doi.org/10.1038/s44334-026-00072-1), report toolpath-dependent bending performance in extruded soda-lime specimens. Their within-study orientation effect and modified test geometry should not be converted into a general tensile-strength ratio or structural certification.

**Transparency is not equivalent to imaging quality.** Transmission, haze, wavefront error, surface figure, roughness, and residual stress require separate measurement. The report includes a photoelasticity image from conventional tempered glass to illustrate a measurement method; it is explicitly not a printed specimen.

**Commercial information remains incomplete.** Evenline, Maple, Nobula, Glassomer, and UpNano represent different offerings and levels of evidence. The report distinguishes supplier claims, affiliated research, patent disclosures, and funding records. Verified current equipment prices, production yields, and comparable numerical TRLs were not established. The cost calculations are transparent planning scenarios, not vendor quotations.

## Reproducible calculations

- Product-specific viscosity curves use SCHOTT AR-GLAS, SCHOTT BOROFLOAT 33, and Corning HPFS 7980 reference points. The silica curve is an approximate Arrhenius limit of VFT with larger residuals. Extrapolations are marked; its calculated working point is not a recommended operating temperature.
- An idealized gravity-nozzle example predicts 1.083 kg/h for explicitly stated inputs. It excludes entrance losses, thermal gradients and production downtime, so it is not a machine performance claim.
- Flow sensitivity, thermal-diffusion scales, and accepted-part cost scenarios are supplied as Python scripts and raw JSON/CSV results.

## Recommended next research

Select one glass grade and part family. Map flow and contact geometry, validate temperature measurements, qualify annealing on representative thick sections, then measure defects and functional performance. Compare the complete cost and cycle time per accepted part against conventional forming and relevant indirect AM methods.

Remaining evidence gaps include matched-route tensile/optical tests, grade-specific refractory lifetime, current commercial prices and yields, and direct molten-silicate apparatus attribution for some requested institutions. Link checks do not verify video playback; access failures are retained in the audit rather than reported as successful validation.
