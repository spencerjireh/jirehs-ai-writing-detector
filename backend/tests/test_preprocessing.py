import pytest

from app.preprocessing import preprocess


def test_sentence_tokenization(medium_text):
    result = preprocess(medium_text)
    assert result.stats.sentence_count == 4


def test_word_tokenization(short_text):
    result = preprocess(short_text)
    assert result.stats.word_count == 5
    assert "this" in result.words
    assert "short" in result.words


def test_char_count(short_text):
    result = preprocess(short_text)
    assert result.stats.char_count == len(short_text)


def test_avg_word_length(short_text):
    result = preprocess(short_text)
    assert result.stats.avg_word_length > 0
    assert isinstance(result.stats.avg_word_length, float)


def test_empty_string():
    result = preprocess("")
    assert result.stats.word_count == 0
    assert result.stats.sentence_count == 0
    assert result.stats.char_count == 0
    assert result.stats.avg_word_length == 0.0
    assert result.words == []
    assert result.sentences == []


def test_single_word():
    result = preprocess("Hello")
    assert result.stats.word_count == 1
    assert result.stats.sentence_count == 1
    assert result.words == ["hello"]


def test_whitespace_only():
    result = preprocess("   \n\t  ")
    assert result.stats.word_count == 0
    assert result.stats.sentence_count == 0


def test_unicode_text():
    result = preprocess("The cafe's menu had crepes and souffle.")
    assert result.stats.word_count > 0
    assert result.stats.sentence_count == 1


def test_preserves_original_text(medium_text):
    result = preprocess(medium_text)
    assert result.text == medium_text


def test_words_are_lowercase():
    result = preprocess("Hello World FOO")
    assert all(w == w.lower() for w in result.words)


def test_hyphenated_words():
    result = preprocess("This is a well-known fact.")
    assert "well-known" in result.words


def test_contractions():
    result = preprocess("It's a dog's life, isn't it?")
    assert "it's" in result.words
    assert "isn't" in result.words
