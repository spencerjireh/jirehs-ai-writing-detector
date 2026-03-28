import logging

from fastapi import APIRouter, Request

from app.analyzers.linguistic import analyze_linguistics
from app.core.models import (
    AnalyzeRequest,
    AnalyzeResponse,
    LinguisticFactor,
    ScoredResult,
)
from app.preprocessing import preprocess
from app.report.builder import build_report
from app.scoring.aggregator import aggregate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/analyze")
async def analyze_text(request: Request, body: AnalyzeRequest) -> AnalyzeResponse:
    config = request.app.state.config
    detectors = request.app.state.detectors

    analysis = preprocess(body.text)
    warnings: list[str] = []

    # Run all detectors with graceful degradation
    all_scored: list[ScoredResult] = []
    for detector in detectors:
        try:
            results = detector.score_all(analysis)
            all_scored.extend(results)
        except Exception as exc:
            logger.warning("Detector %s failed: %s", detector.name, exc)
            warnings.append(f"Detector '{detector.name}' was skipped due to an error")

    # Run linguistic analyzers with graceful degradation
    linguistic_factors: list[LinguisticFactor] = []
    try:
        linguistic_factors = analyze_linguistics(analysis, config.get("linguistic", {}))
    except Exception as exc:
        logger.warning("Linguistic analysis failed: %s", exc)
        warnings.append("Linguistic analysis was skipped due to an error")

    # Aggregate scores and classify
    aggregated = aggregate(all_scored, linguistic_factors, config)

    # Build and return report
    return build_report(analysis, all_scored, linguistic_factors, aggregated, warnings)
