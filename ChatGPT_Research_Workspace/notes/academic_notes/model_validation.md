# Model interpretation and validation

The material anchors are archived in `sources/data/viscosity_inputs.json` and the actual datasheets in `sources/papers/phys_*.pdf`. AR-GLAS uses three points for three fitted VFT parameters, so exact interpolation is expected and does not demonstrate predictive accuracy. BOROFLOAT uses four nominal anchors. HPFS 7980 fixes T0 at 0 K and fits a two-parameter Arrhenius limit; its maximum residual is about 0.38 logarithmic decades and its working-point extrapolation is unsuitable for equipment design.

The scripts check monotonicity, inverse recovery of specified logarithmic thresholds, and the dPa s to Pa s conversion. Raw residuals and threshold extrapolation flags are retained. These checks establish numerical consistency of the stated models, not experimental validation.

The nozzle example assumes constant viscosity, laminar Newtonian flow, a cylindrical bore and hydrostatic pressure. The short bore makes omitted entrance effects material. Surface tension, density, dimensions, head and viscosity are scenario inputs. Characteristic capillary and gravitational deformation times assume constant viscosity and cannot be interpreted as observed failure times in a cooling bead.

The thermal diffusivity example uses low-temperature nominal properties: BOROFLOAT conductivity at 90 °C and heat capacity over 20–100 °C. It is not an annealing schedule. The fully restrained elastic stress scale is not the residual stress of a free printed object. Commercial economics uses analyst-selected inputs and distinct hypothetical products; its calculations do not rank actual machines.

Executed 29 September 2026: viscosity and engineering invariant checks passed; cost outputs reproduce the values printed in chapter 07. The numerical source files allow re-execution rather than reliance on values transcribed into prose.

Executed 30 September 2026: engineering script reran successfully after replacing the misleading “room temperature” diffusivity label with the documented low-temperature property ranges. The computed values did not change.
