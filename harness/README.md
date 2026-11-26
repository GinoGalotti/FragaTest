# Evaluation harness

Runs golden cases ([golden_cases.json](golden_cases.json)) against the answers recorded in [data/fraga-log-sample.csv](../data/fraga-log-sample.csv). No model or API key is needed.

## Run

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt     # Windows (on Linux/macOS: .venv/bin/pip)
.venv/Scripts/python -m pytest harness -v         # CI-style, exit code 1 on failure
.venv/Scripts/python harness/fraga_eval.py        # plain report, standard library only
```

## Golden case fields

| Field | Meaning |
|---|---|
| `must_contain` | Facts the answer must contain (case-insensitive; `1,688` = `1688`). |
| `must_not_contain` | Content that must not appear (wrong amounts, personal data). |
| `expected_sources` | Policy IDs that must be cited. |
| `allow_non_current_sources` | Set to `true` only when citing a repealed policy is correct (e.g. L20 explains the repeal). |

Every case is also checked for citing a non-current (repealed) policy.

## Decisions for you

- [ ] **Known-bad recorded answers in CI:** let them fail (honest red: the harness finds v1 defects), or mark them `xfail` as documented defects so CI stays green and goes red only on change?
- [ ] Which 5–10 cases to include (G01 and G02 are examples).
- [ ] Add checks for refusal and personal data (L05, L09, L18)? For example, a regex for case numbers like `2025-0412`.
