# Open questions

Questions raised during the exercise. Where we need an answer to move forward, we write an **assumption** and note its impact if it turns out to be wrong.
Status: `open` (no assumption yet) · `assumed` (we proceed on the assumption) · `answered` (by email from Advania).

## SLA and performance

**Q1. Peak hours and the 8 s p95.** Is it acceptable to miss 8 s at p95 during peak hours? Or only for questions that touch many documents?
- Assumption: _TBD_ · Status: open

**Q2. User-selected effort or certainty.** Can users choose effort or certainty (e.g. "triple-check the references")? If so, 8 s may be unrealistic for that mode.
- Assumption: No, users cannot choose. · Status: assumed

**Q3. Where the 8 s is measured.** Does it start when the API receives the call? Can users upload files, or only ask in plain text? If they can upload, is there a separate SLA for upload and processing (which depends on their setup)?
- Assumption: Measured from when the API receives the call. · Status: assumed

**Q4. (AI-added) Does the 400 peak users refer to v2?** v1 has 150 users, so we read "about 400 Fråga users at 08:30–09:30" as the v2 projection. What are the request rate and think time per user?
- Assumption: Yes, 400 is the v2 peak. · Status: assumed

**Q5. (AI-added) Streaming and Summarize.** Is the 8 s time to first token or to the full answer? Does it apply to Summarize on long case files?
- Assumption: _TBD_ · Status: open

**Q6. (AI-added) How 99.5 % availability is measured.** Per application or per platform, per month? Do planned maintenance windows count? (99.5 % ≈ 3.6 h of downtime a month.)
- Assumption: Planned maintenance does not count against the 99.5 %. · Status: assumed

**Q7. (AI-added) Data centre setup.** Do the two DCs run active-active or active-passive? What is the target recovery time? Are in-flight requests retried?
- Assumption: _TBD_ · Status: open

**Q8. (AI-added) Other tenants.** What load do the other 4 applications generate, and when do they peak? Are there GPU quotas or priority per tenant?
- Assumption: No per-tenant GPU quotas or priority. · Status: assumed

**Q9. GPU cost and quota.** Are there consumption limits, e.g. a maximum GPU time or cost per query? How much of the GPU capacity can testing use, compared with production? Do tests run on the production setup?
- Assumption: We need to measure cost per query (in production and in testing). · Status: assumed

## Answer quality

**Q10. Language.** Only Swedish, or Swedish and English? Translation may add processing time.
- Assumption: One language only (Swedish). · Status: assumed

**Q11. Target thumbs-down rate.** Is there a commitment on how often answers can be rated down? We need a process to collect ratings in production and during development, and to classify the failure (wrong policy, wrong amount, "I don't know"). For me, "no embarrassing answers" means asking for confirmation instead of hallucinating.
- Assumption: _TBD_ · Status: open

**Q12. (AI-added) Rating coverage and reliability.** What share of answers get rated (5 of 20 in the sample have none)? Are ratings reviewed? In the sample, some wrong answers are rated up (see notes/TestForCurrentLog.md).
- Assumption: _TBD_ · Status: open

**Q13. (AI-added) What guardrails check today.** Input, output or both? What is their current false-refusal rate (L05)?
- Assumption: _TBD_ · Status: open

**Q14. Personalisation.** Can users personalise how Fråga answers them (more concise, more detailed, etc.)? Or are the response guidelines set for the whole system, and enforced by our tests?
- Assumption: No personalisation; guidelines are system-wide. · Status: assumed

**Q15. Memory.** Does a query carry memory of the user's earlier questions, or is each query independent?
- Assumption: No memory between conversations. · Status: assumed
- AI note, please confirm: Incident 3 mentions follow-up messages, so within one conversation the earlier messages are sent with each request. Does "no memory" mean only between conversations?

## Documents and ingestion

**Q16. (AI-added) How repeal is recorded.** Is policy status (current/repealed, replaced by) a metadata field that retrieval can filter on? How quickly does a repeal reach the index?
- Assumption: _TBD_ · Status: open

**Q17. (AI-added) The 40k documents.** What formats and languages? Do several versions of the same policy exist? How often do documents change? How long does a full re-index take?
- Assumption: _TBD_ · Status: open

## Platform and process

**Q18. (AI-added) API change policy.** Is there versioning or deprecation? Which client libraries and versions do the consuming apps use (Incident 3)?
- Assumption: The API must be versioned. · Status: assumed

**Q19. (AI-added) Model upgrades.** Who triggers them? Are model versions pinned per application? Is a canary or shadow rollout possible (Incident 2)?
- Assumption: A canary rollout is possible, and the platform team owns it. · Status: assumed

**Q20. (AI-added) Environments and data.** Is there a staging environment like production? Can we use anonymised production logs as test data (GDPR)? (See also Q9: do tests share production GPUs?)
- Assumption: _TBD_ · Status: open

**Q21. (AI-added) Audit evidence.** What format does the external auditor expect, and how long must it be kept?
- Assumption: _TBD_ · Status: open

**Q22. (AI-added) Ownership.** Who owns the golden datasets and evaluations: the platform team or each app team?
- Assumption: _TBD_ · Status: open

**Q23. Access to users and experts.** Do we have access to real users or policy experts? Can they periodically review a sample of logged answers with us (especially for the new Summarize feature)?
- Assumption: Yes. · Status: assumed
