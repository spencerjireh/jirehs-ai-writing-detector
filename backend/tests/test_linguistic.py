import pytest

from app.analyzers.linguistic import (
    analyze_linguistics,
    lexical_diversity,
    sentence_length_variation,
    passive_voice_ratio,
    transition_density,
    punctuation_analysis,
    rare_word_ratio,
)
from app.preprocessing import preprocess


def test_analyze_linguistics_returns_all_factors(config):
    analysis = preprocess(
        "The quick brown fox jumps over the lazy dog. "
        "She sells seashells by the seashore."
    )
    factors = analyze_linguistics(analysis, config["linguistic"])
    assert len(factors) == 7
    names = {f.name for f in factors}
    assert "Lexical Diversity" in names
    assert "Sentence Length Variation" in names
    assert "Passive Voice" in names
    assert "Transition Density" in names
    assert "Punctuation Patterns" in names
    assert "Rare Words" in names
    assert "Reading Grade Level" in names


def test_lexical_diversity_high_repetition():
    words = ["the", "the", "the", "the", "the", "is", "is", "is", "is", "is"]
    cfg = {"low_threshold": 0.4, "weight": 1.0, "cap": 8}
    factor = lexical_diversity(words, cfg)
    assert factor.value < 0.4
    assert factor.score_contribution > 0


def test_lexical_diversity_varied_text():
    words = ["cat", "dog", "bird", "fish", "tree", "house", "car", "book", "sun", "moon"]
    cfg = {"low_threshold": 0.4, "weight": 1.0, "cap": 8}
    factor = lexical_diversity(words, cfg)
    assert factor.value >= 0.4
    assert factor.score_contribution == 0


def test_lexical_diversity_empty():
    cfg = {"low_threshold": 0.4, "weight": 1.0, "cap": 8}
    factor = lexical_diversity([], cfg)
    assert factor.value == 0.0
    assert factor.score_contribution == 0


def test_sentence_variation_uniform():
    sentences = [
        "This has five words total.",
        "This also five words yes.",
        "Again five words are here.",
    ]
    cfg = {"cv_threshold": 0.35, "weight": 1.0, "cap": 10}
    factor = sentence_length_variation(sentences, cfg)
    assert factor.score_contribution > 0


def test_sentence_variation_diverse():
    sentences = [
        "Short.",
        "This is a medium length sentence with several words.",
        "Yes.",
        "And this one is even longer with quite a few more words added to make it substantial.",
    ]
    cfg = {"cv_threshold": 0.35, "weight": 1.0, "cap": 10}
    factor = sentence_length_variation(sentences, cfg)
    assert factor.value >= 0.35


def test_sentence_variation_single_sentence():
    cfg = {"cv_threshold": 0.35, "weight": 1.0, "cap": 10}
    factor = sentence_length_variation(["Just one sentence."], cfg)
    assert factor.score_contribution == 0


def test_passive_voice_high():
    sentences = [
        "The ball was kicked by the player.",
        "The cake was eaten by the children.",
        "The book was written by the author.",
        "I went home.",
    ]
    cfg = {"ai_threshold": 0.15, "weight": 1.0, "cap": 8}
    factor = passive_voice_ratio(sentences, cfg)
    assert factor.value > 0.15
    assert factor.score_contribution > 0


def test_passive_voice_low():
    sentences = [
        "I kicked the ball.",
        "The children ate the cake.",
        "The author wrote the book.",
    ]
    cfg = {"ai_threshold": 0.15, "weight": 1.0, "cap": 8}
    factor = passive_voice_ratio(sentences, cfg)
    assert factor.score_contribution == 0


def test_passive_voice_empty():
    cfg = {"ai_threshold": 0.15, "weight": 1.0, "cap": 8}
    factor = passive_voice_ratio([], cfg)
    assert factor.score_contribution == 0


def test_transition_density_high():
    words = ["furthermore", "the", "data", "moreover", "shows", "consequently",
             "the", "results", "additionally", "prove"]
    cfg = {"ai_threshold": 0.20, "words": ["furthermore", "moreover", "consequently", "additionally"],
           "weight": 1.0, "cap": 8}
    factor = transition_density(words, cfg)
    assert factor.value >= 0.20
    assert factor.score_contribution > 0


def test_transition_density_low():
    words = ["the", "cat", "sat", "on", "the", "mat"]
    cfg = {"ai_threshold": 0.20, "words": ["furthermore", "moreover"], "weight": 1.0, "cap": 8}
    factor = transition_density(words, cfg)
    assert factor.score_contribution == 0


def test_transition_density_empty():
    cfg = {"ai_threshold": 0.20, "words": ["furthermore"], "weight": 1.0, "cap": 8}
    factor = transition_density([], cfg)
    assert factor.score_contribution == 0


def test_punctuation_monotonous():
    text = "This is a sentence. This is another sentence. And another one. Yes indeed. Quite so."
    cfg = {"weight": 1.0, "cap": 6}
    factor = punctuation_analysis(text, cfg)
    assert factor.score_contribution > 0


def test_punctuation_diverse():
    text = "Really? Yes! It's true -- and (surprisingly) it works; well, mostly."
    cfg = {"weight": 1.0, "cap": 6}
    factor = punctuation_analysis(text, cfg)
    assert factor.score_contribution == 0


def test_punctuation_empty():
    cfg = {"weight": 1.0, "cap": 6}
    factor = punctuation_analysis("", cfg)
    assert factor.score_contribution == 0


def test_rare_words_common_vocabulary():
    words = ["the", "cat", "sat", "on", "the", "mat", "and", "ate", "food", "today"]
    cfg = {"human_range": [0.03, 0.08], "ai_threshold": 0.12, "weight": 1.0, "cap": 6}
    factor = rare_word_ratio(words, cfg)
    assert factor.score_contribution >= 0


def test_rare_words_empty():
    cfg = {"human_range": [0.03, 0.08], "ai_threshold": 0.12, "weight": 1.0, "cap": 6}
    factor = rare_word_ratio([], cfg)
    assert factor.score_contribution == 0


def test_all_factors_have_explanations(config):
    analysis = preprocess(
        "The quick brown fox jumps over the lazy dog. She sells seashells."
    )
    factors = analyze_linguistics(analysis, config["linguistic"])
    for f in factors:
        assert len(f.explanation) > 0


def test_all_factors_respect_cap(config):
    analysis = preprocess(
        "Furthermore, moreover, consequently, additionally, nevertheless. " * 10
    )
    factors = analyze_linguistics(analysis, config["linguistic"])
    for f in factors:
        cfg_section = config["linguistic"].get(
            f.name.lower().replace(" ", "_"), {}
        )
        if isinstance(cfg_section, dict) and "cap" in cfg_section:
            assert f.score_contribution <= cfg_section["cap"]
