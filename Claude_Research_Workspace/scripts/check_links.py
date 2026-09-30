#!/usr/bin/env python
"""check_links.py - validates every URL and DOI in latex/references.bib and every \\href in the sections.
Writes sources/data/link_check.csv. Uses only the standard library (urllib)."""
import re, pathlib, csv, ssl, urllib.request, urllib.error, socket, time
ROOT = pathlib.Path(__file__).resolve().parent.parent
bib = (ROOT / "latex" / "references.bib").read_text(encoding="utf-8")
urls = set(re.findall(r"url\s*=\s*\{([^}]+)\}", bib, flags=re.I))
dois = set(re.findall(r"doi\s*=\s*\{([^}]+)\}", bib, flags=re.I))
for tex in (ROOT / "latex" / "sections").glob("*.tex"):
    urls.update(re.findall(r"\\href\{([^}]+)\}", tex.read_text(encoding="utf-8")))
targets = sorted(urls | {f"https://doi.org/{d}" for d in dois})
ctx = ssl.create_default_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) glass-am-link-checker/1.0"
rows = []
def probe(u):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(u, method=method, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
                return r.status, r.geturl()
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 400, 500, 501):
                continue
            return e.code, u
        except (urllib.error.URLError, socket.timeout, ssl.SSLError, ConnectionError, OSError) as e:
            if method == "HEAD":
                continue
            return f"ERR {type(e).__name__}", u
    return "ERR", u
for u in targets:
    code, final = probe(u)
    verdict = "ok" if isinstance(code, int) and code < 400 else ("blocked-bot(403)" if code == 403 else "check")
    rows.append((u, code, verdict, final))
    print(f"{str(code):>8}  {verdict:<16} {u}")
    time.sleep(0.2)
out = ROOT / "sources" / "data" / "link_check.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["url", "status", "verdict", "final_url"]); w.writerows(rows)
ok = sum(1 for r in rows if r[2] == "ok"); blocked = sum(1 for r in rows if r[2].startswith("blocked")); bad = len(rows) - ok - blocked
print(f"\nSUMMARY: {len(rows)} targets, {ok} ok, {blocked} bot-blocked (403), {bad} need review -> {out}")
