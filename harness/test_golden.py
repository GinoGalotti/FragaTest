import pytest

from fraga_eval import evaluate, load_all, normalise

CASES, LOG, POLICIES = load_all()


@pytest.mark.parametrize("case", CASES, ids=[c["id"] + "-" + c["log_id"] for c in CASES])
def test_golden_case(case):
    failures = evaluate(case, LOG, POLICIES)
    assert not failures, "; ".join(failures)


# Self-tests: the checker must catch what it claims to catch (a harness that only passes proves nothing).
def test_normalise_thousands_separator():
    assert normalise("Up to 1,688 SEK") == "up to 1688 sek"


def test_detects_repealed_source():
    case = {"log_id": "L03", "expected_sources": []}
    assert any("non-current" in f for f in evaluate(case, LOG, POLICIES))


def test_detects_missing_fact():
    case = {"log_id": "L07", "must_contain": ["3 weeks"]}
    assert evaluate(case, LOG, POLICIES) == ["missing fact: '3 weeks'"]
