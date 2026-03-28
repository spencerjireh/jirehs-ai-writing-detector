from app.core.models import AggregatedScore, LinguisticFactor, ScoredResult


def aggregate(
    detector_results: list[ScoredResult],
    linguistic_factors: list[LinguisticFactor],
    config: dict,
) -> AggregatedScore:
    contributions: list[dict] = []

    for r in detector_results:
        contributions.append({
            "name": r.detector_name,
            "type": "detector",
            "score_contribution": r.score_contribution,
        })

    for f in linguistic_factors:
        contributions.append({
            "name": f.name,
            "type": "linguistic",
            "score_contribution": f.score_contribution,
        })

    raw_total = sum(c["score_contribution"] for c in contributions)

    if raw_total > 100:
        scale = 100 / raw_total
        for c in contributions:
            c["score_contribution"] = int(c["score_contribution"] * scale)
        total = sum(c["score_contribution"] for c in contributions)
        # Distribute rounding remainder to largest contributor
        remainder = 100 - total
        if remainder > 0 and contributions:
            contributions.sort(key=lambda c: c["score_contribution"], reverse=True)
            contributions[0]["score_contribution"] += remainder
        total = 100
    else:
        total = raw_total

    classification = classify(total, config)

    return AggregatedScore(
        score=total,
        classification=classification,
        contributions=contributions,
    )


def classify(score: int, config: dict) -> str:
    thresholds = config.get("scoring", {}).get("classification", {})
    likely_human = thresholds.get("likely_human", 30)
    possibly_ai = thresholds.get("possibly_ai", 60)

    if score < likely_human:
        return "Likely Human-Written"
    elif score < possibly_ai:
        return "Possibly AI-Generated"
    else:
        return "Likely AI-Generated"
