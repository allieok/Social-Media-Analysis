import json
import sys

from test_pipeline import sample

from jet_social.cli import main


def test_validation_errors_do_not_print_input(tmp_path, monkeypatch, capsys):
    path = tmp_path / "bad.json"
    obj = sample()
    obj["posts"][0]["purpose"] = "PRIVATE_CONTEXT_DO_NOT_LOG"
    path.write_text(json.dumps(obj))
    monkeypatch.setattr(sys, "argv", ["jet-social", "validate", str(path)])
    assert main() == 2
    output = capsys.readouterr()
    assert "PRIVATE_CONTEXT_DO_NOT_LOG" not in output.err
    assert "Validation failed" in output.err


def test_demo_rejects_real_dataset(tmp_path, monkeypatch):
    path = tmp_path / "real.json"
    obj = sample()
    obj["synthetic"] = False
    for post in obj["posts"]:
        post["metrics"]["source"] = "owner_export"
        post["features"] = []
    path.write_text(json.dumps(obj))
    target = tmp_path / "runs"
    monkeypatch.setattr(
        sys, "argv", ["jet-social", "demo", "--input", str(path), "--output", str(target)]
    )
    assert main() == 2
    assert not target.exists()
