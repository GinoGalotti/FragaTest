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

We will aim to be as data driven as possible, measuring the current metrics and the impact of changes. 

For that, we can add some performance tests on code, but also have regular runs of performance tests on "real data" which can quickly inform the team when something is changing. If we can run it often enough, it is easier to triage when a change can cause an impact.

Performance relies on regular testing. This is a non-deterministic application, so we need to gather enough data points to create trends and understand deviation. 

This is challenged by how much we can spend on testing (and how much of our GPU quota we can access for testing), and that should fluctuate during development. Early on a feature we just want to catch if we are very far off from our targets, while closer to a release we can be more strict with our performance metrics. 

### Start with what we know

We have current usage and load on V1. If we extrapolate the numbers, assume a similar load spread and create likely and worst case scenarios, how do we stand? Test that. 

* Produce "as valid as possible" dummy policies with similar repeal cases and connections to fill an environment and measure how it affects our speed. 
* Measure the delta caused by more repealed and connection between policies. Having 30k policies, how long does it take to consult something that clearly touches an area with 1 policy, 10 repealed and 1 current policy, or 20 connected ones. Produce data to calculate projections.
* Measure the impact on improving the platforms and hardware. If we double the GPU, do we have the same speed with double the load? Do we have more speed on same load? 
* Test the load balancer and the rules on high load. Do we stagger the queries, limit the effort to offer faster answers (have stricter rules for more costly models)? 

### Discover what we don't know

Understand the new users and policies that will be added. Do we have new cases? Things to check:

* Format of the new policies, language, etc.
* Usage from the new users. Are they querying things differently?
* Are policies grouped? Can all users access all policies? Can we partition the data in a way that we limit the contexts that different use cases create? If so, test for those partitions and validate it.


### Validate the optimizations

Higher usage means it is more relevant to focus on ways to optimize the application. 
* Cached answers: especially if we see most new users ask the same queries
* Hierarchy of policy retrieval: maybe some policies are asked more often so we should have a faster access to them
* Better model balancing: specific groups might often ask simple questions and could be defaulted to simpler models

I am NOT an optimization engineer, but if we are going to invest on any of those solutions we should test that they work and ideally measure the impact. That way we can use the data to inform where can we get a bigger return. 
