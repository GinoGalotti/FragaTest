# Quality Strategy — Fråga v2 on the shared AI platform

> Brief: max 4 pages, ~90 min. Template: each section lists what the brief asks for (**Brief**) and the questions to answer (**Ask yourself**). Delete the prompts once written.

## 1. What quality means

**Brief:** quality for case workers, citizens, and the teams that build on the platform.

| Who | What "good" means for them | Harm when it goes wrong |
|---|---|---|
| Case worker (1,200 in v2) | | |
| Citizen (indirect user) | | |
| App teams on the platform (Fråga + 4 others) | | |
| Auditor / municipality | | |

Ask yourself:
- What is the worst realistic harm? (Example: a citizen is denied support because of a repealed rule, as in Incident 1.)
- How do you turn "No embarrassing answers. Ship on time." into something you can measure?
- When the two goals conflict, which wins, and who decides?

## 2. Quality attributes, ranked

**Brief:** rank them and give a reason for each rank.

| Rank | Attribute | Why this rank | How we measure it |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| … | | | |

Candidates: factual correctness and grounding, currency (no repealed rules), privacy (P-107), safe refusal and honest uncertainty, API compatibility and stability, latency (p95 ≤ 8 s), availability (99.5 %), auditability, isolation between tenants (noisy neighbours), Swedish language handling, cost.

Ask yourself: what are you ranking *below* availability or latency, and can you defend that in the session?

## 3. Risk map

**Brief:** a risk map.

| ID | Risk | Likelihood (1–5) | Impact (1–5) | Score | Evidence (incident / log line) | Mitigation (test, gate or monitor) |
|---|---|---|---|---|---|---|
| R1 | | | | | | |

Ask yourself:
- Does each incident and each failing log line appear as a risk?
- Are risks that are new in v2 covered (40k docs, 1,200 users, Summarize)?
- Are shared-platform risks covered (other apps, GPU contention, a model upgrade affecting every tenant)?

## 4. What we test where

**Brief:** unit, contract, integration, evaluations, production monitoring — across the API and the 5 services behind it.

| Layer → / Service ↓ | Unit | Contract | Integration | Evaluations | Prod monitoring |
|---|---|---|---|---|---|
| Public API (OpenAI-compatible) | | | | | |
| Model gateway | | | | | |
| Retrieval | | | | | |
| Guardrails | | | | | |
| Ingestion | | | | | |
| Audit log | | | | | |

Ask yourself:
- Contract tests: who are the consumers? Do the off-the-shelf OpenAI client libraries count as consumers (Incident 3)?
- What runs on each commit, on each PR, nightly, on demand, and before a release (your pyramid / cadence pillar)?

## 5. Proving the service levels (load, stress, failover)

**Brief:** load, stress and failover tests, with a pass condition for each.

| Test | Scenario / workload model | Pass condition | Environment | Cadence |
|---|---|---|---|---|
| Load (peak hour) | | p95 ≤ 8 s, error rate ≤ … | | |
| Stress (find the limit) | | | | |
| Soak | | | | |
| Failover (lose one DC) | | | | |
| Noisy neighbour (other 4 apps at peak) | | | | |
| Ingestion at 40k docs | | | | |

Ask yourself:
- How do you get from users to requests per second? (400 users starting work 08:30–09:30, questions per user, think time.)
- Does the 8 s apply to Summarize, and to streamed answers? (See notes/OpenQuestions.md.)
- What does 99.5 % allow? (≈ 3.6 h of downtime a month.) Is failover expected to happen within that budget?

## 6. A fast pipeline the team trusts

**Brief:** bring the pipeline to a fast signal the team trusts.

Today: 41 % unit coverage, 220 end-to-end tests, 12 % flaky (≈ 26 tests), 38 min.

| Stage | Trigger | Time budget | What runs | Blocks merge? |
|---|---|---|---|---|
| Local | save / pre-commit | seconds | | no |
| PR | pull request | 10–15 min | | yes |
| Nightly | schedule | ≤ 60 min | | reports |
| On demand | schedule / pre-release | | perf, failover, localisation | release gate |

Ask yourself:
- Flaky tests: quarantine, fix or delete? Who owns that, and by when?
- How does test selection by changed area work in practice?
- With no QA and 6 engineers, how does the team own quality? (The session asks this.)

## 7. Production monitoring

Ask yourself:
- Which signals would have caught Incident 2 within minutes rather than 2 days? (Latency per model version, retrieval hit rate on Swedish queries.)
- Do you sample answers in production for online evaluation? How do you handle privacy?
- Thumbs ratings: what is the coverage, and how far can you trust them? (See notes/TestForCurrentLog.md.)
- What is alerted, and what goes on a dashboard?

## 8. Release criteria and gates

| Gate | Criterion | Evidence for the auditor | Who signs off |
|---|---|---|---|
| | | | |

Ask yourself:
- What blocks a weekly release, and what blocks the v2 launch?
- What evidence can an external auditor trace (test run, model version, dataset version, sign-off)?
- What is the rollback path, and are canary releases or feature flags used?

## 9. If I had more time

What you would do next, in order.
