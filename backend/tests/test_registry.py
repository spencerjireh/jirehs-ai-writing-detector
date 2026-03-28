import pytest

from app.detectors.registry import discover_detectors


def test_discovers_all_detectors(config):
    detectors = discover_detectors(config)
    assert len(detectors) == 4


def test_detector_names(config):
    detectors = discover_detectors(config)
    names = {d.name for d in detectors}
    assert "Vocabulary" in names
    assert "Structural" in names
    assert "VagueLanguage" in names
    assert "Emphasis" in names


def test_detectors_have_config(config):
    detectors = discover_detectors(config)
    for d in detectors:
        assert d._cap > 0


def test_detectors_can_score(config):
    from app.preprocessing import preprocess

    detectors = discover_detectors(config)
    analysis = preprocess("This is a test sentence.")
    for d in detectors:
        results = d.score_all(analysis)
        assert isinstance(results, list)
        for r in results:
            assert r.score_contribution >= 0
