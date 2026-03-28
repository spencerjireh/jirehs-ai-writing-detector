import re

from app.core.models import LinguisticFactor, TextAnalysis

_VOWEL_GROUP = re.compile(r"[aeiouy]+", re.IGNORECASE)


def count_syllables(word: str) -> int:
    word = word.lower().rstrip("e")
    if not word:
        return 1
    count = len(_VOWEL_GROUP.findall(word))
    return max(count, 1)


def flesch_kincaid_grade(analysis: TextAnalysis) -> float:
    if analysis.stats.sentence_count == 0 or analysis.stats.word_count == 0:
        return 0.0

    total_syllables = sum(count_syllables(w) for w in analysis.words)
    words_per_sentence = analysis.stats.word_count / analysis.stats.sentence_count
    syllables_per_word = total_syllables / analysis.stats.word_count

    grade = 0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59
    return round(max(grade, 0.0), 1)


def reading_grade_factor(analysis: TextAnalysis, config: dict) -> LinguisticFactor:
    grade = flesch_kincaid_grade(analysis)
    ai_threshold = config.get("ai_threshold", 14)
    weight = config.get("weight", 1.0)
    cap = config.get("cap", 6)

    if grade >= ai_threshold:
        raw = int((grade - ai_threshold + 1) * 2)
        contribution = min(int(raw * weight), cap)
        explanation = (
            f"Flesch-Kincaid grade level {grade} exceeds AI threshold of "
            f"{ai_threshold}, suggesting overly uniform academic prose."
        )
    else:
        contribution = 0
        explanation = (
            f"Flesch-Kincaid grade level {grade} is within normal range "
            f"(threshold: {ai_threshold})."
        )

    return LinguisticFactor(
        name="Reading Grade Level",
        value=grade,
        score_contribution=contribution,
        explanation=explanation,
    )
