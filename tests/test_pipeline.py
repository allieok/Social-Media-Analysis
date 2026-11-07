import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from jet_social.models import Dataset
from jet_social.pipeline import rate, run

FIXTURE = Path(__file__).parents[1] / "examples/synthetic/posts.json"


def sample():
    return json.loads(FIXTURE.read_text())


@pytest.mark.parametrize("change", ["withdrawn", "expired", "no_analysis"])
def test_consent_blocks_processing(change, tmp_path):
    obj = sample()
    consent = obj["posts"][0]["consent"]
    if change == "withdrawn":
        consent["status"] = "withdrawn"
    elif change == "expired":
        consent["expires_at"] = "2000-01-01T00:00:00Z"
    else:
        consent["purposes"] = ["review"]
    with pytest.raises(ValueError, match="Processing blocked"):
        run(Dataset.model_validate(obj), b"fixture", tmp_path)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("change", ["duplicate", "interval", "negative", "window", "missing"])
def test_invalid_data_rejected(change):
    obj = sample()
    post = obj["posts"][0]
    if change == "duplicate":
        obj["posts"].append(post)
    elif change == "interval":
        post["features"][0]["end_ms"] = post["duration_ms"] + 1
    elif change == "negative":
        post["metrics"]["reach"] = -1
    elif change == "window":
        post["metrics"]["observed_at"] = post["published_at"]
    else:
        post["metrics"]["saves"] = None
        post["metrics"]["missing_reason"] = None
    with pytest.raises(ValidationError):
        Dataset.model_validate(obj)


def test_missing_and_zero_denominator_are_not_zero_rates():
    assert rate(4, 0) is None
    assert rate(None, 100) is None
    assert rate(0, 100) == 0
    assert rate(5, 100) == 0.05


def test_runs_preserve_windows_and_do_not_overwrite(tmp_path):
    obj = sample()
    post = obj["posts"][0]
    post["metrics"]["window_hours"] = 24
    data = Dataset.model_validate(obj)
    first = run(data, b"fixture", tmp_path)
    second = run(data, b"fixture", tmp_path)
    assert first != second
    baseline = json.loads((first / "baselines.json").read_text())
    assert {r["window_hours"] for r in baseline} == {24, 168}
    manifest = json.loads((first / "manifest.json").read_text())
    assert manifest["status"] == "completed"
    assert manifest["external_calls"] == 0
    assert len(manifest["artifact_sha256"]) == 2
    data.authorize(datetime.now(UTC))


def test_schema_matches_export():
    path = Path(__file__).parents[1] / "schemas/dataset.schema.json"
    assert json.loads(path.read_text()) == Dataset.model_json_schema()
