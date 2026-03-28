from abc import ABC, abstractmethod

from app.core.models import DetectorResult, ScoredResult, TextAnalysis


class BaseDetector(ABC):
    def __init__(self, config: dict) -> None:
        self._config = config
        self._weight: float = config.get("weight", 1.0)
        self._cap: int = config.get("cap", 10)
        self._points_per_match: int = config.get("points_per_match", 1)

    @abstractmethod
    def detect(self, analysis: TextAnalysis) -> DetectorResult:
        ...

    def score(self, analysis: TextAnalysis) -> ScoredResult:
        result = self.detect(analysis)
        weighted = int(result.raw_score * self._weight)
        capped = min(weighted, self._cap)
        return ScoredResult(
            detector_name=self.name,
            matches=result.matches,
            raw_score=result.raw_score,
            weight=self._weight,
            cap=self._cap,
            score_contribution=capped,
        )

    def score_all(self, analysis: TextAnalysis) -> list[ScoredResult]:
        """Return per-sub-detector results. Override for compound detectors."""
        return [self.score(analysis)]

    @property
    def name(self) -> str:
        cls_name = type(self).__name__
        return cls_name.replace("Detector", "").strip()

    @classmethod
    def config_key(cls) -> str:
        raise NotImplementedError(
            f"{cls.__name__} must implement config_key() classmethod"
        )
