"""Golden-case checks for Fråga answers recorded in data/fraga-log-sample.csv.

Checks look for patterns (facts, sources, forbidden content), not exact wording.
Run as a script for a report, or via pytest (test_golden.py) in CI.
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "data" / "fraga-log-sample.csv"
POLICIES = ROOT / "data" / "fraga-policy-excerpts.csv"
CASES = Path(__file__).resolve().parent / "golden_cases.json"


def load_csv(path, key):
    with open(path, encoding="utf-8", newline="") as f:
        return {row[key]: row for row in csv.DictReader(f)}


def normalise(text):
    """Lower-case and drop thousands separators, so '1,688 SEK' matches '1688 sek'."""
    return re.sub(r"(?<=\d)[,\s](?=\d{3}\b)", "", text).lower()


def cited(row):
    return {s.strip() for s in row["sources_cited"].split(";") if s.strip() not in ("", "none")}


def evaluate(case, log, policies):
    """Return a list of failure messages; an empty list means the case passes."""
    row = log[case["log_id"]]
    answer, sources = normalise(row["answer"]), cited(row)
    failures = []
    for fact in case.get("must_contain", []):
        if normalise(fact) not in answer:
            failures.append("missing fact: %r" % fact)
    for bad in case.get("must_not_contain", []):
        if normalise(bad) in answer:
            failures.append("forbidden content: %r" % bad)
    for pattern in case.get("forbidden_patterns", []):  # e.g. case numbers from other cases (P-107)
        if re.search(pattern, row["answer"]):
            failures.append("forbidden pattern: %s" % pattern)
    if "starts_with" in case and not answer.startswith(normalise(case["starts_with"])):
        failures.append("wrong verdict: expected answer to start with %r" % case["starts_with"])
    missing = set(case.get("expected_sources", [])) - sources
    if missing:
        failures.append("missing sources: %s" % sorted(missing))
    repealed = sorted(s for s in sources if s in policies and policies[s]["status"] != "Current")
    if repealed and not case.get("allow_non_current_sources", False):
        failures.append("non-current source cited: %s" % repealed)
    return failures


def load_all():
    return json.loads(CASES.read_text(encoding="utf-8")), load_csv(LOG, "log_id"), load_csv(POLICIES, "doc_id")


def main():
    """Report each recorded v1 answer against its golden case.

    Exit code 1 only if the harness disagrees with the human-labelled verdict
    (v1_expected), i.e. the evaluator itself is wrong. Failing v1 answers are findings.
    """
    cases, log, policies = load_all()
    failed = disagree = 0
    for case in cases:
        failures = evaluate(case, log, policies)
        verdict = "fail" if failures else "pass"
        failed += verdict == "fail"
        disagree += verdict != case["v1_expected"]
        print("%s %s (%s) [%s] %s" % (verdict.upper(), case["id"], case["log_id"], ",".join(case["criteria"]), "; ".join(failures)))
    print("\nv1 recorded answers: %d/%d pass. Harness agrees with human labels on %d/%d."
          % (len(cases) - failed, len(cases), len(cases) - disagree, len(cases)))
    return 1 if disagree else 0


if __name__ == "__main__":
    sys.exit(main())
