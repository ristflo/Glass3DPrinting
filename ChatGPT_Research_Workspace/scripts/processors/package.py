"""Build a portable research archive, inventory its files, and verify every byte.

Run after integrate.py, build.ps1, verify.py and inspect_pdf.py. The archive
receipt is external because it contains the archive's own hash.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'artifacts/MANIFEST.json'
ARCHIVE = ROOT / 'output/glass_3d_printing_report.zip'
RECEIPT = ROOT / 'artifacts/package_validation.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def included_files():
    result = []
    for path in ROOT.rglob('*'):
        rel = path.relative_to(ROOT)
        if rel.parts[:2] == ('scripts', 'tmp') or '__pycache__' in rel.parts:
            continue
        if path in (ARCHIVE, RECEIPT) or path.suffix.lower() in ('.pyc', '.zip'):
            continue
        if path.is_file():
            if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
                raise RuntimeError(f'Unsafe archive path: {rel}')
            result.append(path)
    return sorted(result)


def main():
    validation = json.loads((ROOT / 'artifacts/validation.json').read_text(encoding='utf-8'))
    inspection = json.loads((ROOT / 'artifacts/pdf_inspection.json').read_text(encoding='utf-8'))
    for field in ('undefined_citations', 'missing_metadata', 'missing_figures', 'asset_errors', 'hash_errors'):
        if validation[field]:
            raise RuntimeError(f'Unresolved validation errors: {field}')
    if inspection['undefined_reference_warning']:
        raise RuntimeError('Unresolved PDF references')
    if inspection['pdf_sha256'] != digest(ROOT / 'output/glass_3d_printing_sota_monograph.pdf'):
        raise RuntimeError('PDF changed since inspection; rerun inspect_pdf.py')
    for rel in ('artifacts/VERIFICATION_WALKTHROUGH.md', 'output/executive_summary.md',
                'output/master_source_index.csv', 'README.md'):
        if not (ROOT / rel).is_file():
            raise RuntimeError(f'Missing deliverable: {rel}')
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    files = included_files()
    inventory = [{'path':p.relative_to(ROOT).as_posix(), 'bytes':p.stat().st_size,
                  'sha256':digest(p)} for p in files if p != MANIFEST]
    manifest['file_inventory'] = inventory
    manifest['packaged_at_utc'] = datetime.now(timezone.utc).isoformat()
    manifest['inventory_note'] = ('All packaged files except MANIFEST.json itself. '
        'Archive excludes scripts/tmp, __pycache__, ZIP files and the external '
        'artifacts/package_validation.json receipt, which hashes the final ZIP.')
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    with zipfile.ZipFile(ARCHIVE, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in files:
            archive.write(path, path.relative_to(ROOT).as_posix())
    expected = {p.relative_to(ROOT).as_posix():digest(p) for p in files}
    with zipfile.ZipFile(ARCHIVE) as archive:
        corrupt = archive.testzip()
        if corrupt:
            raise RuntimeError(f'ZIP CRC failure: {corrupt}')
        if len(archive.namelist()) != len(expected) or set(archive.namelist()) != set(expected):
            raise RuntimeError('Archive membership mismatch')
        for name, sha in expected.items():
            if hashlib.sha256(archive.read(name)).hexdigest() != sha:
                raise RuntimeError(f'Archived file hash mismatch: {name}')
    result = {'verified_at_utc':datetime.now(timezone.utc).isoformat(),
              'archive':ARCHIVE.relative_to(ROOT).as_posix(), 'files':len(files),
              'bytes':ARCHIVE.stat().st_size, 'sha256':digest(ARCHIVE),
              'crc_check':'passed', 'all_member_sha256_checks':'passed',
              'workspace_relative_paths':True, 'excluded_scratch_and_tooling':True,
              'manifest_sha256':digest(MANIFEST)}
    RECEIPT.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
