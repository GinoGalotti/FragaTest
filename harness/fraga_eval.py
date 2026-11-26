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
    cases, log, policies = load_all()
    failed = 0
    for case in cases:
        failures = evaluate(case, log, policies)
        failed += bool(failures)
        print("%s %-4s (%s) %s" % ("PASS" if not failures else "FAIL", case["id"], case["log_id"], "; ".join(failures)))
    print("\n%d/%d golden cases passed" % (len(cases) - failed, len(cases)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
