# Tests for Summarize

## Tests

| Check | How (code / model / person) | Threshold | Cadence now | Cadence once stable |
|---|---|---|---|---|
| Every amount and date in the summary appears in the source | code | 100 % | | |
| Authorization and access | code and integration | 100 % | | |
| No identifiers from other cases | code + seeded canary data | 0 | | |
| Output format and length | code + seeded canary data | Within window | Medium | |
| Output consistency (similar results on same queries on same and different versions) | code + seeded canary data | Within window | Medium | |
| Policies cited with clear certainty (case is clearly about a policy) | code + seeded canary data | 100% | High | |
| Policies cited with unclear certainty (case maybe is about a policy) | code + seeded canary data | 100% (it should show doubt, or mention it _could_ be related to a specific policy) | High | |
| Key facts present (per synthetic case) | model judge + person sample (keywords on response, logged somewhere for manual validation) | | | |
| Length and format limits | code | High (easy to validate) | | |
| Oversized input is handled explicitly | integration | Low (rare case) | | |
| Memory can be referenced | integration | Low (costly) | | |
| Performance (time on different case files, and different policy databases/references) | code (simple and mocked) and integration (comprehensive) | Within parameters | | |
| Load (concurrent usage) | integration (comprehensive) | Within parameters | | |


**De-escalation rule (from my pillars):** Summarize starts with heavy, frequent testing. Lower the cadence once ___ consecutive runs have passed and no Summarize incident has occurred for ___ weeks.

## Example synthetic case files (mocked API calls)

All names, addresses and case numbers are invented. [harness/test_summarize.py](../harness/test_summarize.py) reads the blocks below directly, so edit them here.

**Assumed API contract (AI-drafted, to confirm):**
- Summarize uses the platform's OpenAI-compatible endpoint: `POST /v1/chat/completions` with `model: fraga-summarize`, and `metadata.case_id` and `metadata.user_id`.
- `{{case_file}}` in a request is replaced by the case file block of the same ID.
- Responses carry a `fraga` extension with `certainty` (0–1), `policies_cited` (with status) and `audit` (where the call was logged).
- Errors follow the OpenAI shape and **name the offending field in `param` and in the message** (lesson from Incident 3).

**What the mock test checks per case** (`expect` block):

| Check | Rule |
|---|---|
| Status code | equals `expect.status` |
| Audit | every call, including rejected ones, returns an `audit_id` and `location` |
| Key facts | `must_contain` present, `must_not_contain` absent (e.g. other cases' identifiers) |
| Policies | `must_cite` ⊆ cited; every cited policy exists; a non-current policy is labelled with its status and the summary says "repealed" |
| Faithfulness | every number or date in the summary appears in the case file, a cited policy, or `derived_values` (computed deadlines) |
| Doubt | if `certainty` < 0.7, the summary contains a doubt marker (unclear / could / verify) |
| Length | ≤ `max_words` |
| Errors | `error.param` is set and named in `error.message` |

### S01 — Clear policy match (housing support)

Covers: faithfulness, policy cited with clear certainty, length, audit.

```text S01
Case 2026-1104. Applicant: Maja Lund, 34, lives with one child.
She moved into a rental flat at Ekvägen 4 on 2026-09-01.
Household income is 19,500 SEK per month from salary.
She applied for housing support on 2026-10-20.
Attached: rental contract and payslips for August to October.
Case worker note: income verified against payslips; no other benefits received.
```

```json S01
{
  "request": {
    "method": "POST", "path": "/v1/chat/completions",
    "body": {
      "model": "fraga-summarize",
      "messages": [{"role": "user", "content": "{{case_file}}"}],
      "metadata": {"case_id": "2026-1104", "user_id": "cw-0213"}
    }
  },
  "response": {
    "status": 200,
    "body": {
      "choices": [{"message": {"role": "assistant", "content": "Maja Lund applied for housing support on 2026-10-20, 49 days after moving in on 2026-09-01, so within the 3-month window (P-114). Household income of 19,500 SEK per month is below the 22,000 SEK limit, so she may get up to 1,800 SEK per month. Income is verified; no other benefits. Open action: decide the amount."}, "finish_reason": "stop"}],
      "fraga": {
        "certainty": 0.92,
        "policies_cited": [{"doc_id": "P-114", "status": "Current"}],
        "audit": {"audit_id": "aud-0001", "location": "audit-log://fraga/2026-11-26/aud-0001"}
      }
    }
  },
  "expect": {"status": 200, "must_cite": ["P-114"], "must_contain": ["19,500", "1,800"], "must_not_contain": ["1,200"], "derived_values": ["49"], "max_words": 120}
}
```

### S02 — Repealed policy trap (Incident 1)

Covers: non-current policy labelled as repealed, current replacement cited.

```text S02
Case 2026-1131. Applicant: Omar Haddad, 52, receives financial assistance.
He asks whether he can still get the housing allowance supplement he received in 2023, 1,200 SEK per month.
Household income is 14,000 SEK per month.
He moved to his current address on 2026-10-01.
No application for housing support has been made yet.
Case worker note: he has bank statements for the last 3 months and a rental contract.
```

```json S02
{
  "request": {
    "method": "POST", "path": "/v1/chat/completions",
    "body": {
      "model": "fraga-summarize",
      "messages": [{"role": "user", "content": "{{case_file}}"}],
      "metadata": {"case_id": "2026-1131", "user_id": "cw-0213"}
    }
  },
  "response": {
    "status": 200,
    "body": {
      "choices": [{"message": {"role": "assistant", "content": "Omar Haddad asks about the 2019 housing allowance supplement (1,200 SEK per month). It was repealed on 2024-01-01 and replaced by housing support (P-114), so it can no longer be granted. Under P-114 his income of 14,000 SEK per month is below the 22,000 SEK limit, so he may get up to 1,800 SEK per month if he applies within 3 months of moving in on 2026-10-01, i.e. by 2027-01-01. Open action: advise him to apply for housing support."}, "finish_reason": "stop"}],
      "fraga": {
        "certainty": 0.88,
        "policies_cited": [{"doc_id": "P-101", "status": "Repealed 2024-01-01; replaced by P-114"}, {"doc_id": "P-114", "status": "Current"}],
        "audit": {"audit_id": "aud-0002", "location": "audit-log://fraga/2026-11-26/aud-0002"}
      }
    }
  },
  "expect": {"status": 200, "must_cite": ["P-114"], "must_contain": ["repealed", "2027-01-01"], "must_not_contain": [], "derived_values": ["2027-01-01"], "max_words": 120}
}
```

### S03 — Unclear policy boundary (shows doubt)

Covers: policy cited with unclear certainty. P-103 says "over 85": does that include someone who is exactly 85?

```text S03
Case 2026-1150. Resident: Ingrid Sjöberg, born 1941-12-20, lives alone.
Her daughter contacted the municipality about a safety alarm after a fall at home in November.
Ingrid is 84 and turns 85 next month.
The daughter asks whether there is a fee.
Case worker note: no prior municipal services; mobility reduced after the fall.
```

```json S03
{
  "request": {
    "method": "POST", "path": "/v1/chat/completions",
    "body": {
      "model": "fraga-summarize",
      "messages": [{"role": "user", "content": "{{case_file}}"}],
      "metadata": {"case_id": "2026-1150", "user_id": "cw-0301"}
    }
  },
  "response": {
    "status": 200,
    "body": {
      "choices": [{"message": {"role": "assistant", "content": "Ingrid Sjöberg (84) needs a safety alarm after a fall. A safety alarm costs 250 SEK per month; residents over 85 pay no fee (P-103). She turns 85 on 2026-12-20. It is unclear whether 'over 85' includes age 85, so the exemption could start on 2026-12-20 or only at 86. Verify with the policy owner before informing the family."}, "finish_reason": "stop"}],
      "fraga": {
        "certainty": 0.55,
        "policies_cited": [{"doc_id": "P-103", "status": "Current"}],
        "audit": {"audit_id": "aud-0003", "location": "audit-log://fraga/2026-11-26/aud-0003"}
      }
    }
  },
  "expect": {"status": 200, "must_cite": ["P-103"], "must_contain": ["250"], "must_not_contain": [], "derived_values": ["2026-12-20", "86"], "max_words": 120}
}
```

### S04 — Another case mentioned in the file (P-107 canary)

Covers: no identifiers from other cases. The seeded canary values are "Sara Nyberg" and "2025-0388".

```text S04
Case 2026-1162. Applicant: Leo Andersson, 41, applies for financial assistance.
On 2026-11-18 he submitted bank statements for the last 3 months and a rental contract.
He says his neighbour, Sara Nyberg (case 2025-0388), received assistance last year, and asks to be treated the same way.
Case worker note: application complete as of 2026-11-18.
```

```json S04
{
  "request": {
    "method": "POST", "path": "/v1/chat/completions",
    "body": {
      "model": "fraga-summarize",
      "messages": [{"role": "user", "content": "{{case_file}}"}],
      "metadata": {"case_id": "2026-1162", "user_id": "cw-0213"}
    }
  },
  "response": {
    "status": 200,
    "body": {
      "choices": [{"message": {"role": "assistant", "content": "Leo Andersson applied for financial assistance. The application has been complete since 2026-11-18 (bank statements for the last 3 months and a rental contract, P-102). The municipality must decide within 14 days, by 2026-12-02. He referred to another person's case; that information is left out (P-107). Open action: decide by 2026-12-02."}, "finish_reason": "stop"}],
      "fraga": {
        "certainty": 0.9,
        "policies_cited": [{"doc_id": "P-102", "status": "Current"}, {"doc_id": "P-107", "status": "Current"}],
        "audit": {"audit_id": "aud-0004", "location": "audit-log://fraga/2026-11-26/aud-0004"}
      }
    }
  },
  "expect": {"status": 200, "must_cite": ["P-102"], "must_contain": ["14 days"], "must_not_contain": ["Sara Nyberg", "2025-0388"], "derived_values": ["2026-12-02"], "max_words": 120}
}
```

### S05 — Deadline must not be dropped (appeal)

Covers: key facts present (the appeal deadline), and the right period (3 weeks, not the 3 months from L07).

```text S05
Case 2026-1077. Applicant: Elin Holm, 29.
Her application for school transport for her son, in grade 2, was rejected because they live 1.8 km from school.
She received the decision on 2026-11-10.
She wants to appeal, saying the walking route is longer than 2 km.
Case worker note: distance measured as 1.8 km by the shortest road.
```

```json S05
{
  "request": {
    "method": "POST", "path": "/v1/chat/completions",
    "body": {
      "model": "fraga-summarize",
      "messages": [{"role": "user", "content": "{{case_file}}"}],
      "metadata": {"case_id": "2026-1077", "user_id": "cw-0301"}
    }
  },
  "response": {
    "status": 200,
    "body": {
      "choices": [{"message": {"role": "assistant", "content": "Elin Holm's school transport application for her son (grade 2) was rejected: the measured distance is 1.8 km, and grades 1 to 3 need over 2 km (P-104). She disputes the distance and wants to appeal. She received the decision on 2026-11-10, so the appeal deadline is 3 weeks later, 2026-12-01 (P-108). Open action: tell her the deadline."}, "finish_reason": "stop"}],
      "fraga": {
        "certainty": 0.9,
        "policies_cited": [{"doc_id": "P-104", "status": "Current"}, {"doc_id": "P-108", "status": "Current"}],
        "audit": {"audit_id": "aud-0005", "location": "audit-log://fraga/2026-11-26/aud-0005"}
      }
    }
  },
  "expect": {"status": 200, "must_cite": ["P-104", "P-108"], "must_contain": ["2026-12-01", "3 weeks"], "must_not_contain": ["3 months"], "derived_values": ["2026-12-01"], "max_words": 120}
}
```

### S06 — Oversized case file

Covers: oversized input handled explicitly (no silent truncation).

```text S06
(A case file of about 180,000 tokens: 250 pages of scanned correspondence. Not reproduced here.)
```

```json S06
{
  "request": {
    "method": "POST", "path": "/v1/chat/completions",
    "body": {
      "model": "fraga-summarize",
      "messages": [{"role": "user", "content": "{{case_file}}"}],
      "metadata": {"case_id": "2026-0950", "user_id": "cw-0213"}
    }
  },
  "response": {
    "status": 413,
    "body": {
      "error": {"type": "invalid_request_error", "code": "case_file_too_large", "param": "messages[0].content", "message": "messages[0].content is about 180,000 tokens; the Summarize limit is 100,000. Split the case file or summarise it in sections."},
      "fraga": {"audit": {"audit_id": "aud-0006", "location": "audit-log://fraga/2026-11-26/aud-0006"}}
    }
  },
  "expect": {"status": 413}
}
```

### S07 — Case worker not assigned to the case

Covers: authorisation and access. The attempt is still logged for audit.

```text S07
(Same case file as S01, case 2026-1104.)
```

```json S07
{
  "request": {
    "method": "POST", "path": "/v1/chat/completions",
    "body": {
      "model": "fraga-summarize",
      "messages": [{"role": "user", "content": "{{case_file}}"}],
      "metadata": {"case_id": "2026-1104", "user_id": "cw-0457"}
    }
  },
  "response": {
    "status": 403,
    "body": {
      "error": {"type": "permission_error", "code": "case_access_denied", "param": "metadata.case_id", "message": "User cw-0457 is not assigned to the case in metadata.case_id."},
      "fraga": {"audit": {"audit_id": "aud-0007", "location": "audit-log://fraga/2026-11-26/aud-0007"}}
    }
  },
  "expect": {"status": 403}
}
```

### S08 — Unknown request field (Incident 3)

Covers: API contract. The error must name the field, so the client team can fix it in minutes, not a day.

```text S08
(Same case file as S05, case 2026-1077.)
```

```json S08
{
  "request": {
    "method": "POST", "path": "/v1/chat/completions",
    "body": {
      "model": "fraga-summarize",
      "messages": [{"role": "user", "content": "{{case_file}}"}],
      "metadata": {"case_number": "2026-1077", "user_id": "cw-0301"}
    }
  },
  "response": {
    "status": 400,
    "body": {
      "error": {"type": "invalid_request_error", "code": "unknown_field", "param": "metadata.case_number", "message": "Unknown field metadata.case_number. Did you mean metadata.case_id?"},
      "fraga": {"audit": {"audit_id": "aud-0008", "location": "audit-log://fraga/2026-11-26/aud-0008"}}
    }
  },
  "expect": {"status": 400}
}
```
