import re

import nltk
from nltk.tokenize import sent_tokenize

from app.core.models import TextAnalysis, TextStats

nltk.download("punkt_tab", quiet=True)

_WORD_PATTERN = re.compile(r"[a-zA-Z]+(?:[''-][a-zA-Z]+)*")


def preprocess(text: str) -> TextAnalysis:
    sentences = sent_tokenize(text) if text.strip() else []
    words = _WORD_PATTERN.findall(text.lower())

    char_count = len(text)
    word_count = len(words)
    sentence_count = len(sentences)
    avg_word_length = (
        round(sum(len(w) for w in words) / word_count, 2) if word_count > 0 else 0.0
    )

    stats = TextStats(
        char_count=char_count,
        word_count=word_count,
        avg_word_length=avg_word_length,
        sentence_count=sentence_count,
    )

    return TextAnalysis(
        text=text,
        sentences=sentences,
        words=words,
        stats=stats,
    )
