"""Mocked Summarize API cases, read from notes/TestForSummarize.md.

Illustrative: the responses are mocked, so this shows the shape of the checks
we would run against the real endpoint (PR: mocked; nightly: live model).
"""
import copy
import json
import re

import pytest

from fraga_eval import POLICIES, ROOT, load_csv, normalise

DOC = ROOT / "notes" / "TestForSummarize.md"
POLICY = load_csv(POLICIES, "doc_id")
DOUBT = ("unclear", "could", "verify", "not certain")
NUMBER = re.compile(r"\d+(?:[.,]\d+)*(?:-\d+)*")


def load_cases():
    text = DOC.read_text(encoding="utf-8")
    files = dict(re.findall(r"```text (S\d+)\n(.*?)```", text, re.S))
    cases = []
    for cid, raw in re.findall(r"```json (S\d+)\n(.*?)```", text, re.S):
        case = json.loads(raw)
        case["id"], case["case_file"] = cid, files[cid]
        cases.append(case)
    return cases


CASES = load_cases()


def numbers(text):
    return set(NUMBER.findall(normalise(text)))


def check(case):
    """Return a list of failures for one mocked request/response pair."""
    expect, resp = case["expect"], case["response"]
    body, failures = resp["body"], []
    if resp["status"] != expect["status"]:
        failures.append("status %s != %s" % (resp["status"], expect["status"]))
    audit = body.get("fraga", {}).get("audit", {})
    if not (audit.get("audit_id") and audit.get("location")):
        failures.append("call not logged for audit")
    summary, fraga = body["choices"][0]["message"]["content"], body["fraga"]
    cited = {p["doc_id"]: p["status"] for p in fraga["policies_cited"]}
    low = normalise(summary)
    failures += ["missing: %r" % s for s in expect.get("must_contain", []) if normalise(s) not in low]
    failures += ["forbidden: %r" % s for s in expect.get("must_not_contain", []) if normalise(s) in low]
    failures += ["not cited: %s" % d for d in expect.get("must_cite", []) if d not in cited]
    for doc_id, status in cited.items():
        if doc_id not in POLICY:
            failures.append("cites unknown policy %s" % doc_id)
        elif POLICY[doc_id]["status"] != "Current" and (status == "Current" or "repealed" not in low):
            failures.append("non-current %s not flagged as repealed" % doc_id)
    # Faithfulness: every number must come from the case file, a cited policy, or a declared derivation.
    parts = [case["case_file"]] + expect.get("derived_values", [])
    parts += [d + " " + " ".join(POLICY[d].values()) for d in cited if d in POLICY]
    source = " ".join(parts)
    unsupported = numbers(summary) - numbers(source)
    if unsupported:
        failures.append("numbers not in any source: %s" % sorted(unsupported))
    if fraga["certainty"] < 0.7 and not any(w in low for w in DOUBT):
        failures.append("low certainty (%.2f) but no doubt shown" % fraga["certainty"])
    if len(summary.split()) > expect.get("max_words", 10 ** 6):
        failures.append("summary too long")
    return failures


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_summarize_case(case):
    assert check(case) == []


# Self-tests: the checks catch the failures they are meant to catch.
def mutate(cid, new_summary=None, **fraga):
    case = copy.deepcopy(next(c for c in CASES if c["id"] == cid))
    if new_summary:
        case["response"]["body"]["choices"][0]["message"]["content"] = new_summary
    case["response"]["body"]["fraga"].update(fraga)
    return case


def test_catches_other_case_leak():
    leaked = mutate("S01", "Leo Andersson asks to be treated like Sara Nyberg (case 2025-0388). Decide within 14 days (P-102).")
    assert any("forbidden" in f for f in check(leaked))


def test_catches_invented_number():
    wrong = mutate("S01", "Leo Andersson's application is complete. The municipality decides within 30 days (P-102). 14 days.")
    assert any("30" in f for f in check(wrong))


def test_catches_missing_doubt():
    sure = mutate("S02", "Ingrid Sjöberg pays no fee for the safety alarm (P-103). 250 SEK per month otherwise.", certainty=0.5)
    assert any("doubt" in f for f in check(sure))
