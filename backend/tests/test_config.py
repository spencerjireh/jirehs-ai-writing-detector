import pytest
import yaml
from pathlib import Path

from app.core.config import load_config


def test_valid_config_loads(config):
    assert "vocabulary" in config
    assert "structural" in config
    assert "vague_language" in config
    assert "emphasis" in config
    assert "linguistic" in config
    assert "scoring" in config


def test_config_vocabulary_has_words(config):
    assert len(config["vocabulary"]["words"]) > 0
    assert len(config["vocabulary"]["phrases"]) > 0
    assert config["vocabulary"]["points_per_match"] > 0


def test_config_scoring_thresholds(config):
    cls = config["scoring"]["classification"]
    assert cls["likely_human"] == 30
    assert cls["possibly_ai"] == 60
    assert cls["likely_human"] < cls["possibly_ai"]


def test_missing_file_raises_error():
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent.yaml")


def test_missing_keys_raises_error(tmp_path):
    bad_config = tmp_path / "bad.yaml"
    bad_config.write_text(yaml.dump({"vocabulary": {}}))
    with pytest.raises(ValueError, match="Missing required config sections"):
        load_config(bad_config)


def test_invalid_yaml_raises_error(tmp_path):
    bad_config = tmp_path / "bad.yaml"
    bad_config.write_text("just a string")
    with pytest.raises(ValueError, match="Config must be a YAML mapping"):
        load_config(bad_config)
