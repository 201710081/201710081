"""Fail closed on non-public files and unmasked content in Git snapshots."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata

POLICY = json.loads(Path(__file__).with_name('privacy_policy.json').read_text(encoding='utf-8'))
INFRA = {'.gitignore', '.gitattributes', '.githooks/pre-commit', '.githooks/pre-push',
         '.githooks/run-privacy-check', 'scripts/privacy_guard.py', 'scripts/privacy_policy.json',
         'scripts/install-hooks.ps1', 'tests/test_privacy_guard.py', '.github/workflows/privacy.yml'}
SENSITIVE = [
    ('email', r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}'),
    ('phone', r'01[016789][- .]?\d{3,4}[- .]?\d{4}'),
    ('token', r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16}|sk-[A-Za-z0-9_-]{20,})'),
    ('credential', r'(?i)(?:password|passwd|api[_-]?key|access[_-]?token|비밀번호)\s*[:=]\s*["\']?[^\s"\'\[<]{4,}'),
    ('internal-location', r'(?i)(?:s3://|[A-Z]:[\\/]Users[\\/]|https?://[^\s/]*(?:salesforce\.com|force\.com)|BEGIN .*PRIVATE KEY)'),
    ('embedded-payload', r'(?i)(?:data:[^\s]*;base64|[A-Za-z0-9+/]{100,}={0,2})'),
]

def check_blob(name, data, mode='100644'):
    errors = []
    if mode not in {'100644', '100755'}:
        return ['non-regular file']
    if name in POLICY['reviewed_assets']:
        return [] if hashlib.sha256(data).hexdigest() == POLICY['reviewed_assets'][name] else ['image requires masking and manual review']
    path = PurePosixPath(name)
    if name not in INFRA and not (name == 'README.md' or (name.startswith('docs/') and path.suffix == '.md')):
        return ['file type/path is not approved for publication']
    if set(x.lower() for x in path.parts) & {'data','raw','private','원본','비공개데이터','90_비공개데이터'}:
        return ['private data directory']
    if len(data) > 500_000 or b'\x00' in data or data.startswith((b'PK\x03\x04', b'%PDF', b'\x89PNG')):
        return ['binary, archive or oversized payload']
    try:
        text = unicodedata.normalize('NFKC', data.decode('utf-8-sig'))
    except UnicodeDecodeError:
        return ['not UTF-8 text']
    # Only these exact, reviewable infrastructure files contain test fixtures/code.
    if name in INFRA:
        return []
    for line_no, line in enumerate(text.splitlines(), 1):
        for label, pattern in SENSITIVE:
            if re.search(pattern, line):
                errors.append(f'line {line_no}: {label}')
        probe = line
        for url in sorted(POLICY['existing_public_urls'], key=len, reverse=True):
            probe = probe.replace(url, '')
        for internal_path in INFRA:
            probe = probe.replace(internal_path, '')
        # Career/project dates, section numbering and product names are public metadata.
        probe = re.sub(r'\b(?:19|20)\d{2}[.-](?:0?[1-9]|1[0-2])(?:[.-](?:0?[1-9]|[12]\d|3[01]))?(?!\d)', '', probe)
        probe = re.sub(r'(?:19|20)\d{2}년\s*(?:[1-9]|1[0-2])월', '', probe)
        probe = re.sub(r'(?i)(?<![A-Za-z0-9])(?:S3|B2B|B2C|Cafe24(?:TW)?|Qoo10)(?![A-Za-z0-9])', '', probe)
        probe = re.sub(r'^\s*(?:#{1,6}\s*)?\d+\s*[.·]\s+', '', probe)
        probe = re.sub(r'(?<=>)0[1-9] · ', '', probe)
        probe = re.sub(r'(?<=\*\*)0[1-9] · ', '', probe)
        probe = re.sub(r'(</?h)[1-6](?=[ >])', r'\1', probe)
        probe = re.sub(r'\bwidth="\d+%?"', '', probe)
        # Existing career badges are credentials about the author, not client metrics.
        probe = probe.replace('4년 차', '').replace('15건 이상', '')
        probe = probe.replace('사용자 매뉴얼 24~25쪽 발췌', '사용자 매뉴얼 발췌')
        if re.search(r'\d|[일이삼사오육칠팔구십백천만억조]+\s*(?:퍼센트|억원|만원)', probe):
            errors.append(f'line {line_no}: unmasked number')
    return errors

def git(*args, cwd=None):
    return subprocess.run(['git', *args], cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

def check_snapshot(ref='INDEX', cwd=None):
    raw = git('ls-files', '--stage', '-z', cwd=cwd) if ref == 'INDEX' else git('ls-tree', '-r', '-z', ref, cwd=cwd)
    errors = []
    for record in raw.split(b'\0'):
        if not record:
            continue
        meta, raw_name = record.split(b'\t', 1)
        fields = meta.decode().split()
        mode, sha = (fields[0], fields[1]) if ref == 'INDEX' else (fields[0], fields[2])
        name = raw_name.decode('utf-8')
        if ref == 'INDEX' and fields[2] != '0':
            errors.append(f'{name}: unresolved merge'); continue
        if mode == '160000':
            errors.append(f'{name}: submodules are not allowed'); continue
        for error in check_blob(name, git('cat-file', 'blob', sha, cwd=cwd), mode):
            errors.append(f'{name}: {error}')
    return errors

def check_range(base, tip, cwd=None, remote='origin'):
    args = ['rev-list', '--reverse', tip]
    if base and set(base) != {'0'}:
        args.append('^'+base)
    else:
        args.extend(['--not', '--remotes='+remote])
    commits = git(*args, cwd=cwd).decode().splitlines()
    errors = []
    for sha in commits:
        errors.extend(f'{sha[:8]}: {e}' for e in check_snapshot(sha, cwd))
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--staged', action='store_true')
    parser.add_argument('--snapshot')
    parser.add_argument('--range', nargs=2, dest='revision_range')
    parser.add_argument('--pre-push', action='store_true')
    parser.add_argument('--remote', default='origin')
    args = parser.parse_args()
    try:
        if args.pre_push:
            errors = []
            for line in sys.stdin:
                local_ref, local_sha, remote_ref, remote_sha = line.split()
                if set(local_sha) != {'0'}:
                    errors.extend(check_range(remote_sha, local_sha, remote=args.remote))
        elif args.revision_range:
            errors = check_range(*args.revision_range)
        else:
            errors = check_snapshot(args.snapshot or 'INDEX')
    except (subprocess.CalledProcessError, ValueError, OSError) as exc:
        print('Privacy check could not finish; publication blocked ('+type(exc).__name__+').', file=sys.stderr)
        return 1
    if errors:
        print('Publication blocked. Mask numbers or remove private files from Git:', file=sys.stderr)
        print('\n'.join(errors[:80]), file=sys.stderr)
        return 1
    print('Privacy check passed: only approved publication files.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
