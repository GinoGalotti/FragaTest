# FragaTest — Quality strategy for Fråga v2

Take-home assessment (Advania, Quality & Engineering Excellence Lead): how to make sure the shared AI platform is good enough for Fråga v2 and the other applications to launch on, and what "good" means.

## Repository map

| Folder | Contents |
|---|---|
| [deliverables/](deliverables/) | What gets handed in: quality strategy (01), evaluation design sheet (02), AI usage note (03). Plus a brief checklist (00) and session prep (04). |
| [harness/](harness/) | Runnable evaluation harness (Python + pytest): golden cases checked against the recorded v1 answers. See [harness/README.md](harness/README.md). |
| [notes/](notes/) | Working notes: testing ideas, open questions and assumptions, plans for incidents, scale-up and log-derived tests. |
| [features/](features/) | Assumed definition of new features (Summarize) used to design tests. |
| [data/](data/) | The two CSV appendices from the brief (policy excerpts, v1 log sample). |
| [ai-log/](ai-log/) | Audit trail of how AI was used: prompts, what AI produced, and every edit it made to my documents. |
| [.github/workflows/](.github/workflows/) | CI running the harness on every push. |

## Quick start

```bash
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python -m pytest harness -v
```

## Timeline

Commit timestamps are the time record. `git log --reverse --format="%ad %s" --date=format:%H:%M` shows the order of work.
