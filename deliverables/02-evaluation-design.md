# Evaluation Design Sheet — Fråga answers and guardrails

> Brief: ~45 min. 5–8 evaluation criteria (for answers **and** guardrails), each with a judging method (code check, model as judge, or person) and a pass threshold. Turn at least 8 of the 20 log lines into golden test cases.

## 1. Evaluation criteria

| ID | Criterion | Applies to | Judged by | Pass threshold | Why it matters |
|---|---|---|---|---|---|
| C1 | | Answer | Code | | |
| C2 | | Answer | Model | | |
| C3 | | Guardrail | Code | | |
| C4 | | | Person | | |
| C5 | | | | | |

Ask yourself:
- Does each criterion trace back to a risk (strategy §3), an incident or a log line?
- Is the threshold per case (must pass) or over the whole set (≥ X %)? Safety criteria usually need 100 %.
- How do you check the model judge itself? (Agreement with people on a sample, and how often.)
- Guardrail criteria: do you measure both false negatives (a leak gets through) and false positives (L05: a valid question refused)?
- Non-determinism: how many runs per case, and what pass rate across runs?

Candidate areas: cited source exists and is current · amounts and durations match the source · no personal data from other cases (P-107) · refuses or says "I don't know" when it should, and only then · answers the question asked · Swedish language and compound words · length and format limits.

## 2. Golden test cases

Fields: the answer must contain key facts (not exact wording), must not contain forbidden content, and must cite the expected sources.

| Case | Log | Question (short) | Expected behaviour | Must contain | Must not contain | Expected sources | Criteria | Recorded answer passes? |
|---|---|---|---|---|---|---|---|---|
| G01 | L.. | | | | | | | |
| G02 | | | | | | | | |
| … | | | | | | | | |

Ask yourself:
- Does the set cover each incident type, both rating directions (up and down), and refusals?
- Which golden cases does the recorded v1 answer **fail**? (A harness that only passes proves nothing.)
- Which cases need v2 variants? (Swedish phrasing, compound words, conflicting documents.)
- Who maintains the golden set as policies change?

## 3. Where each criterion runs

| Criterion | Per PR (recorded / mocked) | Nightly (live model) | Pre-release | Production sample |
|---|---|---|---|---|
| | | | | |
