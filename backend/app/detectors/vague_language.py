from app.core.models import DetectorResult, MatchDetail, ScoredResult, TextAnalysis
from app.detectors.base import BaseDetector


class VagueLanguageDetector(BaseDetector):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._sub_configs = {
            "Vague Attributions": config.get("attributions", {}),
            "Superficial Hedging": config.get("superficial", {}),
            "Overgeneralisation": config.get("overgeneralisation", {}),
        }

    def detect(self, analysis: TextAnalysis) -> DetectorResult:
        all_matches: list[MatchDetail] = []
        total_score = 0
        for _, cfg in self._sub_configs.items():
            matches, score = self._detect_phrases(analysis.text, cfg)
            all_matches.extend(matches)
            total_score += score
        return DetectorResult(matches=all_matches, raw_score=total_score)

    def score_all(self, analysis: TextAnalysis) -> list[ScoredResult]:
        results = []
        for sub_name, cfg in self._sub_configs.items():
            matches, raw_score = self._detect_phrases(analysis.text, cfg)
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

    def _detect_phrases(
        self, text: str, cfg: dict
    ) -> tuple[list[MatchDetail], int]:
        ppm = cfg.get("points_per_match", 2)
        phrases = [p.lower() for p in cfg.get("phrases", [])]
        text_lower = text.lower()
        matches: list[MatchDetail] = []
        for phrase in phrases:
            start = 0
            while True:
                idx = text_lower.find(phrase, start)
                if idx == -1:
                    break
                matches.append(MatchDetail(text=phrase, position=idx))
                start = idx + 1
        return matches, len(matches) * ppm

    @classmethod
    def config_key(cls) -> str:
        return "vague_language"
