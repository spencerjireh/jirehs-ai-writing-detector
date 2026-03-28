import pytest

from app.core.models import (
    AggregatedScore,
    LinguisticFactor,
    MatchDetail,
    ScoredResult,
    TextAnalysis,
    TextStats,
)
from app.report.builder import build_report


@pytest.fixture
def sample_analysis():
    return TextAnalysis(
        text="Test text.",
        sentences=["Test text."],
        words=["test", "text"],
        stats=TextStats(
            char_count=10,
            word_count=2,
            avg_word_length=4.0,
            sentence_count=1,
        ),
    )


@pytest.fixture
def sample_detectors():
    return [
        ScoredResult(
            detector_name="Vocabulary",
            matches=[
                MatchDetail(text="delve", position=0),
                MatchDetail(text="delve", position=20),
                MatchDetail(text="robust", position=10),
            ],
            raw_score=6,
            weight=1.0,
            cap=15,
            score_contribution=6,
        ),
    ]


@pytest.fixture
def sample_factors():
    return [
        LinguisticFactor(
            name="Lexical Diversity",
            value=0.42,
            score_contribution=4,
            explanation="Low TTR.",
        ),
    ]


@pytest.fixture
def sample_aggregated():
    return AggregatedScore(
        score=10,
        classification="Likely Human-Written",
        contributions=[],
    )


def test_report_has_score(sample_analysis, sample_detectors, sample_factors, sample_aggregated):
    report = build_report(sample_analysis, sample_detectors, sample_factors, sample_aggregated)
    assert report.score == 10
    assert report.classification == "Likely Human-Written"


def test_report_has_stats(sample_analysis, sample_detectors, sample_factors, sample_aggregated):
    report = build_report(sample_analysis, sample_detectors, sample_factors, sample_aggregated)
    assert report.stats.word_count == 2
    assert report.stats.char_count == 10


def test_report_has_timestamp(sample_analysis, sample_detectors, sample_factors, sample_aggregated):
    report = build_report(sample_analysis, sample_detectors, sample_factors, sample_aggregated)
    assert report.timestamp is not None


def test_report_has_linguistic_factors(sample_analysis, sample_detectors, sample_factors, sample_aggregated):
    report = build_report(sample_analysis, sample_detectors, sample_factors, sample_aggregated)
    assert len(report.linguistic_factors) == 1
    assert report.linguistic_factors[0].name == "Lexical Diversity"


def test_report_has_pattern_detections(sample_analysis, sample_detectors, sample_factors, sample_aggregated):
    report = build_report(sample_analysis, sample_detectors, sample_factors, sample_aggregated)
    assert len(report.pattern_detections) == 1
    det = report.pattern_detections[0]
    assert det.category == "Vocabulary"
    assert det.occurrences == 3
    assert "delve (x2)" in det.details
    assert "robust" in det.details


def test_report_includes_warnings(sample_analysis, sample_detectors, sample_factors, sample_aggregated):
    report = build_report(
        sample_analysis, sample_detectors, sample_factors, sample_aggregated,
        warnings=["Detector X was skipped"],
    )
    assert "Detector X was skipped" in report.warnings


def test_report_no_warnings_default(sample_analysis, sample_detectors, sample_factors, sample_aggregated):
    report = build_report(sample_analysis, sample_detectors, sample_factors, sample_aggregated)
    assert report.warnings == []


def test_report_empty_detectors(sample_analysis, sample_factors, sample_aggregated):
    report = build_report(sample_analysis, [], sample_factors, sample_aggregated)
    assert report.pattern_detections == []


def test_report_skips_zero_contribution_no_matches(sample_analysis, sample_factors, sample_aggregated):
    zero_result = ScoredResult(
        detector_name="Empty",
        matches=[],
        raw_score=0,
        weight=1.0,
        cap=10,
        score_contribution=0,
    )
    report = build_report(sample_analysis, [zero_result], sample_factors, sample_aggregated)
    assert len(report.pattern_detections) == 0
