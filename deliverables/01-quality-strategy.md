# Quality Strategy — Fråga v2 on the shared AI platform

**Question:** how do we make sure the platform is good enough for Fråga v2, and the other four applications, to launch on, and what does "good" mean?
**Short answer:** good means *a case worker can repeat an answer to a citizen without harm, and a team can build on the API without surprises*. We prove it with three things: evaluations that check answer patterns (not wording); contract, load and failover tests with numeric pass conditions; and a fast, trusted pipeline whose results become the auditor's evidence. Assumptions are listed in [notes/OpenQuestions.md](../notes/OpenQuestions.md).

## 1. What quality means

| For | Good means | Harm when it fails |
|---|---|---|
| **Citizens** (indirect) | Decisions based on current, correct rules; their data never shown in someone else's case | Denied support or a missed deadline because of a wrong rule; a privacy breach |
| **Case workers** (150 → 1,200) | Answers they can repeat: correct values, current policy cited, doubt shown when unsure; fast at 08:30 | Repeating a wrong answer (Incident 1); losing trust, so the tool is abandoned |
| **App teams** (Fråga + 4) | A stable, OpenAI-compatible API; errors that say what is wrong; no slowdown from other tenants | A day lost to an unclear breaking change (Incident 3) |
| **Municipality / auditor** | Every release traceable to its evidence; data stays in Sweden; P-107 enforced | Failed audit; contract breach (99.5 %, p95 ≤ 8 s) |

Leadership's goals, made measurable. **"No embarrassing answers"** = zero C1/C2 failures (privacy, repealed rules) and doubt shown on uncertain cases. **"Ship on time"** = weekly releases that pass automated gates without a manual heroics phase. When the two conflict, safety wins, but a narrow fix ships behind a flag rather than a whole release slipping.

## 2. Quality attributes, ranked

| # | Attribute | Why this rank |
|---|---|---|
| 1 | **Answer safety**: no other-case data (P-107), no repealed rule presented as current | Irreversible harm to citizens, legal exposure; both have already happened (L18, Incident 1) |
| 2 | **Correctness**: values, units, rule branch | 7 of 20 v1 answers were wrong; a wrong deadline harms citizens |
| 3 | **Honest uncertainty**: refuse or show doubt instead of guessing | The cheapest protection against unknown failures; makes 1–2 safer |
| 4 | **API stability for tenants** | Five apps depend on it; one breaking change cost two teams a day |
| 5 | **Availability** (99.5 %) | Contractual; an outage is visible, unlike a wrong answer, so it is lower harm |
| 6 | **Latency** (p95 ≤ 8 s) | Contractual, but a slow correct answer beats a fast wrong one |
| 7 | **Cost per answer / summary** | Shared GPUs; it constrains testing too (Q9) |

**Auditability and compliance are not ranked: they are a gate.** Without traceable evidence, nothing ships (§8).

## 3. Risk map

Likelihood (L) and impact (I) on a 1–5 scale; score = L × I. Evidence is from the brief and the log.

| ID | Risk | L | I | Score | Evidence | Main mitigation |
|---|---|---|---|---|---|---|
| R1 | Personal data from another case in an answer or summary | 4 | 5 | **20** | L18 (rated up) | C1 code check + seeded canaries in every tier; output guardrail; Summarize scoped per case |
| R2 | Repealed rule presented as current, worse with 13x the documents | 4 | 5 | **20** | Incident 1, L03 | C2 status check; ingestion test (repeal reaches the index); prod monitor |
| R3 | Wrong value or rule branch | 4 | 4 | **16** | L07, L11, L16 | C3 + C4; boundary cases |
| R4 | Peak load misses p95 8 s (8x users, 13x docs, shared GPUs, untested) | 4 | 4 | **16** | No load test since v1 | Load and stress tests, §5 |
| R5 | DC failover fails or exceeds the availability budget | 3 | 5 | **15** | Never tested | Failover test, §5 |
| R6 | API change breaks tenant apps | 3 | 4 | 12 | Incident 3 | Contract tests with real SDKs; error contract; versioning |
| R7 | Model upgrade regresses latency or Swedish retrieval | 3 | 4 | 12 | Incident 2 (2 days to detect) | Upgrade gate, shadow, canary, per-version monitoring |
| R8 | Summarize omits or invents facts | 3 | 4 | 12 | New, untested feature | Faithfulness and omission checks; extra cadence (§4) |
| R9 | Flaky pipeline means red gets ignored | 4 | 3 | 12 | 12 % flaky, 38 min | §6 |
| R10 | False refusals erode trust | 3 | 2 | 6 | L05 | C5 threshold |

## 4. What we test where

| Service ↓ / Layer → | Unit | Contract | Integration | Evaluations | Production monitoring |
|---|---|---|---|---|---|
| **Public API** | schema validation, error builder | **real OpenAI SDKs (Python, JS, .NET), multi-turn, per build**; errors name the field; versioned schema | auth per case (Summarize), rate limits | — | 4xx/5xx by client library and version; p95 per tenant |
| **Model gateway** | routing rules | model and version pinning per tenant | timeout, retry, fallback model | latency benchmark per model version | p95 and error rate per model version |
| **Retrieval** | status filter, chunking, Swedish compound splitting | — | index of 40k realistic docs (incl. repeal chains) | recall@k on a labelled set incl. compound words; C2 | empty-result rate; % citing non-current policy |
| **Guardrails** | PII and case-number detectors | — | end-to-end block path | C1, C5 on labelled sets | blocks/day; refusal-rate spikes |
| **Ingestion** | status and effective-date parsing | document metadata schema | repeal → index → answer within the SLA | — | ingestion lag; failed documents |
| **Audit log** | record format | — | every call logged, including rejections; survives failover | — | write failures (alert on any) |

**Evaluations:** six criteria (C1–C6) and golden cases from the log ([02](02-evaluation-design.md)), run on recorded and mocked answers per commit and against the live model nightly (5 runs per case). **Summarize** gets its own checks ([notes/TestForSummarize.md](../notes/TestForSummarize.md)): faithfulness (every number traces to the case or a policy), no other-case data, policy links with reasons, a length ratio, and doubt on unclear policy. It starts on the highest cadence and steps down after 4 clean weeks with no incident.

## 5. Proving the service levels

Workload model (assumptions Q4, Q8): **400 Fråga users at the 08:30–09:30 peak, ~5 questions each → ~0.6 req/s on average, 3x bursts → ~2 req/s**, plus the other four tenants' recorded peaks. Data: 40k documents including repeal chains. Mix: 80 % Q&A, 20 % Summarize (assumed). Environment: production-like, with Swedish DCs.

| Test | Scenario | Pass condition | Cadence |
|---|---|---|---|
| **Load** | 2x the projected peak, all 5 tenants, 1 h | p95 ≤ 8 s per tenant; errors < 1 %; GPU < 80 % | nightly (short), weekly (full) |
| **Stress** | ramp until it breaks | breaking point ≥ 2x peak; overload returns 429 with retry-after, never 5xx or a silent drop; recovers within 5 min | before milestones |
| **Soak** | peak load for 4 h | no p95 drift > 10 %; no memory or queue growth | weekly |
| **Failover** | kill one DC at peak | p95 ≤ 8 s again within 5 min; in-flight requests retried or cleanly failed; **no lost audit records**; failover stays in Sweden | monthly + before launch |
| **Noisy neighbour** | one tenant at 5x its own peak | other tenants' p95 ≤ 8 s (needs per-tenant quotas, Q8) | before launch |
| **Model upgrade** | new model vs the current one | p95 ≤ 1.2x the current one; compound-word recall not lower; golden set not lower | each upgrade |

Budget: 99.5 % allows ~3.6 h of downtime a month. A failover that takes 30 min uses 14 % of it, so it must be fast and rare.

## 6. A fast signal the team trusts

From one 38-minute pipeline to four tiers. A test's tier is set by its **risk covered** (incident regressions and C1/C2 always run first), **flakiness** and **greenness** (always green and low-risk → lower cadence).

| Tier | Trigger | Budget | What runs |
|---|---|---|---|
| Local | save / pre-commit | seconds | unit tests and recorded evaluations for the changed area |
| PR | pull request | ≤ 12 min | contract (real SDKs), C1/C2/C3 on recorded and mocked answers, critical end-to-end tests selected by changed files |
| Nightly | schedule | ≤ 60 min | full end-to-end suite, live-model evals (5 runs), short load test; results posted to the team channel |
| On demand | weekly / milestone | — | full load, stress, soak, failover; model-upgrade gate |

**Flaky tests (≈ 26 of 220):** quarantined out of the gating tiers on the first flake. The owner fixes or deletes each within 2 weeks, and the flaky rate is reported weekly (target < 2 %). **Coverage:** don't chase 41 % → X overall; require ≥ 80 % on the code that guards R1–R3 (guardrails, the status filter, API schema). **Ownership:** with no QA, quality is part of the definition of done: tests, logging and a monitor ship with each feature. A rotating release captain runs the gate, and the golden set is shared with the Fråga team (Q22).

## 7. What we monitor in production

Per tenant and per model version: p95 latency, availability, error rate by status code and **client library** (catches Incident 3 in minutes); **retrieval empty-result rate and compound-word query hit rate** (Incident 2); % of answers citing a non-current policy (target 0, Incident 1); guardrail blocks and refusal rate; certainty distribution; thumbs-down rate and **rating coverage**; ingestion lag; audit write failures; cost per answer and per summary. Alerts go to the on-call owner. A weekly person audit samples answers **including up-voted ones**, since ratings proved unreliable (L03, L07, L18 rated up).

## 8. Release criteria and gates

| Gate | Criteria |
|---|---|
| **Every weekly release** | C1 and C2 100 %; golden set ≥ 95 % (C3 100 %); contract tests with real SDKs green; p95 benchmark ≤ 1.2x the previous release; no open incident regression failing; evidence pack produced |
| **Model upgrade** | the weekly gate, plus the compound-word retrieval set and a shadow run on duplicated production queries, then a canary (5 % of users, 48 h) with rollback per tenant |
| **API change** | a stricter schema is a breaking change: new version, deprecation window, release notes to tenants |
| **v2 launch** | all of the above, plus load, stress, soak and failover passed at 40k docs; Summarize 100 % on C1, C2 and C6; a person sign-off from the Fråga product owner |

**Evidence for the auditor (every release):** commit SHA, model and index versions, evaluation and test results, load-test report, who signed off and when. Stored immutably and linked from the release. **Compliance, checked at each gate:** GDPR (personal data in case files, summaries and audit logs: minimised, access-controlled, with a defined retention period); P-107; data residency in Sweden, including during failover; **EU AI Act**: AI used by public authorities for access to public benefits may be classified as high-risk, so the classification needs verifying with legal before v2. If it is high-risk, human oversight, logging and accuracy documentation become launch criteria.

## 9. What I would do next

1. Confirm the open questions that change numbers: Q4/Q8 (workload), Q7 (DC setup), Q16 (repeal metadata), Q18 (API versioning).
2. Build the live-mode harness, with the Swedish compound-word and boundary variants.
3. Run the first load and failover test at 40k docs. It is the largest unknown, and its fixes take weeks.
4. Agree the weekly numbers with leadership and the golden-set ownership with the app teams.
