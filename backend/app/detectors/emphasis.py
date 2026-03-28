import re

from app.core.models import DetectorResult, MatchDetail, ScoredResult, TextAnalysis
from app.detectors.base import BaseDetector


class EmphasisDetector(BaseDetector):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._undue_cfg = config.get("undue", {})
        self._promotional_cfg = config.get("promotional", {})
        self._elegant_cfg = config.get("elegant_variation", {})

        self._undue_patterns = {
            w.lower(): re.compile(rf"\b{re.escape(w)}\b", re.IGNORECASE)
            for w in self._undue_cfg.get("words", [])
        }
        self._promotional_phrases = [
            p.lower() for p in self._promotional_cfg.get("phrases", [])
        ]
        self._synonym_groups: list[list[str]] = self._elegant_cfg.get(
            "synonym_groups", []
        )
        self._proximity = self._elegant_cfg.get("proximity_sentences", 4)

        self._sub_configs = {
            "Undue Emphasis": self._undue_cfg,
            "Promotional Language": self._promotional_cfg,
            "Elegant Variation": self._elegant_cfg,
        }

    def detect(self, analysis: TextAnalysis) -> DetectorResult:
        all_matches: list[MatchDetail] = []
        total_score = 0
        for _, (matches, score) in self._detect_all(analysis).items():
            all_matches.extend(matches)
            total_score += score
        return DetectorResult(matches=all_matches, raw_score=total_score)

    def score_all(self, analysis: TextAnalysis) -> list[ScoredResult]:
        results = []
        for sub_name, (matches, raw_score) in self._detect_all(analysis).items():
            cfg = self._sub_configs[sub_name]
            weight = cfg.get("weight", 1.0)
            cap = cfg.get("cap", 10)
            weighted = int(raw_score * weight)
            capped = min(weighted, cap)
            results.append(
                ScoredResult(
                    detector_name=sub_name,
                    matches=matches,
                    raw_score=raw_score,
                    weight=weight,
                    cap=cap,
                    score_contribution=capped,
                )
            )
        return results

    def _detect_all(
        self, analysis: TextAnalysis
    ) -> dict[str, tuple[list[MatchDetail], int]]:
        return {
            "Undue Emphasis": self._detect_undue(analysis.text),
            "Promotional Language": self._detect_promotional(analysis.text),
            "Elegant Variation": self._detect_elegant_variation(analysis.sentences),
        }

    def _detect_undue(self, text: str) -> tuple[list[MatchDetail], int]:
        ppm = self._undue_cfg.get("points_per_match", 2)
        matches: list[MatchDetail] = []
        for word, pattern in self._undue_patterns.items():
            for m in pattern.finditer(text):
                matches.append(MatchDetail(text=word, position=m.start()))
        return matches, len(matches) * ppm

    def _detect_promotional(self, text: str) -> tuple[list[MatchDetail], int]:
        ppm = self._promotional_cfg.get("points_per_match", 3)
        text_lower = text.lower()
        matches: list[MatchDetail] = []
        for phrase in self._promotional_phrases:
            start = 0
            while True:
                idx = text_lower.find(phrase, start)
                if idx == -1:
                    break
                matches.append(MatchDetail(text=phrase, position=idx))
                start = idx + 1
        return matches, len(matches) * ppm

    def _detect_elegant_variation(
        self, sentences: list[str]
    ) -> tuple[list[MatchDetail], int]:
        ppm = self._elegant_cfg.get("points_per_match", 3)
        matches: list[MatchDetail] = []

        for group in self._synonym_groups:
            group_lower = [w.lower() for w in group]
            for i, sentence in enumerate(sentences):
                window_start = max(0, i - self._proximity + 1)
                window = sentences[window_start : i + 1]
                window_text = " ".join(window).lower()

                words_found = [w for w in group_lower if w in window_text]
                if len(words_found) >= 2:
                    sentence_lower = sentence.lower()
                    current_words = [w for w in group_lower if w in sentence_lower]
                    prior_text = " ".join(sentences[window_start:i]).lower()
                    prior_words = [w for w in group_lower if w in prior_text]
                    if current_words and prior_words:
                        for w in current_words:
                            if w in prior_words:
                                continue
                            matches.append(
                                MatchDetail(
                                    text=f"elegant variation: {w} (synonym of {prior_words[0]})",
                                    position=0,
                                )
                            )

        return matches, len(matches) * ppm

    @classmethod
    def config_key(cls) -> str:
        return "emphasis"
