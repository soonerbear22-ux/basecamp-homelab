import sys
from pathlib import Path
from unittest.mock import Mock
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from init_collection import ensure_collection
from site_config import read_env, check_values

def test_missing_collection_created_with_correct_contract():
    session = Mock(); session.get.return_value.status_code = 404
    assert ensure_collection("http://vectors.example.invalid", session) == "created"
    assert session.put.call_args.kwargs["json"] == {"vectors": {"size": 2560, "distance": "Cosine"}}

@pytest.mark.parametrize("size,distance", [(1536, "Cosine"), (2560, "Dot")])
def test_mismatch_never_replaces_collection(size, distance):
    session = Mock(); session.get.return_value.status_code = 200
    session.get.return_value.json.return_value = {"result": {"config": {"params": {"vectors": {"size": size, "distance": distance}}}}}
    with pytest.raises(ValueError): ensure_collection("http://vectors.example.invalid", session)
    session.put.assert_not_called()

def test_matching_collection_does_not_write():
    session = Mock(); session.get.return_value.status_code = 200
    session.get.return_value.json.return_value = {"result": {"config": {"params": {"vectors": {"size": 2560, "distance": "Cosine"}}}}}
    assert ensure_collection("http://vectors.example.invalid", session) == "verified"
    session.put.assert_not_called()

def test_environment_values_are_data_not_shell(tmp_path):
    file = tmp_path / "site.env"
    file.write_text("VALUE='literal $text with spaces'\n# Comment\n")
    assert read_env(file)["VALUE"] == "literal $text with spaces"

def test_examples_fail_preflight_without_printing_values():
    with pytest.raises(ValueError, match="SERVICE") as error:
        check_values({"SERVICE": "http://example.invalid"})
    assert "http://" not in str(error.value)
