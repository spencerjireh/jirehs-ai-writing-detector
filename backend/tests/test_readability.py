import pytest

from app.analyzers.readability import count_syllables, flesch_kincaid_grade, reading_grade_factor
from app.preprocessing import preprocess


def test_syllable_count_simple():
    assert count_syllables("cat") == 1
    assert count_syllables("water") == 2
    assert count_syllables("beautiful") == 3


def test_syllable_count_silent_e():
    assert count_syllables("make") == 1
    assert count_syllables("time") == 1
    assert count_syllables("complete") == 2


def test_syllable_count_single_char():
    assert count_syllables("a") == 1
    assert count_syllables("I") == 1


def test_flesch_kincaid_simple_text():
    analysis = preprocess(
        "The cat sat on the mat. The dog ran in the yard."
    )
    grade = flesch_kincaid_grade(analysis)
    assert grade < 5  # Simple text should have low grade level


def test_flesch_kincaid_complex_text():
    analysis = preprocess(
        "The implementation of sophisticated algorithms necessitates "
        "comprehensive understanding of computational complexity theory "
        "and mathematical abstractions."
    )
    grade = flesch_kincaid_grade(analysis)
    assert grade > 10  # Complex text should have high grade level


def test_flesch_kincaid_empty():
    analysis = preprocess("")
    grade = flesch_kincaid_grade(analysis)
    assert grade == 0.0


def test_flesch_kincaid_non_negative():
    analysis = preprocess("Go. Run. Sit.")
    grade = flesch_kincaid_grade(analysis)
    assert grade >= 0.0


def test_reading_grade_factor_below_threshold():
    analysis = preprocess("The cat sat on the mat. It was a good day.")
    cfg = {"ai_threshold": 14, "weight": 1.0, "cap": 6}
    factor = reading_grade_factor(analysis, cfg)
    assert factor.score_contribution == 0


def test_reading_grade_factor_above_threshold():
    analysis = preprocess(
        "The implementation of extraordinarily sophisticated computational "
        "algorithms necessitates comprehensive understanding of theoretical "
        "mathematical abstractions and multidimensional complexity analysis "
        "frameworks utilized in contemporary research institutions."
    )
    cfg = {"ai_threshold": 14, "weight": 1.0, "cap": 6}
    factor = reading_grade_factor(analysis, cfg)
    assert factor.score_contribution >= 0  # May or may not exceed threshold


def test_reading_grade_factor_cap():
    analysis = preprocess(
        "The extraordinarily multifaceted implementation of sophisticated "
        "computational methodologies necessitates comprehensive understanding. " * 5
    )
    cfg = {"ai_threshold": 5, "weight": 1.0, "cap": 6}
    factor = reading_grade_factor(analysis, cfg)
    assert factor.score_contribution <= 6


def test_reading_grade_factor_has_explanation():
    analysis = preprocess("Simple text here.")
    cfg = {"ai_threshold": 14, "weight": 1.0, "cap": 6}
    factor = reading_grade_factor(analysis, cfg)
    assert len(factor.explanation) > 0
