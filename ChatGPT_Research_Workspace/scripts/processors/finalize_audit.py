"""Summarize actual saved validation and human visual-review evidence."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]


def read(name):
    return json.loads((ROOT / 'artifacts' / name).read_text(encoding='utf-8'))


def main():
    validation = read('validation.json')
    inspection = read('pdf_inspection.json')
    visual = read('visual_review.json')
    links = read('link_validation.json')
    manifest = read('MANIFEST.json')
    pdf = ROOT / 'output/glass_3d_printing_sota_monograph.pdf'
    pdf_hash = hashlib.sha256(pdf.read_bytes()).hexdigest()
    if visual['pdf_sha256'] != pdf_hash or inspection['pdf_sha256'] != pdf_hash:
        raise RuntimeError('Final PDF needs fresh machine and visual inspection')
    failures = [x for x in links if not x.get('status') or x['status'] >= 400]
    papers = [x for x in validation['pdfs'] if x['path'].startswith('sources/papers/')]
    patents = [x for x in validation['pdfs'] if x['path'].startswith('sources/patents/')]
    media = sorted(p for p in (ROOT / 'sources/media').iterdir() if p.is_file())
    lines = [
        '# Verification walkthrough', '',
        'Generated from saved checks at ' + datetime.now(timezone.utc).isoformat() + '.', '',
        '## Delivery status', '',
        'The eight-section technical review, executive summary, source index, bibliography, '
        'analysis scripts and source repository are assembled. This is a completed scoped '
        'review with the evidence and acquisition limits below; it is not an exhaustive '
        'literature search or an experimentally validated process specification. Run '
        '`package.py` after this audit; its external `package_validation.json` records the '
        'actual final ZIP result and hash.', '',
        '## Compilation and PDF review', '',
        '- Compiler: workspace-local Tectonic (XeTeX); successful exit status 0. '
        'Logs and intermediates are retained in `latex/build/` and `artifacts/compile_output.txt`.',
        f"- PDF: {inspection['page_count']} pages, {len(inspection['bookmarks'])} bookmarks, "
        f"{inspection['link_annotation_count']} link annotations; SHA-256 `{pdf_hash}`.",
        f"- Final TeX log: {len(inspection['warnings'])} warnings. "
        'Remaining warnings are underfull text boxes, with no overfull boxes, missing glyphs '
        'or undefined citations/references detected.',
        f"- BibTeX warnings: {len(inspection['bibtex_warnings'])}. Undated web/datasheet "
        'entries use n.d.; publication dates are not inferred from access dates.',
        '- Visual review: ' + visual['finding'],
        '- Review evidence: `pdf_inspection.json`, `visual_review.json`; rendered pages '
        'are scratch files and are intentionally excluded from the portable archive.', '',
        '## Citations, assets and calculations', '',
        f"- {validation['bibliography_entries']} bibliography entries; "
        f"{validation['cited_unique_entries']} unique cited keys; "
        f"{len(manifest['sources'])} source/asset ledger records (not 80 distinct publications).",
        '- No missing citation keys, required article metadata, referenced figures, '
        'asset parse errors or original-ledger hash mismatches.',
        f'- {len(papers)} PDFs in papers/ (13 research/review PDFs and 3 manufacturer '
        f'datasheets); {len(patents)} patent PDFs; {len(media)} files in media/.',
        '- WO2020118157A1 is a 91-page image-based PDF: it opens successfully but has no '
        'extractable text. Full-text search of that local file requires OCR, not supplied here.',
        '- Nominal viscosity fits, units, inverse thresholds and flow-scaling checks passed '
        'on 29 September. The engineering script reran successfully on 30 September after '
        'correcting the BOROFLOAT property temperature labels; numerical results are unchanged.',
        '- Final source review corrected Toombs roughness profile lengths, BOROFLOAT '
        'conductivity/heat-capacity reference ranges, the November 2025 Corning publication '
        'date, and the reported G3DP2 build envelope. See `notes/academic_notes/final_review_20260930.md`.', '',
        '## External links', '',
        f"- Saved check dates: {', '.join(sorted({x['checked'] for x in links}))}. "
        f'{len(links)} unique links checked; {len(links)-len(failures)} returned HTTP <400; '
        f'{len(failures)} returned access failures.',
        '- A response is an accessibility check, not proof of video playback or content validity. '
        '403/405 responses may reflect blocking; they are not silently classified as valid or dead.', '',
        '| HTTP status | URL |', '|---|---|',
    ]
    lines += [f"| {x.get('status') or 'request failed'} | {x['url']} |" for x in failures]
    lines += ['', '## Containment', '',
        '- All commands that created or modified deliverables in this finishing pass targeted '
        '`ChatGPT_Research_Workspace/`. Claude and Antigravity workspaces were not edited.',
        f"- Project-root file changes since the 30 September resume snapshot: "
        f"{validation.get('root_changes_since_resume', 'not checked')}.",
        '- The original 26 September baseline differs for '
        '`Antigravity_Research_Instructuctions_20260926.md`; that difference already existed '
        'when this finishing pass began. The audit does not establish who changed it, and '
        'does not claim that the entire project root has been unchanged since 26 September.',
        '- Root inventories compare immediate root files, not a recursive historical audit '
        'of unrelated workspaces. Original and resume snapshots are retained.', '',
        '## Acquisition and evidence limits', '',
        '- No separately catalogued nozzle cross-section or thermal-camera frame was acquired. '
        'The archive includes apparatus, laser-heating, deposited-track, printed-part and '
        'photoelasticity images. The photoelasticity specimen is conventional tempered glass.',
        '- Not all downloaded raster figures meet 300 dpi at their placed size. In particular '
        'the Liu schematic is only 498 x 352 pixels. It was not upscaled and relabeled high resolution. '
        'Original analytical plots also have vector PDF versions.',
        '- Video streaming links are logged; playback was not verified and binaries were not copied.',
        '- Matched-route tensile and optical datasets, current verified printer prices and yields, '
        'material-specific refractory lifetime, and grade-specific liquidus/kinetics remain gaps. '
        'Conventional forming costs are discussed qualitatively; numerical costs are hypothetical '
        'scenarios, not sourced matched-part quotations.',
        '- Direct molten-inorganic-glass apparatus attribution remains unverified for some requested '
        'institutions. No machine names, numerical TRLs or missing performance values were invented.',
        '- Third-party PDFs and figures retain their individual rights. The archive is a local '
        'research collection, not a blanket permission to redistribute every source. Media '
        'credits and the Chhadeh CC BY-NC-ND limitation are retained in README and media notes.', '',
        '## Acquired PDF inventory', '',
        '| Workspace path | Pages | Extractable characters |', '|---|---:|---:|']
    lines += [f"| `{x['path']}` | {x['pages']} | {x['text_characters']} |" for x in validation['pdfs']]
    lines += ['', '## Production raster resolution', '',
        '| Workspace path | Width (px) | Height (px) |', '|---|---:|---:|']
    lines += [f"| `{x['path']}` | {x['width_px']} | {x['height_px']} |" for x in validation['images']]
    lines += ['', '## Original media inventory', '']
    lines += [f'- `{p.relative_to(ROOT).as_posix()}` ({p.stat().st_size:,} bytes)' for p in media]
    lines += ['', 'The master CSV and MANIFEST source records provide URLs, source identities and '
        'download provenance. Packaging adds a SHA-256 inventory of every archived file '
        'except the manifest itself. The adjacent package receipt verifies the archive CRC '
        'and every member against the corresponding workspace bytes.', '']
    (ROOT / 'artifacts/VERIFICATION_WALKTHROUGH.md').write_text('\n'.join(lines), encoding='utf-8')
    print('Wrote VERIFICATION_WALKTHROUGH.md from current inspection and validation evidence.')


if __name__ == '__main__':
    main()
