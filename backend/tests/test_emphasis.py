import pytest

from app.detectors.emphasis import EmphasisDetector
from app.preprocessing import preprocess


@pytest.fixture
def detector(config):
    return EmphasisDetector(config["emphasis"])


def test_detects_undue_emphasis(detector):
    analysis = preprocess("This is a tremendous and remarkable achievement.")
    result = detector.detect(analysis)
    texts = [m.text for m in result.matches]
    assert "tremendous" in texts
    assert "remarkable" in texts


def test_detects_promotional(detector):
    analysis = preprocess("This is a real game-changer with revolutionary features.")
    result = detector.detect(analysis)
    texts = [m.text for m in result.matches]
    assert "game-changer" in texts
    assert "revolutionary" in texts


def test_detects_elegant_variation(detector):
    analysis = preprocess(
        "The company announced new plans. "
        "The organisation will expand next year. "
        "This firm has a strong track record."
    )
    result = detector.detect(analysis)
    elegant = [m for m in result.matches if "elegant variation" in m.text]
    assert len(elegant) > 0


def test_elegant_variation_no_match_beyond_proximity(detector):
    filler = "This is a filler sentence. " * 10
    analysis = preprocess(
        f"The company announced plans. {filler}The firm is growing."
    )
    result = detector.detect(analysis)
    elegant = [m for m in result.matches if "elegant variation" in m.text]
    assert len(elegant) == 0


def test_no_matches_clean_text(detector):
    analysis = preprocess("I went to the park and sat on a bench.")
    result = detector.detect(analysis)
    assert len(result.matches) == 0
    assert result.raw_score == 0


def test_score_all_returns_three_results(detector):
    analysis = preprocess("Some text here.")
    results = detector.score_all(analysis)
    assert len(results) == 3


def test_undue_cap_enforcement(detector):
    text = " ".join(["tremendous remarkable groundbreaking extraordinary"] * 10)
    analysis = preprocess(text)
    results = detector.score_all(analysis)
    undue = next(r for r in results if r.detector_name == "Undue Emphasis")
    assert undue.score_contribution <= undue.cap


def test_promotional_cap_enforcement(detector):
    text = ". ".join(["This is a game-changer and revolutionary"] * 10)
    analysis = preprocess(text)
    results = detector.score_all(analysis)
    promo = next(r for r in results if r.detector_name == "Promotional Language")
    assert promo.score_contribution <= promo.cap


def test_empty_text(detector):
    analysis = preprocess("")
    result = detector.detect(analysis)
    assert len(result.matches) == 0


def test_case_insensitive_undue(detector):
    analysis = preprocess("TREMENDOUS results and Remarkable findings.")
    result = detector.detect(analysis)
    assert len(result.matches) == 2
