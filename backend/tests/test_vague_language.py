import pytest

from app.detectors.vague_language import VagueLanguageDetector
from app.preprocessing import preprocess


@pytest.fixture
def detector(config):
    return VagueLanguageDetector(config["vague_language"])


def test_detects_attribution(detector):
    analysis = preprocess("Experts agree that this is the best approach.")
    result = detector.detect(analysis)
    assert any("experts agree" in m.text for m in result.matches)


def test_detects_superficial(detector):
    analysis = preprocess("It is worth noting that significant developments have occurred.")
    result = detector.detect(analysis)
    texts = [m.text for m in result.matches]
    assert "it is worth noting" in texts
    assert "significant developments" in texts


def test_detects_overgeneralisation(detector):
    analysis = preprocess("Everyone knows that this is true. It is well established.")
    result = detector.detect(analysis)
    texts = [m.text for m in result.matches]
    assert "everyone knows" in texts
    assert "it is well established" in texts


def test_no_matches_clean_text(detector):
    analysis = preprocess("I had lunch at noon and went for a walk.")
    result = detector.detect(analysis)
    assert len(result.matches) == 0
    assert result.raw_score == 0


def test_score_all_returns_three_results(detector):
    analysis = preprocess("Some text here.")
    results = detector.score_all(analysis)
    assert len(results) == 3


def test_case_insensitive(detector):
    analysis = preprocess("EXPERTS AGREE that Studies Show results.")
    result = detector.detect(analysis)
    assert len(result.matches) >= 2


def test_cap_enforcement(detector):
    text = ". ".join(
        ["Experts agree this is true"] * 10
        + ["Studies show things work"] * 10
    )
    analysis = preprocess(text)
    results = detector.score_all(analysis)
    attr = next(r for r in results if r.detector_name == "Vague Attributions")
    assert attr.score_contribution <= attr.cap


def test_empty_text(detector):
    analysis = preprocess("")
    result = detector.detect(analysis)
    assert len(result.matches) == 0


def test_combined_score(detector):
    analysis = preprocess(
        "Experts agree that significant developments have occurred. "
        "Everyone knows this is the case."
    )
    result = detector.detect(analysis)
    assert result.raw_score > 0
    assert len(result.matches) >= 3
