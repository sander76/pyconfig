"""Helper."""

import logging
from pathlib import Path

from pydantic_loader.config import PydanticConfig

_LOGGER = logging.getLogger(__name__)


class DummyConfig(PydanticConfig):
    a: int = 1
    b: str = "ABC"
    a_list: list = [
        1,
        2,
        3,
        "contents",
    ]


class NestedConfig(PydanticConfig):
    a: int = 1
    b: str = "ABC"
    c: DummyConfig = DummyConfig()
    pth: Path = Path("c:\\temp")
    dct: dict = {"a": 10, "value": True}
    result: bool = False


CONFIG: DummyConfig
