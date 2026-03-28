from collections import Counter
from datetime import datetime, timezone

from app.core.models import (
    AggregatedScore,
    AnalyzeResponse,
    LinguisticFactor,
    PatternDetection,
    ScoredResult,
    TextAnalysis,
)


def build_report(
    analysis: TextAnalysis,
    detector_results: list[ScoredResult],
    linguistic_factors: list[LinguisticFactor],
    aggregated: AggregatedScore,
    warnings: list[str] | None = None,
) -> AnalyzeResponse:
    pattern_detections = _build_pattern_detections(detector_results)

    return AnalyzeResponse(
        score=aggregated.score,
        classification=aggregated.classification,
        stats=analysis.stats,
        linguistic_factors=linguistic_factors,
        pattern_detections=pattern_detections,
        warnings=warnings or [],
        timestamp=datetime.now(timezone.utc),
    )


def _build_pattern_detections(
    results: list[ScoredResult],
) -> list[PatternDetection]:
    detections: list[PatternDetection] = []

    for result in results:
        if result.score_contribution == 0 and not result.matches:
            continue

        match_counter: Counter[str] = Counter(m.text for m in result.matches)
        details = [
            f"{text} (x{count})" if count > 1 else text
            for text, count in match_counter.most_common()
        ]

        occurrences = len(result.matches)
        explanation = (
            f"Found {occurrences} match{'es' if occurrences != 1 else ''} "
            f"contributing {result.score_contribution} points."
        )

        detections.append(
            PatternDetection(
                category=result.detector_name,
                occurrences=occurrences,
                score_contribution=result.score_contribution,
                details=details,
                explanation=explanation,
            )
        )

    return detections
