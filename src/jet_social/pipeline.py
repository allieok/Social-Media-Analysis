"""Offline baseline calculation; never invokes a model or uploads data."""

import csv
import hashlib
import json
import subprocess
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import median
from uuid import uuid4

from jet_social import __version__
from jet_social.models import Dataset


def rate(numerator: int | None, denominator: int | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def load_dataset(path: Path) -> Dataset:
    dataset = Dataset.model_validate_json(path.read_bytes())
    dataset.authorize(datetime.now(UTC))
    return dataset


def run(dataset: Dataset, input_bytes: bytes, output_root: Path) -> Path:
    dataset.authorize(datetime.now(UTC))
    rows = []
    grouped = defaultdict(list)
    for post in dataset.posts:
        m = post.metrics
        row = {
            "post_id": str(post.post_id),
            "account_id": str(post.account_id),
            "platform": post.platform,
            "purpose": post.purpose,
            "window_hours": m.window_hours,
            "reach": m.reach,
            "saves": m.saves,
            "shares": m.shares,
            "save_rate_per_reach": rate(m.saves, m.reach),
            "share_rate_per_reach": rate(m.shares, m.reach),
            "missing_reason": m.missing_reason,
            "synthetic": dataset.synthetic,
        }
        rows.append(row)
        grouped[(str(post.account_id), post.platform, post.purpose, m.window_hours)].append(row)

    baselines = []
    for (account, platform, purpose, window), group in sorted(grouped.items()):
        values = [r["save_rate_per_reach"] for r in group if r["save_rate_per_reach"] is not None]
        baselines.append(
            {
                "account_id": account,
                "platform": platform,
                "purpose": purpose,
                "window_hours": window,
                "post_count": len(group),
                "primary_metric_missing_fraction": 1 - len(values) / len(group),
                "median_save_rate_per_reach": median(values) if values else None,
            }
        )

    run_id = str(uuid4())
    target = output_root / run_id
    target.mkdir(parents=True, exist_ok=False)
    try:
        revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True
        ).strip()
        dirty = bool(
            subprocess.check_output(
                ["git", "status", "--porcelain"], stderr=subprocess.DEVNULL, text=True
            ).strip()
        )
    except (OSError, subprocess.CalledProcessError):
        revision, dirty = "unavailable", None
    manifest = {
        "run_id": run_id,
        "schema_version": "1.0",
        "package_version": __version__,
        "started_at": datetime.now(UTC).isoformat(),
        "git_revision": revision,
        "git_worktree_dirty": dirty,
        "input_sha256": hashlib.sha256(input_bytes).hexdigest(),
        "synthetic": dataset.synthetic,
        "post_count": len(rows),
        "stage": "offline_baseline",
        "external_calls": 0,
        "model": None,
        "prompt": None,
        "status": "running",
    }
    manifest_path = target / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    try:
        with (target / "posts.csv").open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        (target / "baselines.json").write_text(json.dumps(baselines, indent=2) + "\n")
    except Exception:
        manifest["status"] = "failed"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        raise
    manifest["status"] = "completed"
    manifest["completed_at"] = datetime.now(UTC).isoformat()
    manifest["artifact_sha256"] = {
        name: hashlib.sha256((target / name).read_bytes()).hexdigest()
        for name in ("posts.csv", "baselines.json")
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return target
