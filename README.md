# JET Social Media Analysis

Batch-first tools for a 10-week student-organization content research pilot.
See [ARCHITECTURE.md](ARCHITECTURE.md) for the design and [docs/START_HERE.md](docs/START_HERE.md)
for the information needed to begin the real-data pilot.

## Quick start

Requirements: Python 3.12 and [uv](https://docs.astral.sh/uv/getting-started/installation/)
0.13.5 (the version used to generate the lockfile and in CI).
FFmpeg is available in the current Codex workspace and will be needed for future media extraction;
the offline baseline demo does not require it.

```bash
git clone https://github.com/allieok/Social-Media-Analysis.git
cd Social-Media-Analysis
uv sync --locked
uv run jet-social doctor
uv run jet-social validate examples/synthetic/posts.json
uv run jet-social demo
uv run pytest
```

Each demo run creates a new ignored `work/runs/<run-id>/` directory containing
`posts.csv`, `baselines.json`, and `manifest.json`. These use 20 entirely invented posts;
their numbers are software examples, not research findings. Rates use reach as the denominator.
Baselines are separated by account, platform, purpose, and measurement window.

## Available now

- Strict, versioned intake, consent, metric, and timed-feature contracts.
- Consent validation, missing-value handling, zero-denominator handling, and duplicate-ID rejection.
- Offline baseline analysis and provenance/artifact hashes.
- Synthetic fixture, generated JSON Schema, locked Python environment, tests, and CI workflow.
- Pilot configuration template and onboarding, data-governance, and implementation checklists.

ASR/OCR/VLM extraction, review/script/poster generation, S3 integration, live budget controls,
resumable extraction stages, and a UI are still planned. The provider interface is a contract only.
No live service is provisioned and no model API is called by this starter.

## Commands

```bash
# Real metadata must stay in an ignored, access-controlled private location.
uv run jet-social validate private/posts.json
uv run jet-social analyze private/posts.json --output private/runs
uv run jet-social schema --output schemas/dataset.schema.json
uv run ruff check .
uv run ruff format --check .
```

`analyze` performs local arithmetic on an approved manifest, not video analysis. Local files
are not encrypted or access-controlled by this application; the operator must secure them.
Validation checks declared consent, not its authenticity: the data approver must verify it.
The TOML file is a planning template and is not yet consumed by the CLI. Live controls must
be implemented and tested before live processing.

Do not commit actual media, metrics, consent records, notes, provider outputs, or credentials.
`.gitignore` helps prevent accidents; it is not a confidentiality control. Repository visibility
and public release approval remain project-owner decisions. No software license has been
chosen; the owner must choose one before advertising the code for reuse.
