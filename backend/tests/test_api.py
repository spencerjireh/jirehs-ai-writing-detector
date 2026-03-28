from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

CORPUS_DIR = Path(__file__).parent / "corpus"


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def _load_corpus(filename: str) -> str:
    return (CORPUS_DIR / filename).read_text()


def test_analyze_returns_200(client):
    response = client.post("/api/analyze", json={"text": "Hello world."})
    assert response.status_code == 200


def test_analyze_response_has_expected_fields(client):
    response = client.post("/api/analyze", json={"text": "Hello world."})
    data = response.json()
    assert "score" in data
    assert "classification" in data
    assert "stats" in data
    assert "linguistic_factors" in data
    assert "pattern_detections" in data
    assert "timestamp" in data
    assert "warnings" in data


def test_analyze_stats_correct(client):
    response = client.post("/api/analyze", json={"text": "Hello world."})
    stats = response.json()["stats"]
    assert stats["word_count"] == 2
    assert stats["sentence_count"] == 1
    assert stats["char_count"] == 12


def test_analyze_empty_text_returns_422(client):
    response = client.post("/api/analyze", json={"text": ""})
    assert response.status_code == 422


def test_analyze_missing_text_returns_422(client):
    response = client.post("/api/analyze", json={})
    assert response.status_code == 422


def test_analyze_clean_text_low_score(client):
    response = client.post(
        "/api/analyze",
        json={
            "text": (
                "I walked to the store yesterday because we ran out of milk. "
                "The weather was nice, maybe around 70 degrees. "
                "I also grabbed some bananas and a loaf of bread. "
                "On the way back I saw my neighbor walking her dog. "
                "We talked for a bit about the new restaurant that opened on Main Street. "
                "She said the pasta was good but the service was slow. "
                "I might try it this weekend if I can get a reservation."
            )
        },
    )
    data = response.json()
    assert data["score"] < 30
    assert data["classification"] == "Likely Human-Written"


def test_analyze_ai_text_high_score(client):
    response = client.post(
        "/api/analyze",
        json={
            "text": (
                "In today's rapidly evolving digital landscape, it's important to note that "
                "innovative solutions play a crucial role in streamlining operations. "
                "Let us delve into the multifaceted ecosystem of robust technologies that "
                "leverage cutting-edge approaches. Furthermore, experts agree that these "
                "transformative tools are not only remarkable but also groundbreaking. "
                "Studies show that a myriad of organisations have adopted holistic strategies "
                "to navigate the unprecedented challenges of the modern era. "
                "Despite initial setbacks, the industry offers tremendous opportunities for growth. "
                "From small startups to large enterprises, everyone knows that the paradigm shift "
                "has fostered a new wave of extraordinary innovation."
            )
        },
    )
    data = response.json()
    assert data["score"] >= 30  # Should score notably higher than clean text
    assert len(data["pattern_detections"]) > 0


def test_analyze_has_linguistic_factors(client):
    response = client.post(
        "/api/analyze",
        json={
            "text": (
                "The quick brown fox jumps over the lazy dog. "
                "She sells seashells by the seashore. "
                "Peter Piper picked a peck of pickled peppers."
            )
        },
    )
    data = response.json()
    assert len(data["linguistic_factors"]) > 0


def test_analyze_score_between_0_and_100(client):
    response = client.post(
        "/api/analyze",
        json={"text": "Some text to analyze for AI patterns."},
    )
    data = response.json()
    assert 0 <= data["score"] <= 100


# --- Corpus-based integration tests ---


def test_corpus_ai_essay_01_high_score(client):
    text = _load_corpus("ai_essay_01.txt")
    response = client.post("/api/analyze", json={"text": text})
    data = response.json()
    assert data["score"] >= 60, f"AI essay 01 scored {data['score']}, expected >= 60"
    assert data["classification"] == "Likely AI-Generated"


def test_corpus_ai_essay_02_high_score(client):
    text = _load_corpus("ai_essay_02.txt")
    response = client.post("/api/analyze", json={"text": text})
    data = response.json()
    assert data["score"] >= 60, f"AI essay 02 scored {data['score']}, expected >= 60"
    assert data["classification"] == "Likely AI-Generated"


def test_corpus_human_essay_01_low_score(client):
    text = _load_corpus("human_essay_01.txt")
    response = client.post("/api/analyze", json={"text": text})
    data = response.json()
    assert data["score"] < 30, f"Human essay 01 scored {data['score']}, expected < 30"
    assert data["classification"] == "Likely Human-Written"


def test_corpus_human_essay_02_low_score(client):
    text = _load_corpus("human_essay_02.txt")
    response = client.post("/api/analyze", json={"text": text})
    data = response.json()
    assert data["score"] < 30, f"Human essay 02 scored {data['score']}, expected < 30"
    assert data["classification"] == "Likely Human-Written"


def test_corpus_ai_essay_has_pattern_detections(client):
    text = _load_corpus("ai_essay_01.txt")
    response = client.post("/api/analyze", json={"text": text})
    data = response.json()
    assert len(data["pattern_detections"]) > 0
    categories = [d["category"] for d in data["pattern_detections"]]
    assert "Vocabulary" in categories


def test_corpus_response_schema(client):
    text = _load_corpus("ai_essay_01.txt")
    response = client.post("/api/analyze", json={"text": text})
    data = response.json()
    assert isinstance(data["score"], int)
    assert isinstance(data["classification"], str)
    assert isinstance(data["stats"]["word_count"], int)
    assert isinstance(data["linguistic_factors"], list)
    assert isinstance(data["pattern_detections"], list)
    assert isinstance(data["timestamp"], str)
    for factor in data["linguistic_factors"]:
        assert "name" in factor
        assert "value" in factor
        assert "score_contribution" in factor
        assert "explanation" in factor
    for detection in data["pattern_detections"]:
        assert "category" in detection
        assert "occurrences" in detection
        assert "score_contribution" in detection
        assert "details" in detection
