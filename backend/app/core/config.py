from pathlib import Path

import yaml

_REQUIRED_TOP_KEYS = {"vocabulary", "structural", "vague_language", "emphasis", "linguistic", "scoring"}


def load_config(path: str | Path = "config/detectors.yaml") -> dict:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path) as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValueError("Config must be a YAML mapping")

    missing = _REQUIRED_TOP_KEYS - config.keys()
    if missing:
        raise ValueError(f"Missing required config sections: {missing}")

    _validate_vocabulary(config["vocabulary"])
    _validate_scoring(config["scoring"])

    return config


def _validate_vocabulary(cfg: dict) -> None:
    for key in ("weight", "cap", "words", "phrases", "points_per_match"):
        if key not in cfg:
            raise ValueError(f"vocabulary section missing key: {key}")
    if not isinstance(cfg["words"], list) or not cfg["words"]:
        raise ValueError("vocabulary.words must be a non-empty list")
    if not isinstance(cfg["phrases"], list) or not cfg["phrases"]:
        raise ValueError("vocabulary.phrases must be a non-empty list")


def _validate_scoring(cfg: dict) -> None:
    if "classification" not in cfg:
        raise ValueError("scoring section missing 'classification'")
    cls = cfg["classification"]
    for key in ("likely_human", "possibly_ai"):
        if key not in cls:
            raise ValueError(f"scoring.classification missing key: {key}")
