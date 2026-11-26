# Testing the scale-up from v1 to v2

How we test for the challenges of moving from v1 to v2.

## The numbers

| Dimension | v1 | v2 | Factor |
|---|---|---|---|
| Case workers | 150 | 1,200 | 8x |
| Peak users (08:30–09:30) | ? | ~400 (Fråga alone) | see Q4 |
| Policy documents | 3,000 | 40,000 | ~13x |
| Features | Q&A | Q&A + Summarize | new |
| Tenants on the platform | 5 apps | 5 apps | shared GPUs, 2 DCs |

> Note: the document growth is ~13x (40,000 / 3,000), not 15x as I first wrote in the pillars.

## Areas and questions

**Retrieval quality at 13x the documents**
- More near-duplicates, old versions and conflicting rules. Does precision drop? How do you measure it? (Recall@k on a labelled set.)
- More repealed documents: the Incident 1 risk grows.

**Latency and throughput**
- Workload model: users → requests per second at peak. Where do the numbers come from (v1 logs, extrapolated)?
- Does retrieval latency grow with index size? Summarize prompts are long: what does that do to GPU time?

**Shared platform**
- Noisy neighbour: Fråga's peak combined with the other 4 apps' peaks.
- Fair share and quotas: can one tenant starve the others?

**Failover**
- Lose one DC at peak: does the other hold the full load and still meet p95 ≤ 8 s?
- Lose a single service (retrieval, guardrails, audit log): degrade or fail? If audit logging is down, do we still answer?

**Ingestion**
- Time to load 40k documents; time for an update or repeal to reach answers.

**New users, new questions**
- 8x the users means more departments and topics, so new question types. How do you find them early? (Pilot logs, a beta group, topic clustering.)
- Which v1 golden cases still hold, and which need v2 variants?

## Test plan skeleton

| Test | Workload / scenario | Pass condition | Environment | Cadence |
|---|---|---|---|---|
| | | | | |
