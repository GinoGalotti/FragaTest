# Session 01 — 2026-11-26 (Claude Code, Claude Opus 5.5)

| # | Time | My request (summary) | What the AI did | My decision / review |
|---|---|---|---|---|
| 1 | ~09:00 | Clone the empty repo and get it ready. | Cloned it and confirmed it was empty. | — |
| 2 | ~09:14 | Push a dummy README. | Committed and pushed a placeholder README to `main`. | — |
| 3 | ~09:40 | Full brief: see [00-initial-prompt.md](00-initial-prompt.md). Structure the repo, add questions and templates, fix wording with a change log, keep an AI audit trail. | Read the brief PDF and both CSVs. Restructured the repo; git-ignored the PDF. Wrote a brief checklist, templates for the strategy, evaluation sheet, AI usage note and session prep. Rewrote my notes for clarity and added 14 open questions ([edits.md](edits.md)). Added a first-pass verdict on all 20 log lines. Scaffolded the harness (2 example cases plus self-tests) and a CI workflow. | _To review:_ log verdicts in notes/TestForCurrentLog.md · added questions · harness CI decision (see harness/README.md). |

## Issues the AI found along the way

- Global `pytest` on this machine fails to start (an old `pytest-flask` plugin breaks on import). The harness uses a project `.venv` instead.
- Document growth is ~13x, not 15x (40,000 / 3,000). Flagged in notes/TestForUpscaling.md.
- The AI first marked L11 as correct, then corrected it to wrong on recheck (grade 5 has a > 3 km limit). This shows why the first pass needs my review.
