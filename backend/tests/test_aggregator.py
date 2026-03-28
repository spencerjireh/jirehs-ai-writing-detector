import pytest

from app.core.models import LinguisticFactor, ScoredResult
from app.scoring.aggregator import aggregate, classify


@pytest.fixture
def scoring_config(config):
    return config


def _make_scored(name: str, contribution: int) -> ScoredResult:
    return ScoredResult(
        detector_name=name,
        raw_score=contribution,
        weight=1.0,
        cap=100,
        score_contribution=contribution,
    )


def _make_factor(name: str, contribution: int) -> LinguisticFactor:
    return LinguisticFactor(
        name=name,
        value=0.5,
        score_contribution=contribution,
        explanation="test",
    )


def test_sum_contributions(scoring_config):
    detectors = [_make_scored("A", 10), _make_scored("B", 20)]
    factors = [_make_factor("C", 5)]
    result = aggregate(detectors, factors, scoring_config)
    assert result.score == 35


def test_normalization_over_100(scoring_config):
    detectors = [_make_scored("A", 60), _make_scored("B", 60)]
    factors = [_make_factor("C", 30)]
    result = aggregate(detectors, factors, scoring_config)
    assert result.score == 100


def test_normalization_preserves_proportions(scoring_config):
    detectors = [_make_scored("A", 80), _make_scored("B", 40)]
    factors = [_make_factor("C", 80)]
    result = aggregate(detectors, factors, scoring_config)
    assert result.score == 100
    contribs = {c["name"]: c["score_contribution"] for c in result.contributions}
    assert contribs["A"] >= contribs["B"]


def test_classify_likely_human(scoring_config):
    assert classify(0, scoring_config) == "Likely Human-Written"
    assert classify(10, scoring_config) == "Likely Human-Written"
    assert classify(29, scoring_config) == "Likely Human-Written"


def test_classify_possibly_ai(scoring_config):
    assert classify(30, scoring_config) == "Possibly AI-Generated"
    assert classify(45, scoring_config) == "Possibly AI-Generated"
    assert classify(59, scoring_config) == "Possibly AI-Generated"


def test_classify_likely_ai(scoring_config):
    assert classify(60, scoring_config) == "Likely AI-Generated"
    assert classify(80, scoring_config) == "Likely AI-Generated"
    assert classify(100, scoring_config) == "Likely AI-Generated"


def test_zero_score(scoring_config):
    result = aggregate([], [], scoring_config)
    assert result.score == 0
    assert result.classification == "Likely Human-Written"


def test_boundary_30(scoring_config):
    detectors = [_make_scored("A", 30)]
    result = aggregate(detectors, [], scoring_config)
    assert result.classification == "Possibly AI-Generated"


def test_boundary_60(scoring_config):
    detectors = [_make_scored("A", 60)]
    result = aggregate(detectors, [], scoring_config)
    assert result.classification == "Likely AI-Generated"


def test_contributions_tracked(scoring_config):
    detectors = [_make_scored("Vocab", 10)]
    factors = [_make_factor("Lexical", 5)]
    result = aggregate(detectors, factors, scoring_config)
    names = [c["name"] for c in result.contributions]
    assert "Vocab" in names
    assert "Lexical" in names
