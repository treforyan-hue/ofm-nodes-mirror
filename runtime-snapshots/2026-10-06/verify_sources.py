"""Verify complete pinned source snapshots; optionally restore to a new Linux root."""
import argparse
import hashlib
import io
import json
import os
import tarfile
from pathlib import Path, PurePosixPath

parser = argparse.ArgumentParser()
parser.add_argument('--snapshot', type=Path, default=Path(__file__).resolve().parent)
parser.add_argument('--restore', type=Path, help='Explicit Linux-only restore into a new, empty absolute directory')
args = parser.parse_args()
snapshot = args.snapshot.resolve()
manifest = json.loads((snapshot/'sources.lock.json').read_text(encoding='utf-8'))
if args.restore is not None:
    if os.name != 'posix' or not args.restore.is_absolute():
        raise SystemExit('Restore is allowed only to an absolute directory on a Linux build/test host.')
    target = args.restore.resolve()
    if target == Path('/') or (target.exists() and any(target.iterdir())):
        raise SystemExit('Restore requires a new or empty directory; existing runtime is never overwritten.')
    target.mkdir(parents=True, exist_ok=True)

verified_files = 0
for entry in manifest['packages']:
    compressed = io.BytesIO()
    archive_hash = hashlib.sha256()
    for record in entry['parts']:
        part = (snapshot/record['path']).resolve()
        if not part.is_relative_to(snapshot): raise RuntimeError('Archive part escapes snapshot')
        data = part.read_bytes()
        if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
            raise RuntimeError('Archive part checksum mismatch: '+record['path'])
        archive_hash.update(data); compressed.write(data)
    if compressed.tell() != entry['bytes'] or archive_hash.hexdigest() != entry['sha256']:
        raise RuntimeError('Complete archive mismatch: '+entry['archive'])
    compressed.seek(0)
    expected = {r['path']:r for r in entry['files']}
    seen = set()
    key = PurePosixPath(entry['directory'])
    if str(key) == 'core': package = Path('.')
    elif len(key.parts) == 2 and key.parts[0] == 'nodes': package = Path('custom_nodes')/key.parts[1]
    else: raise RuntimeError('Unsupported source package layout')
    with tarfile.open(fileobj=compressed, mode='r:gz') as tar:
        for member in tar:
            relative = PurePosixPath(member.name)
            if not member.isfile() or relative.is_absolute() or '..' in relative.parts or member.name not in expected or member.name in seen:
                raise RuntimeError('Unsafe/unexpected source archive member')
            data = tar.extractfile(member).read()
            record = expected[member.name]
            if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
                raise RuntimeError('Source file mismatch: '+member.name)
            seen.add(member.name); verified_files += 1
            if args.restore is not None:
                file = (target/package/Path(*relative.parts)).resolve()
                if not file.is_relative_to(target): raise RuntimeError('Restore destination escapes target')
                file.parent.mkdir(parents=True, exist_ok=True)
                with file.open('xb') as out: out.write(data)
                file.chmod(member.mode & 0o777)
    if seen != expected.keys(): raise RuntimeError('Source archive omits declared files')
print(json.dumps({'packages':len(manifest['packages']),'source_files':verified_files,'verified':True,'restored':args.restore is not None}))
