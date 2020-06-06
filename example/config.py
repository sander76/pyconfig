"""Simple example."""
from pathlib import Path

from pydantic_loader import load_json, save_json
from pydantic import BaseSettings


class DummyConfig(BaseSettings):
    """An app configuration class"""

    a: int = 1
    b: str = "ABC"


config = DummyConfig()

save_json(config, Path("config.json"))

config = load_json(DummyConfig, Path("config.json"))
