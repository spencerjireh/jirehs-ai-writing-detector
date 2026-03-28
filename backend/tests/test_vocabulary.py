import pytest

from app.detectors.vocabulary import VocabularyDetector
from app.preprocessing import preprocess


@pytest.fixture
def detector(config):
    return VocabularyDetector(config["vocabulary"])


def test_detects_ai_word(detector):
    analysis = preprocess("We need to delve into the root cause.")
    result = detector.detect(analysis)
    assert any("delve" in m.text for m in result.matches)


def test_detects_ai_phrase(detector):
    analysis = preprocess("Let us delve into the details of innovative solutions.")
    result = detector.detect(analysis)
    texts = [m.text for m in result.matches]
    assert "delve into" in texts
    assert "innovative solutions" in texts


def test_case_insensitive(detector):
    analysis = preprocess("ROBUST systems are Robust and DELVE into things.")
    result = detector.detect(analysis)
    word_matches = [m.text for m in result.matches if m.text == "robust"]
    assert len(word_matches) == 2


def test_no_matches_clean_text(detector):
    analysis = preprocess("I walked to the store and bought some milk.")
    result = detector.detect(analysis)
    assert len(result.matches) == 0
    assert result.raw_score == 0


def test_score_contribution(detector):
    analysis = preprocess("We leverage robust and innovative approaches.")
    scored = detector.score(analysis)
    assert scored.score_contribution > 0
    assert scored.detector_name == "Vocabulary"


def test_cap_enforcement(detector):
    words = " ".join(["delve robust innovative leverage streamline"] * 10)
    analysis = preprocess(words)
    scored = detector.score(analysis)
    assert scored.score_contribution <= detector._cap


def test_weight_applied(config):
    cfg = dict(config["vocabulary"])
    cfg["weight"] = 2.0
    cfg["cap"] = 100
    detector = VocabularyDetector(cfg)
    analysis = preprocess("We need to delve into things.")
    result_raw = detector.detect(analysis)
    scored = detector.score(analysis)
    assert scored.score_contribution >= result_raw.raw_score


def test_empty_text(detector):
    analysis = preprocess("")
    result = detector.detect(analysis)
    assert len(result.matches) == 0
    assert result.raw_score == 0


def test_single_word_no_match(detector):
    analysis = preprocess("hello")
    result = detector.detect(analysis)
    assert len(result.matches) == 0


def test_single_word_match(detector):
    analysis = preprocess("delve")
    result = detector.detect(analysis)
    assert len(result.matches) == 1


def test_multiple_occurrences(detector):
    analysis = preprocess("We delve into this, then delve into that.")
    result = detector.detect(analysis)
    delve_word = [m for m in result.matches if m.text == "delve"]
    delve_phrase = [m for m in result.matches if m.text == "delve into"]
    assert len(delve_word) == 2
    assert len(delve_phrase) == 2
