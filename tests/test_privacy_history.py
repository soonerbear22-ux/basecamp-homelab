"""Publication regressions for exact H16 history dispositions."""
import importlib.util
import json
from pathlib import Path
import subprocess

import pytest


@pytest.fixture
def validator():
    path = Path(__file__).resolve().parents[1] / "scripts/validate_repository.py"
    spec = importlib.util.spec_from_file_location("privacy_validator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def history(tmp_path, validator):
    validator.ROOT = tmp_path
    def git(*args):
        return subprocess.check_output(["git", "-C", str(tmp_path), *args]).decode().strip()
    git("init", "-q")
    git("config", "user.name", "Privacy tests")
    git("config", "user.email", "privacy@example.invalid")
    def commit(path, content):
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        git("add", path)
        git("commit", "-qm", "fixture")
        return git("rev-parse", "HEAD:" + path)
    def review(blob, path, category="numeric network address found"):
        target = tmp_path / "release/history-privacy-review.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps({"version": 1, "findings": [{
            "blob": blob, "path": path, "category": category,
            "review": "Reviewed fixture; historical infrastructure only."}]}))
    return validator, commit, review, git


def private_address():
    return ".".join(["192", "168", "40", "90"])


def test_exact_reviewed_history_passes(history, capsys):
    v, commit, review, _ = history
    sha = commit("old.md", private_address())
    commit("old.md", "sanitized")
    review(sha, "old.md")
    v.scan_history()
    assert not v.ERRORS
    output = capsys.readouterr().out
    assert "REVIEWED:" in output
    assert private_address() not in output


def test_review_does_not_allow_current_tree(history):
    v, commit, review, _ = history
    sha = commit("old.md", private_address())
    review(sha, "old.md")
    v.privacy("old.md", private_address())
    assert v.ERRORS


def test_changed_blob_fails(history):
    v, commit, review, _ = history
    sha = commit("old.md", private_address())
    review(sha, "old.md")
    commit("old.md", private_address() + " changed")
    v.scan_history()
    assert any("numeric network address" in e for e in v.ERRORS)


def test_identical_blob_at_other_path_fails(history):
    v, commit, review, _ = history
    sha = commit("old.md", private_address())
    review(sha, "old.md")
    commit("copied.md", private_address())
    v.scan_history()
    assert v.ERRORS


def test_secret_category_cannot_be_reviewed(history):
    v, commit, review, _ = history
    sha = commit("old.md", "clean")
    review(sha, "old.md", "non-placeholder credential assignment")
    with pytest.raises(ValueError):
        v.scan_history()


def test_new_secret_in_history_fails(history):
    v, commit, review, _ = history
    sha = commit("old.md", private_address())
    review(sha, "old.md")
    commit("credential.txt", "PASSWORD=" + "unsafe-value")
    v.scan_history()
    assert any("credential assignment" in e for e in v.ERRORS)


def test_unreviewed_branch_fails(history):
    v, commit, _, git = history
    commit("clean.md", "clean")
    git("checkout", "-qb", "other")
    commit("old.md", private_address())
    git("checkout", "-")
    v.scan_history()
    assert v.ERRORS


def test_tag_only_history_fails(history):
    v, commit, _, git = history
    commit("clean.md", "clean")
    git("checkout", "-qb", "other")
    commit("old.md", private_address())
    git("tag", "retained")
    git("checkout", "-")
    git("branch", "-D", "other")
    v.scan_history()
    assert v.ERRORS


def test_commit_message_still_scanned(history):
    v, commit, _, git = history
    commit("clean.md", "clean")
    git("commit", "--allow-empty", "-qm", private_address())
    v.scan_history()
    assert any("historical commit messages" in e for e in v.ERRORS)


def test_stale_review_fails(history):
    v, commit, review, _ = history
    sha = commit("clean.md", "clean")
    review(sha, "clean.md")
    v.scan_history()
    assert any("stale or unmatched" in e for e in v.ERRORS)


def test_known_filter_constant_history_passes(history):
    v, commit, _, _ = history
    commit("knowledge/ingest.py", "SECRET_NAME_PATTERNS = {\n'password'\n}\n")
    v.scan_history()
    assert not v.ERRORS


def test_filter_constant_other_path_fails(history):
    v, commit, _, _ = history
    commit("elsewhere.py", "SECRET_NAME_PATTERNS = {\n'password'\n}\n")
    v.scan_history()
    assert v.ERRORS


def test_filter_constant_real_assignment_fails(validator):
    validator.privacy("knowledge/ingest.py", "SECRET_NAME_PATTERNS = " + "unsafe-value")
    assert validator.ERRORS


def test_redacted_secret_output(validator):
    sample = "ghp_" + "A" * 25
    validator.privacy("fixture", sample)
    assert validator.ERRORS
    assert all(sample not in e for e in validator.ERRORS)


def test_shallow_history_refused(history, monkeypatch):
    v, commit, _, _ = history
    commit("clean.md", "clean")
    monkeypatch.setattr(v, "git", lambda *a, **kw: b"true\n")
    v.scan_history()
    assert v.ERRORS == ["history: full clone required"]
