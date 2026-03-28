import importlib
import pkgutil

import app.detectors as detectors_pkg
from app.detectors.base import BaseDetector


def discover_detectors(config: dict) -> list[BaseDetector]:
    _import_all_detector_modules()
    instances = []
    for cls in _find_subclasses(BaseDetector):
        key = cls.config_key()
        if key in config:
            instances.append(cls(config[key]))
    return instances


def _import_all_detector_modules() -> None:
    package_path = detectors_pkg.__path__
    for _, module_name, _ in pkgutil.iter_modules(package_path):
        if module_name not in ("base", "registry"):
            importlib.import_module(f"app.detectors.{module_name}")


def _find_subclasses(base: type) -> list[type]:
    result = []
    for cls in base.__subclasses__():
        try:
            cls.config_key()
            result.append(cls)
        except NotImplementedError:
            pass
        result.extend(_find_subclasses(cls))
    return result
