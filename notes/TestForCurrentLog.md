# Tests from the current log (thumbs up/down)

Tests we could build to cover the thumbs-up/down answers we see in the v1 log.

## AI first pass — please verify

My (Claude's) reading of each log line against [data/fraga-policy-excerpts.csv](../data/fraga-policy-excerpts.csv).

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
- As rating isn't always truth, we should periodically audit our answers and re-run results to see if we get a similar response. Determinism should be higher on higher certainty/confidence answers. 
- 5 of 20 are unrated, including a wrong one (L11), so rating coverage is a metric in itself.
- Tally: 12 correct, 1 partial, 7 wrong (L03, L05, L07, L11, L13, L16, L18).
- Failure types: repealed source, wrong number, false refusal, missed retrieval, wrong rule branch, privacy leak. Each maps to an evaluation criterion.


### Repealed source cited
Example: L03

We should add tests covering (not only on a specific policy, but covering several policies with similar setup)
* Asking for a policy that has been repealed and have a new one, should answer with the new one (and probably mentioned the repealed). Validate the information (values) show the new one. Certainty should be high.
* Asking for a policy that has been repealed and specifying a time that was before it was repealed should show the old policy values, and mentioned it has been repealed after XXX date. Certainty should be high.
* Asking for a policy that has been repealed and specifying a time that was after it was repealed should show the new policy values, and mentioned it has been repealed after XXX date. Certainty should be high.

False positives can cause a lot of harm, so this should be a test on high cadence / risk / priority. 

### Wrong value (number/duration)
Example: L07, L16

We should have test covering keywords:
* Asking for policies that cite time units and seeing the result contains it (3 weeks, 10 days, 1 year after moving in). Some keywords are important, not only the number.
* Test for boundaries. On the age cases, if the policy mentions "over 85", test for the boundaries (exactly 85). If that causes uncertainty, check that the answer express so.
* Test that we specify the unit: weeks, SEK, age, etc. For clarity, the answer should always contain the unit (and in case of numbers, test for format, like decimals / thousands)

False values and timetables can cause a lot of harm, so this should be a test on high cadence / risk / priority. 

### False Refusal
Example: L05

This might fall into the Embarrasing answers category, but it is always better to refuse than to hallucinate an answer. 

We should test:
* Add the specific test case to the regression suit in case the problem is that a specific keyword on the question. 

This could be covered in a lot of other testing that we are running. It should be included in our testing, but it can be added to a regression suit that runs on lower cadence. 

### Missed Retreival
Example: L13

We should test:
* Add the specific test case to the regression suit in case the problem is that a specific keyword on the question or maybe the specific policy. 

This could be covered in a lot of other testing that we are running. It should be included in our testing, but it can be added to a regression suit that runs on lower cadence. 

### Privacy Leak
Example: L18

We should test:
* Tests that ask for other cases within the same conversation. Guessing we shouldn't reference other cases. Answer should explicitly flag about the rules on sharing information between cases.
* Tests referencing other cases across several policies, and using different styles of language: directly or indirectly asking for other cases. Consult with experts on prompt engineering to focus on those issues (this is a common problem accross AI). Answer should be explicit about this not being permitted.

Privacy leaks can cause a lot of harm, so this should be a test on high cadence / risk / priority. 

