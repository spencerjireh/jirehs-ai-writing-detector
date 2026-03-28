import re

from app.core.models import DetectorResult, MatchDetail, TextAnalysis
from app.detectors.base import BaseDetector


class VocabularyDetector(BaseDetector):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._words = [w.lower() for w in config.get("words", [])]
        self._phrases = [p.lower() for p in config.get("phrases", [])]
        self._word_patterns = {
            w: re.compile(rf"\b{re.escape(w)}\b", re.IGNORECASE)
            for w in self._words
        }

    def detect(self, analysis: TextAnalysis) -> DetectorResult:
        matches: list[MatchDetail] = []
        text_lower = analysis.text.lower()

        for word, pattern in self._word_patterns.items():
            found = pattern.finditer(analysis.text)
            for m in found:
                matches.append(MatchDetail(text=word, position=m.start()))

        for phrase in self._phrases:
            start = 0
            while True:
                idx = text_lower.find(phrase, start)
                if idx == -1:
                    break
                matches.append(MatchDetail(text=phrase, position=idx))
                start = idx + 1

        raw_score = len(matches) * self._points_per_match
        return DetectorResult(matches=matches, raw_score=raw_score)

    @classmethod
    def config_key(cls) -> str:
        return "vocabulary"
