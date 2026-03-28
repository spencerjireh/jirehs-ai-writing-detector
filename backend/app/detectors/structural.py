import re

from app.core.models import DetectorResult, MatchDetail, ScoredResult, TextAnalysis
from app.detectors.base import BaseDetector

_RULE_OF_THREE = re.compile(
    r"\b(\w+(?:\s+\w+){0,3}),\s+(\w+(?:\s+\w+){0,3}),\s+and\s+(\w+(?:\s+\w+){0,3})\b",
    re.IGNORECASE,
)


class StructuralDetector(BaseDetector):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._sub_configs = {
            "Rule of Three": config.get("rule_of_three", {}),
            "Negative Parallelism": config.get("negative_parallelism", {}),
            "Outline Conclusion": config.get("outline_conclusion", {}),
            "False Range": config.get("false_range", {}),
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
            "Rule of Three": self._detect_rule_of_three(analysis),
            "Negative Parallelism": self._detect_pattern(
                analysis.text, self._sub_configs["Negative Parallelism"]
            ),
            "Outline Conclusion": self._detect_pattern(
                analysis.text, self._sub_configs["Outline Conclusion"]
            ),
            "False Range": self._detect_pattern(
                analysis.text, self._sub_configs["False Range"]
            ),
        }

    def _detect_rule_of_three(
        self, analysis: TextAnalysis
    ) -> tuple[list[MatchDetail], int]:
        cfg = self._sub_configs["Rule of Three"]
        ppm = cfg.get("points_per_match", 3)
        matches: list[MatchDetail] = []
        for sentence in analysis.sentences:
            for m in _RULE_OF_THREE.finditer(sentence):
                matches.append(MatchDetail(text=m.group(0), position=m.start()))
        return matches, len(matches) * ppm

    def _detect_pattern(
        self, text: str, cfg: dict
    ) -> tuple[list[MatchDetail], int]:
        ppm = cfg.get("points_per_match", 3)
        patterns = cfg.get("patterns", [])
        matches: list[MatchDetail] = []
        for pat_str in patterns:
            pat = re.compile(pat_str, re.IGNORECASE)
            for m in pat.finditer(text):
                matches.append(MatchDetail(text=m.group(0), position=m.start()))
        return matches, len(matches) * ppm

    @classmethod
    def config_key(cls) -> str:
        return "structural"
