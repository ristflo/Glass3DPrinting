#!/usr/bin/env python
"""build_summary.py - turns synthesis/summary_master.md into the two deliverables:

  glass_am_combined_summary.md   (numbered figures, tables and references, plain Markdown)
  glass_am_combined_summary.tex  (article class, natbib; compile with tectonic or xelatex)

The master uses a small Markdown subset: #/##/### headings with optional {#sec:id}, paragraphs,
"- " and "1. " lists, single-line $$ display math $$, pipe tables introduced by
"Table: caption {#tbl:id widths=a,b,...}", figures "![caption](path){#fig:id width=w}",
citations [@key; @key] and cross references @fig:id, @tbl:id, @sec:id.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = (ROOT / "summary_master.md").read_text(encoding="utf-8")
BIB = (ROOT / "references.bib").read_text(encoding="utf-8")
STEM = "glass_am_combined_summary"

# ------------------------------------------------------------------ front matter
m = re.match(r"---\n(.*?)\n---\n", SRC, re.S)
META = dict(l.split(": ", 1) for l in m.group(1).splitlines())
BODY = SRC[m.end():]

# ------------------------------------------------------------------ block parser
blocks, lines, i = [], BODY.split("\n"), 0
while i < len(lines):
    ln = lines[i]
    if not ln.strip():
        i += 1; continue
    h = re.match(r"(#{1,3}) (.+?)(?:\s*\{#(sec:[\w-]+)\})?\s*$", ln)
    if h:
        blocks.append(("h", len(h.group(1)), h.group(2), h.group(3))); i += 1; continue
    if ln.startswith("$$") and ln.rstrip().endswith("$$"):
        blocks.append(("math", ln.strip()[2:-2].strip())); i += 1; continue
    fn = re.match(r"\[\^([\w-]+)\]: (.+)$", ln)
    if fn:
        blocks.append(("fn", fn.group(1), fn.group(2))); i += 1; continue
    f = re.match(r"!\[(.*)\]\((.+?)\)\{#(fig:[\w-]+) width=([\d.]+)\}\s*$", ln)
    if f:
        blocks.append(("fig", f.group(1), f.group(2), f.group(3), float(f.group(4)))); i += 1; continue
    t = re.match(r"Table: (.*?)\s*\{#(tbl:[\w-]+) widths=([\d.,]+)\}\s*$", ln)
    if t:
        i += 1
        while not lines[i].strip(): i += 1
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
        blocks.append(("tbl", t.group(1), t.group(2), [float(x) for x in t.group(3).split(",")], rows[0], rows[2:])); continue
    if re.match(r"(- |\d+\. )", ln):
        ordered = not ln.startswith("- "); items = []
        while i < len(lines) and re.match(r"(- |\d+\. )", lines[i]):
            items.append(re.sub(r"^(- |\d+\. )", "", lines[i])); i += 1
        blocks.append(("list", ordered, items)); continue
    para = []
    while i < len(lines) and lines[i].strip():
        para.append(lines[i]); i += 1
    blocks.append(("p", " ".join(para)))

# ------------------------------------------------------------------ numbering and citation order
NUM, SECTITLE = {}, {}
nf = nt = 0
for b in blocks:
    if b[0] == "fig": nf += 1; NUM[b[3]] = nf
    if b[0] == "tbl": nt += 1; NUM[b[2]] = nt
    if b[0] == "h" and b[3]: SECTITLE[b[3]] = b[2]
FN = {b[1]: b[2] for b in blocks if b[0] == "fn"}
FN_RE = re.compile(r"\[\^([\w-]+)\]")
CITE_RE = re.compile(r"\[(@[\w:.-]+(?:;\s*@[\w:.-]+)*)\]")
order = []
for k in re.findall(r"@([\w:.-]+)", " ".join(CITE_RE.findall(BODY))):
    if k not in order: order.append(k)
bibkeys = set(re.findall(r"@\w+\{([^,\s]+),", BIB))
missing = [k for k in order if k not in bibkeys]
if missing: sys.exit(f"citation keys missing from references.bib: {missing}")
REF_RE = re.compile(r"@(fig|tbl|sec):([\w-]+)")
for kind, lab in REF_RE.findall(BODY):
    if kind != "sec" and f"{kind}:{lab}" not in NUM: sys.exit(f"undefined reference {kind}:{lab}")
    if kind == "sec" and f"sec:{lab}" not in SECTITLE: sys.exit(f"undefined section reference {lab}")


# ------------------------------------------------------------------ bibliography for the Markdown output
def parse_bib(text):
    out, pos = {}, 0
    for mm in re.finditer(r"@(\w+)\{([^,\s]+),", text):
        key, j, depth, start = mm.group(2), mm.end(), 1, mm.end()
        while depth and j < len(text):
            depth += {"{": 1, "}": -1}.get(text[j], 0); j += 1
        body, fields, k = text[start:j - 1], {}, 0
        for fm in re.finditer(r"([A-Za-z]+)\s*=\s*", body):
            if fm.start() < k: continue
            s = fm.end()
            if s >= len(body): break
            if body[s] == "{":
                d, e = 1, s + 1
                while d and e < len(body):
                    d += {"{": 1, "}": -1}.get(body[e], 0); e += 1
                val = body[s + 1:e - 1]
            else:
                e = body.find(",", s); e = len(body) if e < 0 else e
                val = body[s:e]
            fields[fm.group(1).lower()] = val.strip(); k = e
        fields["_type"] = mm.group(1).lower(); out[key] = fields
    return out


ACC = {"\\'": "\u0301", "\\`": "\u0300", '\\"': "\u0308", "\\^": "\u0302", "\\~": "\u0303", "\\v": "\u030c",
       "\\k": "\u0328", "\\c": "\u0327", "\\r": "\u030a", "\\.": "\u0307"}


def detex(s):
    import unicodedata
    s = s.replace("{\\l}", "ł").replace("{\\L}", "Ł").replace("{\\o}", "ø").replace("\\ss{}", "ß").replace("\\&", "&")
    s = s.replace("\\textdegree{}", "°").replace("$\\mu$", "µ").replace("$\\times$", "×").replace("\\_", "_").replace("\\,", " ").replace("~", " ")
    s = re.sub(r"\$_(\d)\$", lambda q: "₀₁₂₃₄₅₆₇₈₉"[int(q.group(1))], s)
    for cmd, comb in ACC.items():
        s = re.sub(re.escape(cmd) + r"\s*\{?\\?([A-Za-z])\}?", lambda q: unicodedata.normalize("NFC", q.group(1) + comb), s)
    s = s.replace("---", "—").replace("--", "–").replace("``", "“").replace("''", "”")
    s = re.sub(r"\\[A-Za-z]+\s?|\\ ", "", s)
    return re.sub(r"[{}]", "", s).strip()


def fmt_authors(a):
    names = []
    for n in re.split(r"\s+and\s+", a):
        n = detex(n)
        if "," in n:
            last, first = [x.strip() for x in n.split(",", 1)]
            n = f"{first} {last}"
        names.append(n)
    if len(names) > 4: return f"{names[0]} et al"
    return ", ".join(names[:-1]) + (" and " if len(names) > 1 else "") + names[-1]


BIBD = parse_bib(BIB)


def md_reference(n, key):
    f = BIBD[key]
    parts = []
    if f.get("author") or f.get("editor"): parts.append(fmt_authors(f.get("author") or f.get("editor")) + ".")
    parts.append(f"*{detex(f.get('title', key))}*.")
    venue = f.get("journal") or f.get("booktitle") or f.get("school") or f.get("publisher") or f.get("howpublished")
    if venue:
        v = detex(venue)
        if f.get("volume"): v += f" {detex(f['volume'])}"
        if f.get("pages"): v += f", {detex(f['pages'])}"
        parts.append(v + ".")
    if f.get("year") and f["year"] != "n.d.": parts.append(f"{f['year']}.")
    doi = f.get("doi"); url = f.get("url")
    if doi: parts.append(f"[doi:{doi}](https://doi.org/{doi})")
    elif url: parts.append(f"<{url}>")
    return f'{n}. <a id="ref-{key}"></a>' + " ".join(parts)


# ------------------------------------------------------------------ inline conversion
def split_math(s):
    return re.split(r"(\$[^$]+\$)", s)


def md_inline(s):
    s = CITE_RE.sub(lambda q: "[" + ", ".join(f"[{order.index(k) + 1}](#ref-{k})" for k in re.findall(r"@([\w:.-]+)", q.group(1))) + "]", s)

    def ref(q):
        kind, lab = q.groups()
        if kind == "sec":
            title = SECTITLE[f"sec:{lab}"]
            return f"the section “{title}”"
        return ("Figure " if kind == "fig" else "Table ") + str(NUM[f"{kind}:{lab}"])
    s = REF_RE.sub(ref, s)
    return re.sub(r"(?m)^the section", "The section", s)


TEXMAP = {"≈": "$\\approx$", "≤": "$\\leq$", "≥": "$\\geq$", "≫": "$\\gg$", "−": "$-$", "†": "\\textdagger{}", "₂": "\\textsubscript{2}",
          "³": "\\textsuperscript{3}", "²": "\\textsuperscript{2}", "→": "$\\rightarrow$", "“": "``", "”": "''", "µ": "\\textmu{}"}


def tex_text(s):
    hold = []

    def keep(x):
        hold.append(x); return f"\x00{len(hold) - 1}\x00"
    s = FN_RE.sub(lambda q: keep("\\footnote{" + tex_inline(FN[q.group(1)]) + "}"), s)
    s = re.sub(r"`([^`]+)`", lambda q: keep("\\texttt{" + q.group(1).replace("_", "\\_") + "}"), s)
    s = CITE_RE.sub(lambda q: keep("~\\citep{" + ",".join(re.findall(r"@([\w:.-]+)", q.group(1))) + "}"), s)
    s = REF_RE.sub(lambda q: keep({"fig": "Figure", "tbl": "Table", "sec": "Section"}[q.group(1)] + "~\\ref{" + q.group(1) + ":" + q.group(2) + "}"), s)
    s = s.replace("\\", "\\textbackslash{}")
    for ch in "%&#_":
        s = s.replace(ch, "\\" + ch)
    for a, b in TEXMAP.items():
        s = s.replace(a, b)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"\*(.+?)\*", r"\\emph{\1}", s)
    s = re.sub(r" \x00(\d+)\x00", lambda q: (hold[int(q.group(1))] if hold[int(q.group(1))].startswith("~") else " " + hold[int(q.group(1))]), s)
    s = re.sub(r"\x00(\d+)\x00", lambda q: hold[int(q.group(1))].lstrip("~"), s)
    return s


def tex_inline(s):
    return "".join(p if p.startswith("$") and p.endswith("$") and len(p) > 1 else tex_text(p) for p in split_math(s))


# ------------------------------------------------------------------ Markdown output
md = [f"# {META['title']}", "",
      f"**Created:** {META['created']}  ", f"**Updated:** {META['updated']}  ", f"**Generator:** {META['generator']}  ",
      *([f"**Updated by:** {META['updated_by']}"] if META.get('updated_by') else []), "",
      "**Original prompt:**", f"> {META['prompt']}", "",
      "**Context:**", "", f"- {META['context1']}", f"- {META['context2']}", "",
      f"**{META['subtitle']}**", "", META["author"] + ", " + META["date"], ""]
toc = [b for b in blocks if b[0] == "h" and b[1] == 1]
md += ["## Contents", ""] + [f"- [{b[2]}](#{re.sub(r'[^a-z0-9 -]', '', b[2].lower()).replace(' ', '-')})" for b in toc] + ["- [References](#references)", ""]
for b in blocks:
    if b[0] == "h": md += ["#" * (b[1] + 1) + " " + b[2], ""]
    elif b[0] == "p": md += [md_inline(b[1]), ""]
    elif b[0] == "fn": md += [f"[^{b[1]}]: " + md_inline(b[2]), ""]
    elif b[0] == "math": md += ["$$", b[1], "$$", ""]
    elif b[0] == "list":
        md += [(f"{n + 1}. " if b[1] else "- ") + md_inline(it) for n, it in enumerate(b[2])] + [""]
    elif b[0] == "fig":
        cap = md_inline(b[1]); alt = re.sub(r"\[\[?\d+\]?\([^)]*\)[^\]]*\]|[\[\]]", "", b[1])[:80]
        md += [f"![Figure {NUM[b[3]]}]({b[2]})", "", f"*Figure {NUM[b[3]]}. {cap}*", ""]
    elif b[0] == "tbl":
        md += [f"**Table {NUM[b[2]]}.** {md_inline(b[1])}", "", "| " + " | ".join(md_inline(c) for c in b[4]) + " |", "|" + "---|" * len(b[4])]
        md += ["| " + " | ".join(md_inline(c) for c in r) + " |" for r in b[5]] + [""]
md += ["## References", ""] + [md_reference(n + 1, k) for n, k in enumerate(order)] + [""]
(ROOT / f"{STEM}.md").write_text("\n".join(md), encoding="utf-8")

# ------------------------------------------------------------------ LaTeX output
PRE = r"""% Generated by scripts/build_summary.py from summary_master.md. Edit the master, not this file.
% Compile: tectonic -X compile glass_am_combined_summary.tex   (or xelatex + bibtex)
\documentclass[10pt,a4paper]{article}
\usepackage[margin=23mm,top=24mm,bottom=24mm]{geometry}
\usepackage{fontspec}
\usepackage{microtype}
\usepackage{amsmath,amssymb}
\usepackage{booktabs,longtable,array}
\usepackage{graphicx}
\usepackage{siunitx}
\usepackage{float}
\usepackage{xcolor}
\usepackage[font=small,labelfont=bf]{caption}
\usepackage[numbers,sort&compress]{natbib}
\usepackage{xurl}
\usepackage{enumitem}
\usepackage[colorlinks=true,linkcolor=blue!55!black,citecolor=green!40!black,urlcolor=blue!65!black]{hyperref}
\setlength{\parskip}{4pt plus 1pt}\setlength{\parindent}{0pt}
\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.15}
\setlist{leftmargin=*,itemsep=2pt,topsep=3pt}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\title{\textbf{TITLE}\\[4pt]\large SUBTITLE}
\author{\normalsize AUTHOR}
\date{DATE}
\begin{document}
\maketitle
\tableofcontents
\bigskip
"""
tex = [PRE.replace("SUBTITLE", tex_text(META["subtitle"])).replace("TITLE", tex_text(META["title"])).replace("AUTHOR", tex_text(META["author"])).replace("DATE", META["date"])]
for b in blocks:
    if b[0] == "h":
        cmd = ["section", "subsection", "subsubsection"][b[1] - 1]
        tex.append(f"\\{cmd}{{{tex_inline(b[2])}}}" + (f"\\label{{{b[3]}}}" if b[3] else "") + "\n")
    elif b[0] == "p": tex.append(tex_inline(b[1]) + "\n")
    elif b[0] == "math": tex.append("\\[ " + b[1] + " \\]\n")
    elif b[0] == "list":
        env = "enumerate" if b[1] else "itemize"
        tex.append(f"\\begin{{{env}}}\n" + "\n".join("  \\item " + tex_inline(it) for it in b[2]) + f"\n\\end{{{env}}}\n")
    elif b[0] == "fig":
        path = pathlib.Path(b[2]); pdf = path.with_suffix(".pdf")
        use = pdf if (ROOT / pdf).exists() else path
        tex.append("\\begin{figure}[H]\n  \\centering\n  \\includegraphics[width=%.2f\\linewidth]{%s}\n  \\caption{%s}\n  \\label{%s}\n\\end{figure}\n"
                   % (b[4], use.as_posix(), tex_inline(b[1]), b[3]))
    elif b[0] == "tbl":
        scale = 0.95 / max(sum(b[3]), 0.95) * (1 - 0.012 * len(b[3]))
        spec = "@{}" + "".join("L{%.3f\\linewidth}" % (w * scale) for w in b[3]) + "@{}"
        head = " & ".join("\\textbf{%s}" % tex_inline(c) if c else "" for c in b[4]) + " \\\\"
        rows = "\n".join("    " + " & ".join(tex_inline(c) for c in r) + " \\\\" for r in b[5])
        tex.append("{\\footnotesize\n\\begin{longtable}{%s}\n  \\caption{%s}\\label{%s}\\\\\n  \\toprule\n  %s\n  \\midrule\n  \\endfirsthead\n"
                   "  \\toprule\n  %s\n  \\midrule\n  \\endhead\n%s\n  \\bottomrule\n\\end{longtable}\n}\n" % (spec, tex_inline(b[1]), b[2], head, head, rows))
tex.append("\\bibliographystyle{unsrtnat}\n\\bibliography{references}\n\\end{document}\n")
(ROOT / f"{STEM}.tex").write_text("\n".join(tex), encoding="utf-8")
words = len(re.sub(r"[|#*$]", " ", BODY).split())
print(f"blocks {len(blocks)} | figures {nf} | tables {nt} | citations {len(order)} | words in master {words}")
