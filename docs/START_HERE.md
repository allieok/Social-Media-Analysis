# Start the pilot

## What is ready

The Python package and locked environment run offline against 20 synthetic posts. The CLI
validates metadata, blocks expired/withdrawn consent, exports schemas, calculates baseline
rates, and writes auditable run artifacts. CI repeats the offline checks without secrets.
This is an initial working slice, not the full multimodal pipeline.

The current Codex workspace has Python 3.12 and FFmpeg. A project-local virtual environment
is created by `uv sync --locked`. This does not configure your personal computer or provision AWS.

## Provide these first

| Needed | What to provide | Why |
| --- | --- | --- |
| Project ownership | Lead, data/account approver, engineering contact, research/content reviewer | Establish decisions and access responsibilities |
| Pilot scope | Confirm Instagram Reels first; available number of JET and partner posts | Target a 20-post intake trial, then 50–150 total |
| Authorized sample | A privately shared sample export for 2–3 posts first, then 20 approved video files and matching metadata/metrics | Build the importer against actual export fields and media |
| Permissions | Data-owner approval covering analysis, human reviewers, external AI processing if desired, and permitted outputs | Determine which workflows are authorized |
| Outcome definition | Available metrics, observation dates/windows, preferred primary outcome | Avoid comparing incompatible rates |
| Budget | Lean CAD 150 or Base CAD 425 for the full pilot; payer and spending approver | Set measurable provider and processing limits |
| Storage boundary | AWS account/region preference and approved private storage; retention/deletion requirements | Define where data may be stored and processed |
| Repository policy | Confirm private/public visibility and whether this repo contains only the reusable core | Keep real data and organizational results private |

Do not paste API keys, AWS secrets, passwords, private videos, or consent records into GitHub
issues. Use a private, approved transfer location for source material. Add credentials through
Codex environment settings or a managed secret store after provider selection; share only the
credential variable names and access scopes in chat. Do not grant administrator access.

## Minimum sample to share privately

Start with the original export format; you do not need to hand-convert it to our schema.
Provide a description of each column, units, metric definitions, time zone, and date of export.
For each post, include an opaque local ID linking its media to its metrics, duration, publication
date/time, purpose, and known paid/collaboration status. Include reach, saves, and shares if
available. Missing metrics are acceptable when marked with a reason; do not replace them with zero.

For retention/completion, average watch time, profile visits, or follows, include platform
definitions and observation windows. Public engagement counts alone cannot establish private
retention or conversion outcomes. Keep source URLs/account mapping in a separately restricted file.

If sharing a screenshot instead of an export, redact unrelated information and ensure the
account owner approves that transfer. No automated collection or scraping is needed to start.

## Before live model processing

1. Confirm provider/model shortlist, Japanese-language requirements, region constraints,
   data-retention/training terms, and external-model permission for each source.
2. Agree a 20-post cost/quality benchmark and per-run limits for seconds, frames, tokens, and retries.
3. Configure least-privilege runtime credentials and test access using disposable objects.
4. Implement provider calls, usage accounting, bounded retries, caches, and consent enforcement at dispatch.
5. Test deletion and consent withdrawal across local copies, object versions, derived files,
   caches, and provider-retained artifacts before onboarding the full dataset.

Approval to analyze does not automatically authorize external-model processing, public release,
or posting on social platforms. This starter does not post content.

## For review, planning, and poster features

Later provide approved brand guidelines, audience/persona, content goals, good/bad examples,
anonymized meeting notes, prior reviews, poster reference assets with usage rights, and event
facts/CTA. Mark which context is approved for which provider. Name human reviewers and define
a shared scoring rubric before comparing generic and contextual prompts.

## Kickoff reply template

```text
Lead / account approver:
Platform and number of available posts:
Private sample transfer location:
Available metrics and observation windows:
Primary outcome preference:
Owner permission status (analysis / external AI / publication):
Budget and payer:
AWS region/storage preference:
Retention and deletion requirements:
Repository visibility / public-core policy:
Preferred model providers or constraints:
```

Unknown answers are fine. The first 2–3 approved sample posts and ownership/budget decisions
are enough to begin importer design; external AI remains blocked until its prerequisites are met.
