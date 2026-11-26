# Session 01 — 2026-11-26 (Claude Code, Claude Opus 5.5)

| # | Time | My request (summary) | What the AI did | My decision / review |
|---|---|---|---|---|
| 1 | ~09:00 | Clone the empty repo and get it ready. | Cloned it and confirmed it was empty. | — |
| 2 | ~09:14 | Push a dummy README. | Committed and pushed a placeholder README to `main`. | — |
| 3 | ~09:40 | Full brief: see [00-initial-prompt.md](00-initial-prompt.md). Structure the repo, add questions and templates, fix wording with a change log, keep an AI audit trail. | Read the brief PDF and both CSVs. Restructured the repo; git-ignored the PDF. Wrote a brief checklist, templates for the strategy, evaluation sheet, AI usage note and session prep. Rewrote my notes for clarity and added 14 open questions ([edits.md](edits.md)). Added a first-pass verdict on all 20 log lines. Scaffolded the harness (2 example cases plus self-tests) and a CI workflow. | _To review:_ log verdicts in notes/TestForCurrentLog.md · added questions · harness CI decision (see harness/README.md). |
| 4 | ~09:55 | Clarified: the harness illustrates *how* we would test, not a pass/fail gate. The AI got ahead of me; my order of work is: open questions → Summarize feature → TestForLog / Upscaling / Incidents → harness tests and run cadence → deliverables. Commit as we go, as a timetable. | Reframed harness/README.md; switched CI to manual trigger only; committed. | Order of work set by me. |
| — | ~09:55–10:05 | _Not AI work:_ call with the recruiter. I reviewed the open questions and wrote assumptions. | — | — |
| 5 | ~10:10 | Check my open questions pass and its wording; renumber. | Renumbered Q1–Q23, fixed typos and wording, set statuses, flagged Q10 (which language?) and Q15 (memory vs follow-up messages in Incident 3). See [edits.md](edits.md). | _To confirm:_ Q10, Q15. |
| 6 | ~10:15 | Q10: the language doesn't matter; I just don't want localisation in the test cases. Q15: confirmed. | Updated Q10 and Q15 wording. | Confirmed. |
| — | ~10:16–10:36 | _Not AI work:_ I defined Summarize (features/Summarize.md) and wrote the test table in notes/TestForSummarize.md. | — | — |
| 7 | ~10:40 | Create synthetic case files as mocked API calls (payload = case file; response = status code, payload, certainty, policies cited, audit location) and mock a test. | Wrote S01–S08 (clear match, repealed trap, unclear boundary, other-case canary, appeal deadline, oversized 413, unauthorised 403, unknown field 400) in notes/TestForSummarize.md. Wrote harness/test_summarize.py, which reads them from the markdown, with 4 self-tests. 12/12 pass. | _To review:_ the assumed API contract and the case contents. |

## Issues the AI found along the way

- Global `pytest` on this machine fails to start (an old `pytest-flask` plugin breaks on import). The harness uses a project `.venv` instead.
- Document growth is ~13x, not 15x (40,000 / 3,000). Flagged in notes/TestForUpscaling.md.
- The AI first marked L11 as correct, then corrected it to wrong on recheck (grade 5 has a > 3 km limit). This shows why the first pass needs my review.
