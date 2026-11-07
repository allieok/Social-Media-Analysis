# Private data onboarding checklist

This is an operational checklist, not a completed agreement. The Lead and data approver
must record decisions privately before real-data processing.

- [ ] Name each data provider and authorized account representative.
- [ ] Record consent reference, permitted purposes, authorized reviewers, expiry, and withdrawal contact.
- [ ] Decide if external AI processing is permitted, by which provider, under which retention terms.
- [ ] Define original, derived, backup, audit-log, and provider-side retention periods.
- [ ] Define region, encryption, access roles, offboarding, and access-review schedule.
- [ ] Confirm metric definitions, observation dates/windows, usage rights, and platform terms.
- [ ] Test withdrawal: stop jobs; find originals/derivatives/exports; delete or recompute;
      verify versions, backups, local copies, and provider-side handling.
- [ ] Keep identity mapping and source URLs separate from analysis datasets.
- [ ] Record a release-specific review for every proposed public artifact.

## Private consent record template

Keep the completed form outside this repository:

| Field | Value to record |
| --- | --- |
| Consent reference | Opaque consent ID; private evidence location |
| Provider / authorized approver | Named contact stored privately |
| Scope | Sources, posts, purposes, reviewers, external providers |
| Timing | Effective date, expiry, withdrawal process |
| Storage | Region, access roles, original/derived retention |
| Rights | Video, voice, music, logo/reference permissions |
| Publication | What may be released and required approvals |
| Deletion owner | Responsible person and verification procedure |

The schema contains only a minimal processing-gate record; it does not replace the underlying
permission evidence. An opaque ID does not make transcripts, videos, or small aggregates anonymous.

## Publication gate

Prepare an explicit release allowlist. Review source files, Git history, notebook outputs,
screenshots, image metadata, paths, prompts, and small groups for disclosure/re-identification.
Confirm consent, usage rights, and platform terms. Obtain publisher and Project Lead approval.
Do not automate export of private outputs into this repository. CI does not certify privacy.
