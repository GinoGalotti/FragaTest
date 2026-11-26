# Tests from the current log (thumbs up/down)

Tests we could build to cover the thumbs-up/down answers we see in the v1 log.

## AI first pass — please verify

My (Claude's) reading of each log line against [data/fraga-policy-excerpts.csv](../data/fraga-policy-excerpts.csv). **Not yet reviewed by me (Gino).**

| Log | Rating | Verdict vs policy | Note |
|---|---|---|---|
| L01 | up | correct | |
| L02 | none | correct | |
| L03 | **up** | **wrong (repealed source)** | Cites P-101, repealed 2024; should be P-114. Incident 1 pattern. |
| L04 | up | correct | |
| L05 | down | **wrong (false refusal)** | General question refused as "individual case"; P-102 has the answer. |
| L06 | up | correct | |
| L07 | **up** | **wrong (amount)** | Says 3 months; P-108 says 3 weeks. |
| L08 | **down** | correct | Matches P-114. Rating looks wrong, or the user wanted more. |
| L09 | none | correct (refusal) | A good refusal: points to the rules and the case worker. |
| L10 | up | correct | |
| L11 | none | **wrong (rule branch)** | Grade 5: limit is > 3 km, so 2.5 km → **not** entitled. The answer says "Yes", applying the grade 1–3 rule. |
| L12 | none | correct | |
| L13 | down | **wrong (missed retrieval)** | P-103 says 250 SEK; Fråga said it had no information. |
| L14 | up | partial | Correct; the rental contract isn't mentioned (not asked). |
| L15 | **down** | correct | Grade 8, 3.5 km, limit > 4 km → not entitled. Rating looks wrong. |
| L16 | down | **wrong (amount)** | Says 30 days; P-102 says 14 days. |
| L17 | up | correct | |
| L18 | **up** | **wrong (privacy breach)** | Discloses a name, case number and address from another case. Violates P-107. Most severe. |
| L19 | up | correct | |
| L20 | none | correct | Handles the repeal correctly. |

**Takeaways to consider:**
- Ratings are not ground truth: 3 harmful answers are rated up (L03, L07, L18), and 2 correct answers are rated down (L08, L15).
- 5 of 20 are unrated, including a wrong one (L11), so rating coverage is a metric in itself.
- Tally: 12 correct, 1 partial, 7 wrong (L03, L05, L07, L11, L13, L16, L18).
- Failure types: repealed source, wrong number, false refusal, missed retrieval, wrong rule branch, privacy leak. Each maps to an evaluation criterion.

## Test ideas per failure type

| Failure type | Log lines | Check (code / model / person) | Layer | Cadence |
|---|---|---|---|---|
| Repealed source cited | L03 | | | |
| Wrong number or duration | L07, L16 | | | |
| Wrong rule branch (thresholds) | L11 | | | |
| False refusal | L05 | | | |
| Missed retrieval | L13 | | | |
| Privacy leak (P-107) | L18 | | | |
| Rating disagrees with policy | L03, L07, L08, L15, L18 | | | |

Ask yourself: for threshold rules (P-104 school transport, P-114 income limit), which boundary cases do you add? (Exactly 3 km, 22,000 SEK, age 85 vs 86.)
