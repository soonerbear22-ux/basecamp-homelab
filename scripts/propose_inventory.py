"""Propose a validated inventory through a draft PR; never write main or merge.

Use a repository-scoped GitHub credential file outside the checkout. No shell,
checkout hooks, downloaded scripts or repository code are executed by this tool.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import urllib.error
import urllib.request

from collect_inventory import encode, validate

REPO = 'soonerbear22-ux/basecamp-homelab'
TARGET = 'inventory/core-services.json'
CHECKSUMS = 'release/CHECKSUMS.sha256'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError('Redirect refused')


class GitHub:
    def __init__(self, credential):
        self.credential = credential
        self.opener = urllib.request.build_opener(NoRedirect())

    def __call__(self, method, path, body=None):
        request = urllib.request.Request(
            'https://api.github.com/repos/' + REPO + '/' + path,
            data=None if body is None else json.dumps(body).encode(), method=method,
            headers={'Authorization': 'Bearer ' + self.credential,
                     'Accept': 'application/vnd.github+json',
                     'Content-Type': 'application/json',
                     'User-Agent': 'basecamp-inventory',
                     'X-GitHub-Api-Version': '2026-03-10'})
        with self.opener.open(request, timeout=30) as response:
            return json.load(response)


def get_file(api, path, ref):
    result = api('GET', 'contents/' + path + '?ref=' + ref)
    if result.get('encoding') != 'base64':
        raise ValueError('Unexpected content encoding')
    return base64.b64decode(result['content']).decode('utf-8')


def updated_checksums(text, content):
    entries = {}
    for line in text.splitlines():
        match = re.fullmatch(r'([a-f0-9]{64})  ([^\r\n]+)', line)
        if not match or match[2] in entries:
            raise ValueError('Invalid checksum manifest')
        entries[match[2]] = match[1]
    entries[TARGET] = hashlib.sha256(content.encode()).hexdigest()
    return ''.join(entries[path] + '  ' + path + '\n' for path in sorted(entries))


def propose(api, value):
    # Complete schema validation occurs before even the first network request.
    content = encode(validate(value))
    base = api('GET', 'git/ref/heads/main')['object']['sha']
    try:
        previous = get_file(api, TARGET, base)
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise
        previous = None
    if previous == content:
        return 'No change; no publication.'
    digest = hashlib.sha256(content.encode()).hexdigest()
    branch = 'inventory/' + digest
    # Content-addressed branches deliberately avoid overwriting human edits.
    # Include closed PRs: declined proposals must not reopen on every timer run.
    existing = api('GET', 'pulls?state=all&head=soonerbear22-ux:' + branch + '&per_page=100')
    if existing:
        return 'This observation already has a proposal; no mutation.'
    open_prs = api('GET', 'pulls?state=open&per_page=100')
    if len(open_prs) == 100 or any(p['head']['ref'].startswith('inventory/') for p in open_prs):
        return 'An inventory proposal awaits review; latest observation retained locally.'
    try:
        api('GET', 'git/ref/heads/' + branch)
        branch_exists = True
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise
        branch_exists = False
    if branch_exists:
        # Resume after a successful branch write but failed PR creation only
        # when the already published payload matches exactly.
        if get_file(api, TARGET, branch) != content:
            raise ValueError('Existing branch changed; review required')
    else:
        checksums = updated_checksums(get_file(api, CHECKSUMS, base), content)
        base_tree = api('GET', 'git/commits/' + base)['tree']['sha']
        tree = api('POST', 'git/trees', {'base_tree': base_tree, 'tree': [
            {'path': path, 'mode': '100644', 'type': 'blob', 'content': data}
            for path, data in ((TARGET, content), (CHECKSUMS, checksums))]})
        commit = api('POST', 'git/commits', {
            'message': 'Propose observed core container inventory',
            'tree': tree['sha'], 'parents': [base]})
        api('POST', 'git/refs', {'ref': 'refs/heads/' + branch, 'sha': commit['sha']})
    api('POST', 'pulls', {
        'title': 'Review observed core container inventory', 'head': branch,
        'base': 'main', 'draft': True,
        'body': 'Automated observation of allowlisted image IDs and restart policies. '
                'Review the diff and repository checks before merging. This does not '
                'update V1 pins or prove runtime health. Physical moves and incident '
                'resolutions require separate operator notes. If main changed, resolve '
                'the checksum manifest against current main before merging.'})
    return 'Draft inventory proposal created; main unchanged.'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--credential-file', type=Path)
    args = parser.parse_args()
    try:
        value = validate(json.loads(args.inventory.read_text(encoding='utf-8')))
        if args.credential_file is None:
            print('Inventory valid. Dry run only; no network requests.')
            return
        info = args.credential_file.lstat()
        if not stat.S_ISREG(info.st_mode) or (os.name == 'posix' and (
                info.st_mode & 0o077 or info.st_uid != os.geteuid())):
            raise ValueError('Credential must be an owner-only regular file')
        credential = args.credential_file.read_text().strip()
        if not credential or any(c.isspace() for c in credential):
            raise ValueError('Invalid credential')
        print(propose(GitHub(credential), value))
    except Exception:
        raise SystemExit('Proposal failed; inspect configuration privately. No automatic merge was attempted.') from None


if __name__ == '__main__':
    main()
