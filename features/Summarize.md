# Summarize case file (new in v2)

The brief only says v2 "adds a new Summarize case file feature". Everything below is **assumed**. Fill it in, mark each item as an assumption, and link it to notes/OpenQuestions.md.

## Definition (assumed)

| Aspect | Assumption |
|---|---|
| Input | _(case file: documents, notes, emails? formats? size limit?)_ |
| Output | _(length, structure: facts, timeline, open actions, applicable policies?)_ |
| Who uses it, and when | |
| Does it cite policies or case documents? | |
| Language(s) | |
| Latency target (does the 8 s apply?) | |
| Where the case file and summary are stored and logged | |

## Risks

Ask yourself:
- **Privacy (P-107):** can a summary pull in content from another case? (Retrieval scoped by case, cache leakage between users.)
- **Faithfulness:** does every fact in the summary appear in the source? Are amounts, dates and names copied exactly?
- **Omission:** is a critical fact dropped (deadline, appeal window, decision)?
- **Invented policy links:** if it maps a case to policies, are they current (Incident 1)?
- **Size:** what happens when a case file exceeds the context window? Is it truncated silently?
- **Load:** long prompts at peak cost GPU time shared with 4 other apps.

## Tests

| Check | How (code / model / person) | Threshold | Cadence now | Cadence once stable |
|---|---|---|---|---|
| Every amount and date in the summary appears in the source | code | 100 % | | |
| No identifiers from other cases | code + seeded canary data | 0 | | |
| Key facts present (per synthetic case) | model judge + person sample | | | |
| Length and format limits | code | | | |
| Oversized input is handled explicitly | integration | | | |

**De-escalation rule (from my pillars):** Summarize starts with heavy, frequent testing. Lower the cadence once ___ consecutive runs have passed and no Summarize incident has occurred for ___ weeks.

## Example synthetic case file

_(Create 2–3 synthetic case files under `features/examples/` to drive the tests: no real data.)_
