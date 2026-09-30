import requests, re, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) glass-am-harvester"
def save(url, dest):
    r = S.get(url, timeout=120, allow_redirects=True)
    if r.ok and r.content.startswith(b"%PDF"):
        dest.write_bytes(r.content); print("OK  ", dest.name, len(r.content)); return True
    print("FAIL", dest.name, r.status_code, r.content[:60]); return False
def dspace7(base, query, dest):
  try:
      r = S.get(f"{base}/server/api/discover/search/objects", params={"query": query, "size": 3}, timeout=60)
      objs = r.json()["_embedded"]["searchResult"]["_embedded"]["objects"]
      for o in objs:
          item = o["_embedded"]["indexableObject"]; name = item.get("name"); uuid = item["uuid"]
          print("  item:", name)
          b = S.get(f"{base}/server/api/core/items/{uuid}/bundles", timeout=60).json()
          for bundle in b["_embedded"]["bundles"]:
              if bundle["name"] != "ORIGINAL": continue
              bs = S.get(bundle["_links"]["bitstreams"]["href"], timeout=60).json()
              for bit in bs["_embedded"]["bitstreams"]:
                  print("   bitstream:", bit["name"])
                  if bit["name"].lower().endswith(".pdf"):
                      return save(f"{base}/server/api/core/bitstreams/{bit['uuid']}/content", dest)
      return False
  except Exception as e:
    print('DSPACE ERROR', base, e); return False
P = ROOT/"sources"/"papers"; M = ROOT/"sources"/"media"
dspace7("https://dspace.mit.edu", "Additive Manufacturing of Optically Transparent Glass Klein", P/"2015_Klein_Additive_Manufacturing_of_Optically_Transparent_Glass.pdf")
dspace7("https://dspace.mit.edu", "Additive Manufacturing of Transparent Glass Structures Inamura", P/"2018_Inamura_Additive_Manufacturing_of_Transparent_Glass_Structures.pdf")
dspace7("https://repositories.lib.utexas.edu", "Fiber-Fed Printing of Free-Form Free-Standing Glass Structures", P/"2018_Hostetler_Fiber_fed_printing_free_form_free_standing_glass_SFF.pdf")
dspace7("https://repositories.lib.utexas.edu", "Processability of soda-lime glass in laser-based powder bed fusion", P/"2020_SFF_Processability_of_soda_lime_glass_in_LPBF.pdf")
for u, d in [("https://pmc.ncbi.nlm.nih.gov/articles/PMC5379039/pdf/rsta20160156.pdf", P/"2017_Brun_The_molten_glass_sewing_machine.pdf"),
             ("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5379039/pdf/rsta20160156.pdf", P/"2017_Brun_The_molten_glass_sewing_machine.pdf"),
             ("https://pmc.ncbi.nlm.nih.gov/articles/PMC8655167/pdf/ADVS-8-2103180.pdf", P/"2021_Mader_Melt_extrusion_AM_transparent_fused_silica.pdf")]:
    if not d.exists(): save(u, d)
# Wikimedia Commons media + license
for title in ["File:Caustic patterns of a 3D printed glass structure.jpg", "File:Matter-glass-printer.webm", "File:GLASS II - Mediated Matter.webm"]:
    r = S.get("https://commons.wikimedia.org/w/api.php", params={"action":"query","titles":title,"prop":"imageinfo","iiprop":"url|extmetadata|size","format":"json"}, timeout=60).json()
    for pg in r["query"]["pages"].values():
        ii = pg["imageinfo"][0]; em = ii.get("extmetadata", {})
        lic = em.get("LicenseShortName", {}).get("value"); artist = re.sub("<[^>]+>", "", em.get("Artist", {}).get("value", ""))
        print("COMMONS", title, "|", lic, "|", artist, "|", ii["url"], "|", ii.get("size"))
        (M/"commons_media_licenses.txt").open("a", encoding="utf-8").write(f"{title}\t{lic}\t{artist}\t{ii['url']}\t{em.get('Credit',{}).get('value','')}\n")
        if ii["size"] < 60_000_000:
            fn = M / re.sub(r"[^A-Za-z0-9_.-]+", "_", title.replace("File:", ""))
            rr = S.get(ii["url"], timeout=300); fn.write_bytes(rr.content); print("   saved", fn.name, len(rr.content))
# extra BibTeX via doi.org + Crossref lookup for PGM paper
B = ROOT/"sources"/"data"/"bibtex_raw"
for key, doi in [("dgf2026control","10.1016/j.addma.2026.105306"), ("lgd2025tempctrl","10.3390/mi16010029")]:
    r = S.get(f"https://doi.org/{doi}", headers={"Accept":"application/x-bibtex"}, timeout=60)
    if r.ok and r.text.startswith("@"): (B/f"{key}.bib").write_text(r.text, encoding="utf-8"); print("BIB", key)
r = S.get("https://api.crossref.org/works", params={"query.title":"Platinum Group Metals in Glass Making","rows":3}, timeout=60).json()
for it in r["message"]["items"]: print("CROSSREF", it.get("DOI"), "|", it.get("title"), "|", it.get("container-title"), it.get("issued"))
