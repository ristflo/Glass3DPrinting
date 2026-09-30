#!/usr/bin/env python
"""normalize_manifest_paths.py - make every local path in sources/manifest.json use forward slashes."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
p = ROOT / "sources" / "manifest.json"
mf = json.loads(p.read_text(encoding="utf-8"))
n = 0
def fix(rec):
    global n
    for k in ("local_path", "bibtex_path"):
        v = rec.get(k)
        if isinstance(v, str) and "\\" in v:
            rec[k] = v.replace("\\", "/"); n += 1
for section in ("papers", "patents", "media", "figures", "deliverables"):
    for rec in mf.get(section, []):
        fix(rec)
p.write_text(json.dumps(mf, indent=1, ensure_ascii=False), encoding="utf-8")
s = p.read_text(encoding="utf-8")
print("paths normalized:", n, "| backslashes remaining in file:", s.count("\\\\"))
missing = [r["local_path"] for sec in ("papers", "patents", "media", "figures", "deliverables") for r in mf.get(sec, []) if r.get("local_path") and not (ROOT / r["local_path"]).exists()]
print("manifest paths that do not exist on disk:", missing if missing else "none")
