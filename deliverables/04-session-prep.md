# Session preparation (not part of the delivery)

Talking points per agenda area. Lines marked **(+)** are additions to my own notes. **Q** = a question to ask them.

---

## 1. v1 log: how I reached the verdicts, and where Fråga fails

**Method.** I stopped looking at the ratings early. I checked each answer against the excerpt of the policy for its topic.
- (+) The ratings were wrong 5 times: 3 harmful answers were rated up (L03, L07, L18) and 2 correct ones rated down (L08, L15). They feed triage, never pass/fail.

**Three types of failure, by layer:**

| Layer | What happened | Log lines |
|---|---|---|
| Retrieval | Repealed policy cited as current; source missed | L03, L13 (+ L05 probably) |
| Generation | **Right source cited, wrong details** (value, unit, rule branch) | L07, L16, L11 |
| Guardrails | False refusal; another case's personal data shown | L05, L18 |

- (+) **A correct citation does not prove a correct answer.** 3 of the 7 failures cite the right policy.
- (+) **L18 is an upstream failure.** Another case's data reached the model's context at all, so it's an access or index-scoping bug as well as a missed output guardrail.

**Non-determinism is clear, and big.**
- L07 and L19 are the same question with the same source (P-108), but one says "3 months" and the other "3 weeks".
- L03 and L20 handle the same repeal inconsistently.
- So testing is about permutations and repeated runs: the same query several times, plus variations of it.

**The error rate looks very high: 7 of 20 wrong.**
- (+) Be modest about it. With n = 20 the 95 % interval is roughly 15–59 %. The log tells me the *failure types*, not the *failure rate*.

---

## 2. Release decisions and who decides

**What I bring: confidence in the numbers, not just the numbers.**
1. **Against v1 and the golden set:** error rate per criterion, performance, against the previous release.
2. **On new cases:** varied and boundary cases, and recent production queries. How the build generalises beyond the cases we already know.
3. **On Summarize:** a new feature with less data, so lower confidence. I say so explicitly.

**Risk:** known and observed issues are ranked by likelihood × impact. Critical ones are promoted to blockers.

**Context from history.** I'd use data from previous releases to judge a regression.
- Example: if a previous release scored 80 % internally and users had no issues, the current 82 % reads differently.
- (+) This is calibration: how well does the internal score predict what users experience? Track it over releases.

**Reducing risk at launch:**
- Levers we can pull live: feature flags (e.g. Summarize off), per-tenant model pinning, rollback.
- A canary: a small user group or one municipality, with criteria to widen it or roll back.

**Who decides: it's a product decision.**
- I recommend and sign off on the quality risk. The product owner decides.
- We can ship when not everything is green, but every known risk is acknowledged and logged for the audit.
- (+) **One exception:** C1/C2 (privacy, repealed rules) are legal matters, so nobody can accept those risks. Compliance or the DPO has a veto.
- (+) **Fix in my notes:** I wrote "red flag if privacy leaks go beyond a threshold". Make it: **0 before release; in production, any single leak is an incident**, not a rate.
- (+) A platform release touches 5 apps. The decision can be per tenant: pinning lets one app stay on the old version while the platform ships.

---

## 3. The shared platform, beyond load

**Isolation between municipalities**
- Users and queries reach only the policies and cases they should.
- (+) Test it with per-municipality canary records, queried from every other tenant: expect zero hits.
- (+) Cache keys that leave out the tenant are a classic way this leaks.

**Data per municipality**
- Policies probably differ between municipalities, so each query must hit the right set.
- Golden tests are defined per municipality, with that municipality's unique cases covered.

**Q:** Are the databases fully isolated? Do municipal policies supersede general or national ones? (If they do, precedence is a new class of retrieval test.)

**Staggered release:** roll shared changes out to one municipality first, then the rest.

**Audit:** audit data is visible only to the right municipality's people, and contains no privacy breaches itself.

**(+) Contracts:** each app publishes the API calls it depends on, and the platform's CI runs all five apps' contract tests. This is the fix for Incident 3.

**(+) Fairness:** per-tenant quotas and noisy-neighbour tests. One tenant's load or bad input must not degrade the others.

**Ownership is shared:**
- The platform team owns the framework and availability.
- App teams own their features and their own golden cases.
- QA maintains the golden-set framework and quality bar, and signs off on the quality and performance risk.

---

## 4. Evaluation criteria and thresholds

**Thresholds are set by impact.**
- Critical harm (C1, C2) tolerates zero failures.
- Others are informed by previous incidents.
- New areas (Summarize) start from estimates that we tune with data.

**Criteria are a guideline and a conversation.** They move with the risk we can accept for a given release. But they never move under release pressure: tune them between releases.

**Non-determinism means we're never completely sure.**
- Rerun cases, with small variations, as far as the hardware allows, and report probabilities rather than a single pass or fail.
- Rerun recent production queries that share markers (values, policies) with the changed area.
- (+) **Rule of three:** 0 failures in *n* runs still allows a true failure rate of up to about 3/*n* (≈ 6 % for 50). That's why C1 and C2 also have a runtime guardrail and production monitoring.

**When a result lands just below a threshold (e.g. C4 at 94 % vs 95 %):**
1. Which cases failed? New ones or known ones?
2. Is it variance? Rerun and check the flip rate.
3. Is it a regression against the previous release?
4. The product owner makes the decision, records it, and attaches a mitigation (a flag or a monitor).
- For C1/C2 there is no "just below": it blocks.

**Q:** Can tests share the production GPUs, e.g. off-peak? Or do we need isolated GPUs so testing doesn't affect users? (This sets how many reruns we can afford.)

---

## 5. Harness: walkthrough and growth

**Today:** a simple, deliberately limited harness.
- Golden cases → pattern checks plus a status check on each cited policy.
- Recorded mode fails CI only if the harness disagrees with the human label, so it tests the evaluator.
- Demo: `python harness/fraga_eval.py`

**Known limitations, which I raise myself:**
- Partial strings match: "114 days" passes a check for "14 days". (Fix: match on word boundaries.)
- No check for omissions or extra facts.
- Negation: "not 1,800 SEK" passes. (+) Sentiment analysis isn't the right tool here. Use structured output (the model returns the value as a field), entailment (NLI) checks, or a judge model.
- (+) The 9/9 agreement is on cases written knowing the answers, so it's overfit. Live mode is the real test.

**How it grows into live mode:**
1. (+) Call the candidate build through the OpenAI SDK instead of reading the log. This doubles as a contract test.
2. More cases, each run several times, with variations.
3. Compare against previous runs. (+) Store the model, index and commit versions with each run: that's the audit evidence.
4. Dynamic sets built from production queries.
5. Better judging: showing doubt, and the correct data per policy. (+) Calibrate the judge against people (≥ 90 % agreement).
6. Municipality-specific and audit tests.
7. Boundary variants generated from each policy's criteria (exactly 85, exactly 3 km).
8. Modified policy tables to create edge cases (repeal chains, conflicting versions).

---

## 6. Weekly numbers for leadership

**Release and pipeline (per release / week)**

| Number | Target |
|---|---|
| Safety violations (C1/C2) | 0 |
| Expert agreement with our verdicts (% of a sample) | ≥ 90 % |
| Golden-set pass rate, vs last week and last release | ≥ threshold, no regression |
| Performance: p95 at peak, per tenant | ≤ 8 s |
| Pipeline: PR time, nightly time, flaky rate, test-farm utilisation | ≤ 12 min, ≤ 60 min, < 2 % |
| Open issues by severity, and mean age | trend down |

**Production**

| Number | Target |
|---|---|
| Uptime / error budget remaining | 99.5 % |
| Critical issues found (and time to detect) | 0 / minutes |
| % thumbs down (+ rating coverage) | trend, triage only |
| Expert audit accuracy on a production sample | ≥ 95 % |

(+) For leadership, pick ~6 and show the trend with a red/amber/green status. The full list is for the team.

---

## 7a. First 90 days: short version (v2 launches around day 56)

| Period | Focus |
|---|---|
| **Days 0–30** | Listen and set a baseline: run the test cases plus production examples on the new model. (+) First load test at 40k docs (the biggest unknown; its fixes take weeks). Split the pipeline into tiers, quarantine flaky tests, C1/C2 in PR checks. |
| **Days 31–56** | Expensive tests at each milestone, every two weeks after a certain point: performance, load, production-like setups (municipality split, failover). (+) Go/no-go criteria agreed in writing by about week 6. A dry-run release with the full evidence pack. Rollback plan and staggered rollout ready. |
| **Days 57–90** | Roll out to specific groups, told in advance, and iterate on the issues. Keep the old system available for a period, ideally with both models available. (+) Onboard the other 4 apps' golden sets; lower test cadence where tests stay green. |

**Must be true before launch:** load and failover results, C1/C2 gating, the evidence pack, rollback. **Can wait:** coverage targets, generated "unknown scenario" tests, cadence tuning.

---

## 7b. First 90 days: detailed version (v2 launches around day 56)

### Guiding principles (say these first)
- **Surface the biggest unknowns first.** Load at 40k docs, municipality isolation and Summarize all have fixes that take weeks.
- **Launch is a canary, not a big bang.** Day 56 starts a staggered rollout.
- **Every production issue becomes a test case.** That is how the golden set grows after launch.
- **Leave the team owning quality.** Tests, monitors and evidence are part of the definition of done, not QA's job.

### Weeks 1–2: Listen and set a baseline
- **Meet:** PO, platform team, the 4 app teams, compliance / DPO, the auditor contact. Sit with a case worker during the 08:30 peak.
- **Close the questions that change numbers:** workload (Q4/Q8), data-centre setup (Q7), how repeals are recorded (Q16), municipality isolation, GPU sharing for tests.
- **Baseline:** run the golden cases plus recent production examples on the v2 model, several runs each. This gives the first real error rate per criterion.
- **Quick wins:** quarantine flaky tests; put C1/C2 into PR checks.
- **Exit:** baseline report, updated risk map, weekly numbers agreed with leadership.

### Weeks 3–4: Foundations
- **Live-mode harness:** N runs per case; results stored with model, index and commit versions.
- **Golden set grown to ~50–100 cases** with policy experts: per municipality, boundaries, repeal chains.
- **First load test at 40k docs**, as early as the environment allows.
- **Isolation tests:** canaries per municipality, and who can see which audit logs.
- **Tiered pipeline:** PR checks ≤ 12 min; nightly runs against the live model.
- **Exit:** first weekly report to leadership; load-test findings, each with an owner and a date.

### Weeks 5–6: Harden and agree the gate
- Failover, noisy neighbour, contract tests from all 5 apps.
- Summarize evaluations reviewed with experts; judge model calibrated against people.
- EU AI Act classification answered by legal.
- **Go/no-go criteria signed in writing by the PO and compliance by the end of week 6. This is the key milestone.**
- A dry-run release that produces the full evidence pack.
- **Exit:** signed criteria; a rehearsal release an auditor could trace end to end.

### Weeks 7–8: Launch readiness
- Full milestone run: load, stress and soak on a production-like setup with the municipality split.
- **Rollback rehearsed:** actually roll back in staging, and time it.
- **Canary plan:** one municipality, or a group of case workers told in advance. The old system stays available. Criteria for widening and for rolling back are written down.
- **Go/no-go meeting around day 52:** I recommend, the PO decides, risks are logged.

### Weeks 9–10: Staggered rollout
- Widen municipality by municipality while the criteria hold: no C1/C2 issues, expert-audit accuracy on track, p95 within target at the real peak.
- Daily triage for the first 2 weeks; each issue becomes a golden case within a few days.
- Summarize stays behind a flag that can be switched off per municipality.

### Weeks 11–13: Steady state
- Retire v1 once its exit criteria are met.
- Onboard the other 4 apps' golden sets onto the framework.
- Lower test cadence where tests stay green; Summarize steps down after 4 clean weeks.
- Retrospective; next-quarter plan (dynamic sets from production, generated edge cases).

### If they push back
- **"What do you cut if load testing finds a capacity problem?"** Cut scope, not safety: fewer municipalities in the canary, Summarize behind its flag, a slower rollout. Never cut C1/C2 gating, rollback or the evidence pack.
- **"How do we know it worked at day 90?"** v2 live in all municipalities with no C1/C2 incidents; expert agreement ≥ 90 %; PR pipeline ≤ 12 min with flaky tests < 2 %; an evidence pack for every release; app teams adding golden cases without me.
- **Biggest risk to the plan:** access to experts. Without them the golden set doesn't grow, so ask for it in week 1.

**Must be true before launch:** load and failover results, C1/C2 gating, the evidence pack, a rehearsed rollback. **Can wait:** coverage targets, generated "unknown scenario" tests, cadence tuning.

---

## Questions for them

- Are the municipalities' databases fully isolated? Do municipal policies supersede general ones?
- Can tests share the production GPUs (off-peak)? Is there a production-like staging environment?
- Who signs off releases today, and what does the auditor expect to see?
- Who owns each app's evaluations today?
- Do we have access to policy experts or case workers for regular review?
