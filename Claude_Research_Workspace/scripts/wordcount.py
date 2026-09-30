#!/usr/bin/env python
"""wordcount.py - approximate prose word count of the LaTeX sections (tables and macros stripped)."""
import re, glob, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
tot = 0
for f in sorted(glob.glob(str(ROOT / "latex" / "sections" / "*.tex"))):
    s = pathlib.Path(f).read_text(encoding="utf-8")
    s = re.sub(r"%.*", "", s)
    s = re.sub(r"\\begin\{(sidewaystable|table|tabular)\}.*?\\end\{\1\}", "", s, flags=re.S)
    s = re.sub(r"\\(?:citep|citet|cite|cref|Cref|label|ref|includegraphics|input)\*?(?:\[[^\]]*\])?\{[^}]*\}", "", s)
    s = re.sub(r"\\[A-Za-z]+\*?", " ", s)
    s = re.sub(r"[{}\[\]&$^_]", " ", s)
    n = len([w for w in s.split() if re.search(r"[A-Za-z]{2,}", w)])
    tot += n
    print(f"{pathlib.Path(f).name}: {n}")
print("TOTAL prose words (excluding tables):", tot)
