#!/usr/bin/env python
"""sanitize_bib.py - post-process latex/references.bib: decode HTML entities from doi.org BibTeX,
map Unicode punctuation to LaTeX, escape bare ampersands, and report any remaining non-Latin-1 characters."""
import re, pathlib, html, unicodedata
ROOT = pathlib.Path(__file__).resolve().parent.parent
p = ROOT / "latex" / "references.bib"
s = p.read_text(encoding="utf-8")

# 1. HTML entities (doi.org returns &amp; &ndash; &lt; ...)
s = s.replace("&amp;", "\\&").replace("&ndash;", "--").replace("&mdash;", "---").replace("&lt;", "$<$").replace("&gt;", "$>$")
s = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), s)
s = s.replace("&nbsp;", "~")
# 2. bare ampersands inside field values (not already escaped)
s = re.sub(r"(?<!\\)&(?!amp;)", "\\&", s)
# 3. Unicode punctuation
MAP = {"–": "--", "—": "---", "‐": "-", "‑": "-", "‒": "-", "‘": "`", "’": "'",
       "“": "``", "”": "''", "…": "...", " ": "~", " ": "\\,", " ": "\\,", "−": "-",
       "×": "$\\times$", "°": "\\textdegree{}", "μ": "$\\mu$", "µ": "$\\mu$", "′": "'",
       "™": "\\texttrademark{}", "®": "\\textregistered{}", "​": "", "﻿": "",
       "ł": "{\\l}", "Ł": "{\\L}", "ę": "\\k{e}", "Ę": "\\k{E}", "ń": "\\'n", "Ń": "\\'N",
       "ś": "\\'s", "ż": "\\.z", "ź": "\\'z", "ć": "\\'c", "ą": "\\k{a}", "ó": "\\'o",
       "š": "\\v{s}", "č": "\\v{c}", "Š": "\\v{S}", "Č": "\\v{C}", "ž": "\\v{z}", "ř": "\\v{r}", "ě": "\\v{e}", "ů": "\\r{u}",
       "ä": "\\\"a", "ö": "\\\"o", "ü": "\\\"u", "Ä": "\\\"A", "Ö": "\\\"O", "Ü": "\\\"U", "ß": "\\ss{}",
       "é": "\\'e", "è": "\\`e", "í": "\\'i", "á": "\\'a", "ç": "\\c{c}", "ø": "{\\o}", "å": "\\r{a}",
       "ñ": "\\~n", "ê": "\\^e", "â": "\\^a", "û": "\\^u", "ô": "\\^o", "É": "\\'E"}
for a, b in MAP.items():
    s = s.replace(a, b)
# 4. subscript/superscript digits
SUB = {"₀": "$_0$", "₁": "$_1$", "₂": "$_2$", "₃": "$_3$", "₄": "$_4$", "²": "$^2$", "³": "$^3$"}
for a, b in SUB.items():
    s = s.replace(a, b)
# 5. bare underscores in text fields (URLs and DOIs keep theirs)
def esc_underscore(m):
    return m.group(1) + m.group(2).replace("_", "\\_")
s = re.sub(r"(\b(?:series|collection|title|journal|booktitle|publisher|note|address)\s*=\s*)(\{(?:[^{}]|\{[^{}]*\})*\})", esc_underscore, s)
s = s.replace("\\\\_", "\\_")
p.write_text(s, encoding="utf-8")
rest = sorted({c for c in s if ord(c) > 255})
print("remaining chars above U+00FF:", [(c, unicodedata.name(c, "?")) for c in rest])
