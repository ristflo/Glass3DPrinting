#!/usr/bin/env python
"""patch_siunitx.py - normalise siunitx usage in the LaTeX sections and manual bib entries
(product dimensions -> \\qtyproduct, mixed literal/macro units -> pure macro units), and add
the manual bib entry for the 2026 digital-glass-forming controller paper if missing."""
import re, pathlib, glob

ROOT = pathlib.Path(__file__).resolve().parent.parent
files = glob.glob(str(ROOT / "latex" / "sections" / "*.tex")) + [str(ROOT / "scripts" / "build_bib.py")]
REPL = [
    (r"{\degree F}", r"{\degree}F"),
    (r"\SI{+-3}{\celsius}", r"\(\pm\)\SI{3}{\celsius}"),
    (r"\SI{+-1.0}{mm}", r"\(\pm\)\SI{1.0}{mm}"),
    (r"\SI{1.4}{W/m\,K}", r"\SI{1.4}{\watt\per\metre\per\kelvin}"),
    (r"\SI{1200}{J/kg\,K}", r"\SI{1200}{\joule\per\kilogram\per\kelvin}"),
    (r"\SI{280}{N\,cm}", r"\SI{280}{\newton\centi\metre}"),
    (r"\SI{15}{W/m^{2}K}", r"\SI{15}{\watt\per\square\metre\per\kelvin}"),
    (r"\SIrange{50}{100}{W/m^{2}K}", r"\SIrange{50}{100}{\watt\per\square\metre\per\kelvin}"),
    (r"\SI{9e-6}{K^{-1}}", r"\SI{9e-6}{\per\kelvin}"),
    (r"\SI{0.5e-6}{K^{-1}}", r"\SI{0.5e-6}{\per\kelvin}"),
    (r"\SI{-0.012}{K^{-1}}", r"\SI{-0.012}{\per\kelvin}"),
    (r"\SI{3.2}{ppm/K}", r"\SI{3.2e-6}{\per\kelvin}"),
    (r"\SI{0.5}{ppm/K}", r"\SI{0.5e-6}{\per\kelvin}"),
    (r"\SI{6}{inch}", "6-inch"),
    (r"\SI{2500}{kg/m^3}", r"\SI{2500}{\kilogram\per\cubic\metre}"),
    (r"\SI{2400}{kg/m^3}", r"\SI{2400}{\kilogram\per\cubic\metre}"),
    (r"\SI{0.32}{N/m}", r"\SI{0.32}{\newton\per\metre}"),
    (r"\SIrange{0.31}{0.33}{N/m}", r"\SIrange{0.31}{0.33}{\newton\per\metre}"),
    (r"torch-melted soda-lime rod on plate \citep{seel2018}", r"torch-melted soda-lime rod on plate \citep{rammig2012,seel2018}"),
]
prod = re.compile(r"\\SI\{([0-9.]+(?: x [0-9.]+)+)\}")
for f in files:
    p = pathlib.Path(f); s = p.read_text(encoding="utf-8"); o = s
    s = prod.sub(lambda m: "\\qtyproduct{" + m.group(1) + "}", s)
    for a, b in REPL:
        s = s.replace(a, b)
    if s != o:
        p.write_text(s, encoding="utf-8"); print("patched", p.name)

p = ROOT / "scripts" / "build_bib.py"; s = p.read_text(encoding="utf-8")
entry = """@article{dgf2026control,
  title = {Temperature control of digital glass forming processes},
  author = {Tiwari, Balark and Khadka, Nishan and Capps, Nicholas and Bos, Andre and Meredith, Douglas and Bernardin, John and Kinzel, Edward C. and Landers, Robert G.},
  journal = {Additive Manufacturing}, volume = {127}, pages = {105306}, year = {2026},
  publisher = {Elsevier BV}, doi = {10.1016/j.addma.2026.105306}, url = {https://doi.org/10.1016/j.addma.2026.105306}
}
"""
if "@article{dgf2026control" not in s:
    s = s.replace("@article{fluegel2007,", entry + "@article{fluegel2007,", 1)
    p.write_text(s, encoding="utf-8"); print("added dgf2026control to build_bib.py")
left = sum(len(prod.findall(pathlib.Path(f).read_text(encoding="utf-8"))) for f in files)
print("remaining product dimensions inside \\SI:", left)
