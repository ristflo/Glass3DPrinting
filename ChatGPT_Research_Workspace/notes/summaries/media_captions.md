# Media audit — 29 September 2026

The four existing figures were decoded, visually inspected and matched to captions in the archived primary PDFs. Recommended captions and file hashes are in `sources/data/asset_addendum.json`. The original ledger was not changed.

| File | Caption and interpretation | Rights evidence |
|---|---|---|
| `Liu2022_Figure1.jpg` | Four CO2-laser beams heat a glass filament during deposition; source Figure 1. | Liu, Oriekhov and Fokine (2022), [DOI](https://doi.org/10.3389/fmats.2022.978861); CC BY notice on PDF page 1. |
| `Liu2022_Figure6.jpg` | Top views and cross-sections of lines printed at 10–100 mm/min, with laser power varied according to the source article; source Figure 6. This is not a generic micrograph of bubbles or residual stress. | Same article; no separate exclusion visible for this figure. |
| `Massimino2024_Figure1.png` | G3DP3 apparatus with build chamber below furnace and crucible; source Figure 1. | Massimino et al. (2024), [DOI](https://doi.org/10.1007/s40940-024-00279-8); article CC BY 4.0 clause and no figure-specific exclusion found. |
| `Massimino2024_Figure2.png` | Manufactured masonry units assembled before mechanical testing; source Figure 2. This image alone does not demonstrate a load rating or approved building system. | Same article, CC BY 4.0. |

For each reproduction, credit authors/year and original figure number, link the source and [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), and state that the image is unmodified. The recommended captions do this explicitly.

## New photoelastic image

`sources/media/Efferz2024_Figure2.png` is copied unchanged to `latex/figures/Efferz2024_Figure2.png`. The [primary article](https://doi.org/10.1007/s40940-024-00270-3) attributes the work to Lena Efferz, Christian Schuler and Geralt Siebert (2024) and licenses it under CC BY 4.0. Figure 2 has no separate credit exclusion. Its two panels show intensity and isochromatic images near the edge of a 10 mm fully tempered glass specimen. The marked positions are 1.0 and 1.6 mm from the edge; the dashed line marks the chamfer. **This is conventional tempered architectural glass, not printed glass.** Use as a measurement-method illustration only. Image dimensions, SHA-256, direct URL and full suggested caption are in the addendum.

A [Takis lazos photograph](https://commons.wikimedia.org/wiki/File:Photoelasticity_and_color_on_a_stressed_glass_plate.jpg), licensed CC BY-SA 4.0, was also identified. Its binary download returned HTTP 403; no local copy is claimed or used.

## Recent primary PDF

The publisher PDF of [Chhadeh et al. (2026)](https://doi.org/10.1038/s44334-026-00072-1) is archived as `sources/papers/2026_Chhadeh_Toolpath_Design_Mechanical_Strength.pdf`. All 11 pages parsed. **Its license is CC BY-NC-ND 4.0, not CC BY.** The unchanged PDF may be shared under those terms; this audit makes no claim that adapted article figures are freely redistributable. Extracted text is in `sources/data/text/2026_Chhadeh_Toolpath_Design_Mechanical_Strength.txt`.

## Video verification

| Video | Verification on 2026-09-29 |
|---|---|
| [MIT GLASS / G3DP](https://vimeo.com/136764796) | HTTP 200, but script-driven response without a title. Earlier identity record retained. Playback not verified. |
| [MIT GLASS II / G3DP2](https://vimeo.com/211778198) | Same limitation. Playback not verified. |
| [Inside Maple Glass Printing](https://www.youtube.com/watch?v=CSw0Kw6M8i0) | HTTP 200 and expected title present. Playback not verified. |
| [Polariscope](https://www.youtube.com/watch?v=IefRrdTmlbA) | Direct video discovered in the [University of Memphis demonstration page](https://www.memphis.edu/physics/demonstrations/polariscope.php). YouTube returned HTTP 200 and title Polariscope. Playback and specimen material not independently verified. |

The new polariscope link supplies a direct educational video reference, but cannot yet be described as a verified video of stresses in printed glass. No video binaries were copied. University of Maryland's M8-02 demonstration was also checked: a web-reader copy describes stressed glass and a video, while a direct request returned HTTP 404; no usable direct MPEG link was recovered.

## Reproducibility

Existing `scripts/scrapers/acquire_assets.py` (9,490 bytes) and `extend_assets.py` (3,844 bytes) are intact; no repair was needed. They were not rerun because they mutate the original ledger. `scripts/processors/build_asset_addendum.py` rebuilds the audit using existing files and the saved HTTP checks. It verifies PDFs/images, hashes assets, writes only the addendum and copies the new figure into the LaTeX figure folder. This audit does not validate licenses or claims for every other pre-existing source.
