from pathlib import Path

import pytest

from app.core.config import load_config
from app.preprocessing import preprocess


@pytest.fixture
def config():
    config_path = Path(__file__).parent.parent / "config" / "detectors.yaml"
    return load_config(config_path)


@pytest.fixture
def short_text():
    return "This is a short sentence."


@pytest.fixture
def medium_text():
    return (
        "The quick brown fox jumps over the lazy dog. "
        "She sells seashells by the seashore. "
        "Peter Piper picked a peck of pickled peppers. "
        "How much wood would a woodchuck chuck if a woodchuck could chuck wood?"
    )


@pytest.fixture
def ai_like_text():
    return (
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


@pytest.fixture
def human_like_text():
    return (
        "I walked to the store yesterday because we ran out of milk. "
        "The weather was nice, maybe around 70 degrees. "
        "I also grabbed some bananas and a loaf of bread. "
        "On the way back I saw my neighbor walking her dog. "
        "We talked for a bit about the new restaurant that opened on Main Street. "
        "She said the pasta was good but the service was slow. "
        "I might try it this weekend if I can get a reservation."
    )


@pytest.fixture
def sample_analysis(medium_text):
    return preprocess(medium_text)
