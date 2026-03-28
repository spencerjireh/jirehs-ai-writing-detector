import pytest

from app.detectors.structural import StructuralDetector
from app.preprocessing import preprocess


@pytest.fixture
def detector(config):
    return StructuralDetector(config["structural"])


def test_rule_of_three(detector):
    analysis = preprocess(
        "The system provides speed, reliability, and scalability."
    )
    result = detector.detect(analysis)
    assert len(result.matches) > 0
    assert result.raw_score > 0


def test_rule_of_three_no_match(detector):
    analysis = preprocess("The system provides speed and reliability.")
    results = detector.score_all(analysis)
    rot = next(r for r in results if r.detector_name == "Rule of Three")
    assert rot.score_contribution == 0


def test_negative_parallelism(detector):
    analysis = preprocess(
        "The platform is not only fast but also incredibly reliable."
    )
    result = detector.detect(analysis)
    assert any("not only" in m.text.lower() for m in result.matches)


def test_outline_conclusion(detector):
    analysis = preprocess(
        "Despite initial challenges, the platform offers remarkable flexibility."
    )
    result = detector.detect(analysis)
    assert len(result.matches) > 0


def test_false_range(detector):
    analysis = preprocess(
        "From startups to large enterprises, everyone benefits."
    )
    result = detector.detect(analysis)
    assert any("from" in m.text.lower() for m in result.matches)


def test_no_matches_clean_text(detector):
    analysis = preprocess("I went to the store and bought some bread.")
    result = detector.detect(analysis)
    assert len(result.matches) == 0
    assert result.raw_score == 0


def test_score_all_returns_four_results(detector):
    analysis = preprocess("Some text here.")
    results = detector.score_all(analysis)
    assert len(results) == 4


def test_sub_detector_cap_enforcement(detector):
    text = ". ".join(
        [
            "We provide speed, quality, and reliability",
            "It offers strength, agility, and endurance",
            "They deliver power, precision, and control",
            "She brings talent, skill, and determination",
            "He shows courage, wisdom, and patience",
        ]
    )
    analysis = preprocess(text)
    results = detector.score_all(analysis)
    rot = next(r for r in results if r.detector_name == "Rule of Three")
    assert rot.score_contribution <= rot.cap


def test_empty_text(detector):
    analysis = preprocess("")
    result = detector.detect(analysis)
    assert len(result.matches) == 0


def test_combined_score(detector):
    analysis = preprocess(
        "The system is not only fast but also reliable. "
        "It provides speed, power, and efficiency. "
        "From small teams to large organisations, everyone benefits."
    )
    result = detector.detect(analysis)
    assert result.raw_score > 0
    assert len(result.matches) >= 3
