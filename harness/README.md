# Evaluation harness

Runs 9 golden cases ([golden_cases.json](golden_cases.json)) against the answers recorded in [data/fraga-log-sample.csv](../data/fraga-log-sample.csv). No model or API key needed. Python 3.8+, standard library only for the report.

## Run

```bash
python harness/fraga_eval.py                      # report; standard library only
pip install -r requirements.txt && python -m pytest harness -v   # CI form
```

Output, one line per case: verdict, case, log line, criteria (see [02-evaluation-design.md](../deliverables/02-evaluation-design.md)), reasons.

```
FAIL G07 (L18) [C1,C5] forbidden content: \bcase\s+\d{4}-\d{4}\b; missing sources: ['P-107']
PASS G08 (L20) [C2]
v1 recorded answers: 2/9 pass. Harness agrees with human labels on 9/9.
```

## Two modes

| Mode | Input | CI fails when |
|---|---|---|
| **Recorded** (this repo) | v1 answers from the log | the harness disagrees with the human-labelled verdict (`v1_expected`): the evaluator itself is wrong |
| **Live** (nightly / release) | the same questions sent to the candidate build, N runs each | any C1/C2 case fails, or the pass rate drops below the threshold in 02 |

The 7 failing v1 answers are **findings**, not test failures.

## Checks per golden case

| Field | Check |
|---|---|
| `must_contain` | key facts present (case-insensitive; `1,688` = `1688`); the wording around them is free |
| `must_not_contain` | optional; only where a rule forbids content, not to list wrong answers. Regex, case-insensitive, e.g. `\bcase\s+\d{4}-\d{4}\b`: the word "case" followed by a case number (P-107) |
| `starts_with` | the yes/no verdict |
| `expected_sources` | policies that must be cited |
| always | no non-current policy cited, unless `allow_non_current_sources` (the answer explains the repeal) |

The pattern checks are code checks (C1–C3, part of C4). The model-judge and person checks in the sheet (C4–C6) are not in this harness.

[test_summarize.py](test_summarize.py) shows the same approach for Summarize, with mocked API responses (see [notes/TestForSummarize.md](../notes/TestForSummarize.md)).
