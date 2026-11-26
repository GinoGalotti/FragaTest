# Regression tests for known incidents

How we test so that each known incident cannot recur unnoticed.

## Template (one per incident)

| Field | |
|---|---|
| What happened | |
| Root cause (known / assumed) | |
| Why it wasn't caught | |
| How long to detect, and what would detect it in minutes | |
| Regression tests (layer: unit / contract / integration / eval / monitor) | |
| Pass condition | |
| Cadence (commit / PR / nightly / on demand / release) | |
| Owner | |
| Related log lines | |

## Incident 1: repealed housing rule cited

Fråga cited a housing rule repealed in 2024, and a case worker repeated it to a citizen.

Ask yourself:
- Is this a retrieval failure (repealed doc ranked), a data failure (status missing in metadata) or a generation failure (status ignored)? Do you test all three?
- Related log lines: L03 cites repealed P-101 and is rated **up**; L20 handles the repeal correctly.
- With 40k documents, how many repealed or superseded versions will exist? Can you check "no repealed source cited" with code?
- How fast must a repeal reach the index (ingestion SLA)?

### Tests to regress this

* If possible, use the actual query from the user and ensure that we respond with the correct answer (either that the rule has been repealed, or the new policy)
* Have tests where there are policies that are repealed and no superseding policy is found. Test we answer in an acceptable manner
* Have tests with repealed and superseded policies.
* If on the data policies should link to "potential other policies that are connected", test for that. I am guessing all parking-for-disabled policies should be connected and mention which one is the last standing.
* Test specifically for time periods when the currently repealed policy was in force (I am assuming we need to apply the policy THEN)

## Incident 2: model upgrade, 3x slower, Swedish compound-word search broken, 2 days to detect

Ask yourself:
- Which gate should a model upgrade pass? (Latency benchmark, retrieval eval on Swedish queries, golden set.)
- Compound words: which test queries? (Real Swedish terms from the 40k docs, e.g. "bostadstillägg", "färdtjänsttillstånd".)
- Which production signals catch it: p95 per model version, retrieval hit rate, empty-result rate?
- Does a model change go out as a canary, per tenant, with a rollback?

### Tests to regress this

* Add a plan on how to handle model upgrades, including a test bed where exhaustive testing could be sent. As we have an audit on production, we can have a period where we duplicate some queries, send them to the new model and we compare the results.
* Define a canary / AB testing rollout, and ideally involve active users that could validate. Some canary testers should be aware that a new model is being tested (while others shouldn't, to prevent bias). 
* Add compound words on some of the test cases, and add specific test cases dealing with compound words. Those could be validated on code, but also on the integration stage (or wherever the bulk of performance testing is carried)
* Define alarms and monitoring to observe these issues on integration and production (users reporting it without our knowledge is a failure on our part)
* Define a rollback policy in case a new model completely breaks specific use cases. Could we prepare a plan so the rollback is for specific users / organizations (maybe their use cases break the new model).

## Incident 3: stricter API broke two apps on follow-up messages; unclear error; a day to diagnose

Ask yourself:
- Contract tests: run the real off-the-shelf client libraries (OpenAI SDKs, LangChain, etc.) through multi-turn conversations against each build.
- Consumer-driven contracts: do the app teams publish the requests they actually send?
- Error contract: the error must name the rejected field and the API version. Test that.
- Change policy: is a stricter schema treated as a breaking change (versioning, deprecation window, release notes)?
- Why follow-up messages? (Probably extra fields on assistant or tool messages that the SDKs send back.) Test conversation history round-trips.

### Tests to regress this

* Add logging and debugging options and monitoring as the definition of done on the different features. If this goes badly, who is on call and how can we investigate it? (we might make the call that logging makes the API too slow or costly, but it should be a lever we can turn on/off on demand)
* Make sure the system works well with versioning, in case we have to roll back to a previous version. How long do we have to support old API versions?
* Investigate the issue, it is currently a bit confusing. 
* Force failures on the tests so we observe that the system fails gracefully and bubble up the error codes to the right places. 