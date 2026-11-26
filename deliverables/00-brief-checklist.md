# Brief coverage checklist

Each line from the brief, and where it is answered. Tick it when done.

## Deliverables (max 3 hours)

| ✓ | Brief asks for | Where |
|---|---|---|
| ☐ | What quality means for case workers, citizens and platform teams | 01 §1 |
| ☐ | Quality attributes ranked, with a reason for each rank | 01 §2 |
| ☐ | Risk map | 01 §3 |
| ☐ | Test where: unit, contract, integration, evaluations, prod monitoring, across the API and 5 services | 01 §4 |
| ☐ | Load, stress, failover tests, each with a pass condition | 01 §5 |
| ☐ | Fast pipeline signal the team trusts | 01 §6 |
| ☐ | What to monitor in production | 01 §7 |
| ☐ | Release criteria and gates | 01 §8 |
| ☐ | Strategy ≤ 4 pages | 01 |
| ☐ | 5–8 evaluation criteria (answers **and** guardrails), each with a judging method and threshold | 02 §1 |
| ☐ | ≥ 8 log lines turned into golden cases | 02 §2 |
| ☐ | Runnable harness, 5–10 golden cases against the log, CI-ready, with a run note | harness/ |
| ☐ | Short note on how AI tools were used | 03 |
| ☐ | "If I ran out of time, what I'd do next" | 01 §9 |

## Session preparation (not delivered, but asked)

| ✓ | Topic | Where |
|---|---|---|
| ☐ | Weekly numbers for leadership | 04 |
| ☐ | First 90 days | 04 |
| ☐ | Release recommendation reasoning (live scenario) | 04 |
| ☐ | Feature risk walkthrough (live exercise); practise on Summarize | features/Summarize.md |
| ☐ | Questions for them (team, platform, role) | 04 |

## What they look for → where it shows

| They look for | Where it shows |
|---|---|
| Quality framed around people and the harm a wrong answer does | 01 §1–3 |
| Evaluating non-deterministic AI answers | 02, harness |
| Testing a platform others build on: API, services, how they fail together | 01 §4, notes/TestForIncidents.md (Incident 3) |
| Performance, load, failover on a shared platform | 01 §5, notes/TestForUpscaling.md |
| Working engineering: a harness that runs, a sensible order of work | harness/, commit history |
| Release recommendations; a team that owns quality | 01 §6, §8; 04 |
