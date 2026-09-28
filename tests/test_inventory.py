import base64
import copy
import importlib.util
import io
import json
from pathlib import Path
import sys
import urllib.error

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from collect_inventory import CONTAINERS, collect, encode, validate
from propose_inventory import CHECKSUMS, TARGET, propose, updated_checksums


def sample():
    return dict(schema_version=1, scope='core-services', containers={
        name: dict(image_id='sha256:' + 'a' * 64, restart_policy='unless-stopped')
        for name in CONTAINERS})


def missing():
    return urllib.error.HTTPError('https://api.github.com', 404, 'missing', {}, io.BytesIO())


@pytest.mark.parametrize('mutation', [
    lambda v: v.update(extra='private data'),
    lambda v: v.update(scope='unapproved-host'),
    lambda v: v.update(schema_version=True),
    lambda v: v['containers'].pop('qdrant'),
    lambda v: v['containers']['qdrant'].update(environment='private data'),
    lambda v: v['containers']['qdrant'].update(image_id='private registry/name'),
    lambda v: v['containers']['qdrant'].update(restart_policy='secret'),
])
def test_reject_before_network(mutation):
    value = sample()
    mutation(value)
    with pytest.raises(ValueError):
        propose(lambda *args: pytest.fail('Network called before validation'), value)


def test_collect_projects_only_approved_fields():
    calls = []
    def run(args, **kwargs):
        calls.append(args)
        assert args[-1] in CONTAINERS
        assert args[-2] == '{{json .Image}} {{json .HostConfig.RestartPolicy.Name}}'
        return ('"sha256:' + 'a'*64 + '" "unless-stopped"\n').encode()
    assert collect(run) == sample()
    assert len(calls) == len(CONTAINERS)


def test_partial_capture_fails():
    def run(*args, **kwargs):
        raise RuntimeError('missing expected container')
    with pytest.raises(RuntimeError):
        collect(run)


def test_checksums_preserve_other_paths():
    old = 'b'*64 + '  README.md\n' + 'c'*64 + '  ' + TARGET + '\n'
    new = updated_checksums(old, encode(sample()))
    assert new.startswith('b'*64 + '  README.md\n')
    assert new.count(TARGET) == 1


class FakeAPI:
    def __init__(self, current=False, prior=False, pending=False, interrupted=False):
        self.calls = []
        self.current, self.prior, self.pending, self.interrupted = current, prior, pending, interrupted

    def __call__(self, method, path, body=None):
        self.calls.append((method, path, body))
        if method == 'GET':
            if path == 'git/ref/heads/main':
                return {'object': {'sha': 'b'*40}}
            if path.startswith('contents/' + TARGET):
                if self.current or (self.interrupted and '?ref=inventory/' in path):
                    return {'encoding': 'base64', 'content': base64.b64encode(encode(sample()).encode()).decode()}
                raise missing()
            if path.startswith('pulls?state=all'):
                return [{'number': 1}] if self.prior else []
            if path.startswith('pulls?state=open'):
                return [{'head': {'ref': 'inventory/older'}}] if self.pending else []
            if path.startswith('git/ref/heads/inventory/'):
                if self.interrupted:
                    return {'object': {'sha': 'c'*40}}
                raise missing()
            if path.startswith('contents/' + CHECKSUMS):
                return {'encoding': 'base64', 'content': base64.b64encode(('a'*64+'  README.md\n').encode()).decode()}
            if path.startswith('git/commits/'):
                return {'tree': {'sha': 'd'*40}}
        if method == 'POST':
            return {'sha': 'e'*40, 'number': 1}
        raise AssertionError((method, path))


@pytest.mark.parametrize('flag', ['current', 'prior', 'pending'])
def test_no_mutation_for_noop_or_review_pending(flag):
    api = FakeAPI(**{flag: True})
    propose(api, sample())
    assert all(method == 'GET' for method, _, _ in api.calls)


def test_new_proposal_only_writes_two_files_and_draft_branch():
    api = FakeAPI()
    propose(api, sample())
    mutations = [(path, body) for method, path, body in api.calls if method != 'GET']
    assert [p for p, _ in mutations] == ['git/trees', 'git/commits', 'git/refs', 'pulls']
    assert {v['path'] for v in mutations[0][1]['tree']} == {TARGET, CHECKSUMS}
    assert mutations[2][1]['ref'].startswith('refs/heads/inventory/')
    assert mutations[3][1]['draft'] is True
    assert mutations[3][1]['base'] == 'main'


def test_resume_branch_without_overwrite():
    api = FakeAPI(interrupted=True)
    propose(api, sample())
    assert [p for m, p, _ in api.calls if m != 'GET'] == ['pulls']
