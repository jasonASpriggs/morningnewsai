"""
Load the configurations in the ./config/ folder
"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter

from backend.models import NewsSource, NewsTopic

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIRECTORY = PROJECT_ROOT / "config"

# Use TypeAdapter to make NewSource and NewsTopic lists loadable and compatible with pydantic
source_list_adapter = TypeAdapter(list[NewsSource])
topic_list_adapter = TypeAdapter(list[NewsTopic])


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with path.open(encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError(f"Configuration must contain a YAML object: {path}")

    return data


def load_sources(
    path: Path = CONFIG_DIRECTORY / "sources.yaml",
) -> list[NewsSource]:
    data = load_yaml(path)
    return source_list_adapter.validate_python(data.get("sources", []))


def load_topics(
    path: Path = CONFIG_DIRECTORY / "default_topics.yaml",
) -> list[NewsTopic]:
    data = load_yaml(path)
    return topic_list_adapter.validate_python(data.get("topics", []))
