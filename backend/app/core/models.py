from datetime import datetime

from pydantic import BaseModel, Field


class TextStats(BaseModel):
    char_count: int
    word_count: int
    avg_word_length: float
    sentence_count: int


class TextAnalysis(BaseModel):
    text: str
    sentences: list[str]
    words: list[str]
    stats: TextStats


class MatchDetail(BaseModel):
    text: str
    position: int = 0


class DetectorResult(BaseModel):
    matches: list[MatchDetail] = Field(default_factory=list)
    raw_score: int = 0


class ScoredResult(BaseModel):
    detector_name: str
    matches: list[MatchDetail] = Field(default_factory=list)
    raw_score: int = 0
    weight: float = 1.0
    cap: int = 0
    score_contribution: int = 0


class LinguisticFactor(BaseModel):
    name: str
    value: float
    score_contribution: int = 0
    explanation: str = ""


class PatternDetection(BaseModel):
    category: str
    occurrences: int = 0
    score_contribution: int = 0
    details: list[str] = Field(default_factory=list)
    explanation: str = ""


class AggregatedScore(BaseModel):
    score: int
    classification: str
    contributions: list[dict] = Field(default_factory=list)


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1)


class AnalyzeResponse(BaseModel):
    score: int
    classification: str
    stats: TextStats
    linguistic_factors: list[LinguisticFactor] = Field(default_factory=list)
    pattern_detections: list[PatternDetection] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    timestamp: datetime
