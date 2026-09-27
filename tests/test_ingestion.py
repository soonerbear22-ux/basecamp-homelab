"""Protect meaningful failure, replacement and idempotence contracts."""
import importlib.util
from pathlib import Path
from unittest.mock import Mock
import pytest

@pytest.fixture
def ingest(tmp_path, monkeypatch):
    monkeypatch.setenv("KNOWLEDGE_BASE", str(tmp_path))
    monkeypatch.setenv("EMBEDDING_URL", "http://embedding.example.invalid/embed")
    monkeypatch.setenv("QDRANT_URL", "http://qdrant.example.invalid")
    for name in ["inbox", "processed", "state"]:
        (tmp_path / name).mkdir()
    spec = importlib.util.spec_from_file_location("ingest_under_test", Path(__file__).resolve().parents[1] / "knowledge/ingest.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_embedding_failure_preserves_old_index_and_source(ingest, monkeypatch):
    source = ingest.INBOX / "runbook.md"
    source.write_text("# Runbook\nChanged operational content")
    state = {source.name: {"sha256": "old"}}
    delete, put = Mock(), Mock()
    monkeypatch.setattr(ingest, "embed", Mock(side_effect=RuntimeError("unavailable")))
    monkeypatch.setattr(ingest, "delete_document", delete)
    monkeypatch.setattr(ingest, "qdrant_put", put)
    with pytest.raises(RuntimeError):
        ingest.ingest_file(source, state)
    delete.assert_not_called(); put.assert_not_called()
    assert source.exists() and state[source.name]["sha256"] == "old"

def test_same_digest_skips_network_and_moves_file(ingest, monkeypatch):
    source = ingest.INBOX / "same.md"; source.write_text("Unchanged")
    state = {source.name: {"sha256": ingest.file_hash(source)}}
    embed = Mock(); monkeypatch.setattr(ingest, "embed", embed)
    ingest.ingest_file(source, state)
    embed.assert_not_called()
    assert (ingest.PROCESSED / source.name).read_text() == "Unchanged"
    assert not source.exists()

def test_replacement_orders_embeddings_before_delete_and_put(ingest, monkeypatch):
    source = ingest.INBOX / "updated.md"; source.write_text("# Section\nNew content")
    state = {source.name: {"sha256": "old"}}
    calls = []
    monkeypatch.setattr(ingest, "embed", lambda text: calls.append("embed") or [0.1] * 2560)
    monkeypatch.setattr(ingest, "delete_document", lambda name: calls.append("delete"))
    def put(points):
        calls.append("put")
        assert points[0]["payload"]["source"] == source.name
        assert points[0]["payload"]["section"] == "Section"
    monkeypatch.setattr(ingest, "qdrant_put", put)
    ingest.ingest_file(source, state)
    assert calls == ["embed", "delete", "put"]
    assert ingest.STATE_FILE.exists() and not source.exists()

def test_failed_upsert_leaves_source_and_old_state_for_recovery(ingest, monkeypatch):
    source = ingest.INBOX / "updated.md"; source.write_text("Changed")
    state = {source.name: {"sha256": "old"}}
    delete = Mock()
    monkeypatch.setattr(ingest, "embed", lambda _: [0.1] * 2560)
    monkeypatch.setattr(ingest, "delete_document", delete)
    monkeypatch.setattr(ingest, "qdrant_put", Mock(side_effect=RuntimeError("write failed")))
    with pytest.raises(RuntimeError):
        ingest.ingest_file(source, state)
    delete.assert_called_once_with(source.name)
    assert source.exists() and state[source.name]["sha256"] == "old"

def test_dimension_mismatch_is_rejected(ingest, monkeypatch):
    response = Mock(); response.json.return_value = [[0.1, 0.2]]
    monkeypatch.setattr(ingest.requests, "post", Mock(return_value=response))
    with pytest.raises(RuntimeError, match="dimension"):
        ingest.embed("test")

def test_chunking_retains_section_and_covers_tail(ingest):
    chunks = ingest.make_chunks("# Heading\n" + "example text. " * 300 + "END_MARKER")
    assert len(chunks) > 1
    assert all(c["section"] == "Heading" and len(c["text"]) <= 1400 for c in chunks)
    assert chunks[-1]["text"].endswith("END_MARKER")
