import math
import re

from wordfreq import word_frequency

from app.analyzers.readability import reading_grade_factor
from app.core.models import LinguisticFactor, TextAnalysis

_PASSIVE_PATTERN = re.compile(
    r"\b(?:am|is|are|was|were|been|being)\s+\w+ed\b", re.IGNORECASE
)

_PUNCTUATION_CHARS = set(".,;:!?-()\"'")


def analyze_linguistics(
    analysis: TextAnalysis, config: dict
) -> list[LinguisticFactor]:
    factors: list[LinguisticFactor] = []

    if "lexical_diversity" in config:
        factors.append(lexical_diversity(analysis.words, config["lexical_diversity"]))

    if "sentence_length_variation" in config:
        factors.append(
            sentence_length_variation(analysis.sentences, config["sentence_length_variation"])
        )

    if "passive_voice" in config:
        factors.append(passive_voice_ratio(analysis.sentences, config["passive_voice"]))

    if "transition_density" in config:
        factors.append(
            transition_density(analysis.words, config["transition_density"])
        )

    if "punctuation" in config:
        factors.append(punctuation_analysis(analysis.text, config["punctuation"]))

    if "rare_words" in config:
        factors.append(rare_word_ratio(analysis.words, config["rare_words"]))

    if "reading_grade" in config:
        factors.append(reading_grade_factor(analysis, config["reading_grade"]))

    return factors


def lexical_diversity(words: list[str], config: dict) -> LinguisticFactor:
    if not words:
        return LinguisticFactor(
            name="Lexical Diversity",
            value=0.0,
            score_contribution=0,
            explanation="No words to analyze.",
        )

    unique = set(words)
    ttr = round(len(unique) / len(words), 3)

    low = config.get("low_threshold", 0.4)
    weight = config.get("weight", 1.0)
    cap = config.get("cap", 8)

    if ttr < low:
        raw = int((low - ttr) * 20)
        contribution = min(int(raw * weight), cap)
        explanation = (
            f"Type-token ratio of {ttr} is below the typical human range "
            f"(threshold: {low}), suggesting repetitive vocabulary."
        )
    else:
        contribution = 0
        explanation = (
            f"Type-token ratio of {ttr} is within normal range "
            f"(threshold: {low})."
        )

    return LinguisticFactor(
        name="Lexical Diversity",
        value=ttr,
        score_contribution=contribution,
        explanation=explanation,
    )


def sentence_length_variation(
    sentences: list[str], config: dict
) -> LinguisticFactor:
    if len(sentences) < 2:
        return LinguisticFactor(
            name="Sentence Length Variation",
            value=0.0,
            score_contribution=0,
            explanation="Not enough sentences to measure variation.",
        )

    lengths = [len(s.split()) for s in sentences]
    mean = sum(lengths) / len(lengths)
    if mean == 0:
        cv = 0.0
    else:
        variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
        std_dev = math.sqrt(variance)
        cv = round(std_dev / mean, 3)

    threshold = config.get("cv_threshold", 0.35)
    weight = config.get("weight", 1.0)
    cap = config.get("cap", 10)

    if cv < threshold:
        raw = int((threshold - cv) * 30)
        contribution = min(int(raw * weight), cap)
        explanation = (
            f"Coefficient of variation {cv} is below threshold {threshold}, "
            f"suggesting uniform sentence lengths typical of AI writing."
        )
    else:
        contribution = 0
        explanation = (
            f"Coefficient of variation {cv} shows healthy sentence length "
            f"variation (threshold: {threshold})."
        )

    return LinguisticFactor(
        name="Sentence Length Variation",
        value=cv,
        score_contribution=contribution,
        explanation=explanation,
    )


def passive_voice_ratio(
    sentences: list[str], config: dict
) -> LinguisticFactor:
    if not sentences:
        return LinguisticFactor(
            name="Passive Voice",
            value=0.0,
            score_contribution=0,
            explanation="No sentences to analyze.",
        )

    passive_count = sum(
        1 for s in sentences if _PASSIVE_PATTERN.search(s)
    )
    ratio = round(passive_count / len(sentences), 3)

    ai_threshold = config.get("ai_threshold", 0.15)
    weight = config.get("weight", 1.0)
    cap = config.get("cap", 8)

    if ratio >= ai_threshold:
        raw = int((ratio - ai_threshold + 0.05) * 40)
        contribution = min(int(raw * weight), cap)
        explanation = (
            f"Passive voice ratio of {ratio} exceeds AI threshold of "
            f"{ai_threshold}, suggesting formal/academic tone common in AI text."
        )
    else:
        contribution = 0
        explanation = (
            f"Passive voice ratio of {ratio} is within normal range "
            f"(threshold: {ai_threshold})."
        )

    return LinguisticFactor(
        name="Passive Voice",
        value=ratio,
        score_contribution=contribution,
        explanation=explanation,
    )


def transition_density(words: list[str], config: dict) -> LinguisticFactor:
    if not words:
        return LinguisticFactor(
            name="Transition Density",
            value=0.0,
            score_contribution=0,
            explanation="No words to analyze.",
        )

    transition_words = set(w.lower() for w in config.get("words", []))
    count = sum(1 for w in words if w in transition_words)
    density = round(count / len(words), 3)

    ai_threshold = config.get("ai_threshold", 0.20)
    weight = config.get("weight", 1.0)
    cap = config.get("cap", 8)

    if density >= ai_threshold:
        raw = int((density - ai_threshold + 0.05) * 40)
        contribution = min(int(raw * weight), cap)
        explanation = (
            f"Transition word density of {density} exceeds AI threshold of "
            f"{ai_threshold}, suggesting over-structured prose."
        )
    else:
        contribution = 0
        explanation = (
            f"Transition word density of {density} is within normal range "
            f"(threshold: {ai_threshold})."
        )

    return LinguisticFactor(
        name="Transition Density",
        value=density,
        score_contribution=contribution,
        explanation=explanation,
    )


def punctuation_analysis(text: str, config: dict) -> LinguisticFactor:
    if not text.strip():
        return LinguisticFactor(
            name="Punctuation Patterns",
            value=0.0,
            score_contribution=0,
            explanation="No text to analyze.",
        )

    punct_chars = [c for c in text if c in _PUNCTUATION_CHARS]
    total_chars = len(text)
    punct_ratio = round(len(punct_chars) / total_chars, 3) if total_chars > 0 else 0.0

    unique_punct = set(punct_chars)
    punct_diversity = len(unique_punct)

    weight = config.get("weight", 1.0)
    cap = config.get("cap", 6)

    # AI text tends to use limited punctuation variety (mostly periods and commas)
    contribution = 0
    if punct_diversity <= 2 and len(punct_chars) >= 5:
        contribution = min(int(3 * weight), cap)
        explanation = (
            f"Only {punct_diversity} punctuation types used, suggesting "
            f"monotonous punctuation patterns typical of AI writing."
        )
    elif punct_ratio < 0.02 and total_chars > 50:
        contribution = min(int(2 * weight), cap)
        explanation = (
            f"Punctuation ratio of {punct_ratio} is unusually low."
        )
    else:
        explanation = (
            f"Punctuation diversity ({punct_diversity} types, ratio {punct_ratio}) "
            f"appears normal."
        )

    return LinguisticFactor(
        name="Punctuation Patterns",
        value=punct_ratio,
        score_contribution=contribution,
        explanation=explanation,
    )


def rare_word_ratio(words: list[str], config: dict) -> LinguisticFactor:
    if not words:
        return LinguisticFactor(
            name="Rare Words",
            value=0.0,
            score_contribution=0,
            explanation="No words to analyze.",
        )

    human_low, human_high = config.get("human_range", [0.03, 0.08])
    ai_threshold = config.get("ai_threshold", 0.12)
    weight = config.get("weight", 1.0)
    cap = config.get("cap", 6)

    # Words with very low frequency (< 1e-6) are considered rare
    rare_count = sum(
        1 for w in words if word_frequency(w, "en") < 1e-6 and len(w) > 2
    )
    ratio = round(rare_count / len(words), 3)

    if ratio < human_low:
        raw = int((human_low - ratio) * 50)
        contribution = min(int(raw * weight), cap)
        explanation = (
            f"Rare word ratio of {ratio} is below human range "
            f"({human_low}-{human_high}), suggesting common vocabulary "
            f"typical of AI text."
        )
    elif ratio >= ai_threshold:
        # Extremely high rare word ratio is also suspicious
        raw = int((ratio - ai_threshold) * 30)
        contribution = min(int(raw * weight), cap)
        explanation = (
            f"Rare word ratio of {ratio} exceeds AI threshold of "
            f"{ai_threshold}, suggesting artificially varied vocabulary."
        )
    else:
        contribution = 0
        explanation = (
            f"Rare word ratio of {ratio} is within normal human range "
            f"({human_low}-{human_high})."
        )

    return LinguisticFactor(
        name="Rare Words",
        value=ratio,
        score_contribution=contribution,
        explanation=explanation,
    )
