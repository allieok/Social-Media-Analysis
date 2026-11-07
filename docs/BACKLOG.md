# Pilot backlog and acceptance criteria

Use these as initial GitHub issue descriptions. Real private evidence stays outside issues.

| Order | Task | Acceptance |
| --- | --- | --- |
| 1 | Kickoff decisions | Ownership, budget, private storage, metric definitions, consent and retention agreed |
| 2 | Export importer | Map a privately approved 2–3 post sample; preserve missingness and units; reject duplicates |
| 3 | 20-post intake | Approved media/metrics linked by opaque ID; separate identity mapping; provenance recorded |
| 4 | Media preprocessing | FFmpeg audio extraction and bounded frame sampling; timestamps valid; temp files cleaned |
| 5 | Provider benchmark | Japanese quality and data terms compared on same approved sample; actual cost/post recorded |
| 6 | Private S3 storage | Block public access, encryption, scoped roles, lifecycle and deletion/version tests |
| 7 | Extraction runner | Consent checked at dispatch; bounded retry, cache invalidation, partial-stage resume, usage cap tests |
| 8 | Labels and audit | Label guide; stratified 10–20% human audit; per-feature agreement and corrections |
| 9 | Week 5 gate | At least 50 posts, selected primary metric <20% missing, audit agreement >=80%, cost/participation reviewed |
| 10 | Review/planning | Timestamped evidence and specific edits; approved context; generic-vs-contextual blinded scoring |
| 11 | Poster experiment | Fixed A–D conditions and generation counts; blinded scoring and factual/rights review |
| 12 | Content experiments | At least two predeclared comparisons; one factor changed; comparable windows and limitations |
| 13 | Handover/release | Independent rerun, internal report, ownership handover, two-person approval of public artifacts |

The current offline baseline tool is not a substitute for tasks 4–8. It has no model cache,
live spending enforcement, or job-resume capability yet. Introduce these alongside actual providers.
