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

## Incident 2: model upgrade, 3x slower, Swedish compound-word search broken, 2 days to detect

Ask yourself:
- Which gate should a model upgrade pass? (Latency benchmark, retrieval eval on Swedish queries, golden set.)
- Compound words: which test queries? (Real Swedish terms from the 40k docs, e.g. "bostadstillägg", "färdtjänsttillstånd".)
- Which production signals catch it: p95 per model version, retrieval hit rate, empty-result rate?
- Does a model change go out as a canary, per tenant, with a rollback?

## Incident 3: stricter API broke two apps on follow-up messages; unclear error; a day to diagnose

Ask yourself:
- Contract tests: run the real off-the-shelf client libraries (OpenAI SDKs, LangChain, etc.) through multi-turn conversations against each build.
- Consumer-driven contracts: do the app teams publish the requests they actually send?
- Error contract: the error must name the rejected field and the API version. Test that.
- Change policy: is a stricter schema treated as a breaking change (versioning, deprecation window, release notes)?
- Why follow-up messages? (Probably extra fields on assistant or tool messages that the SDKs send back.) Test conversation history round-trips.
