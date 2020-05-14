"""Helper."""

import logging
from pathlib import Path
from typing import Optional, Set

from pydantic_loader.config import PydanticConfig

_LOGGER = logging.getLogger(__name__)


class TableArray(PydanticConfig):
    a: int = 1
    a_list: list = [{"a": 1}, {"b": True}]


class SimpleConfig(PydanticConfig):
    a: int = 1
    b: str = "A string"


class SomeConfig(PydanticConfig):
    a: int = 1
    b: str = "ABC"
    a_list: list = [
        1,
        2,
        3,
    ]


DICT_DUMMY_CONFIG = {"a": 1, "b": "ABC", "a_list": [1, 2, 3]}


class NestedConfig(PydanticConfig):
    a: int = 1
    b: str = "ABC"
    dummy: SomeConfig = SomeConfig()
    pth: Path = Path("c:\\temp")
    dct: dict = {"a": 10, "value": True}
    result: bool = False
    flt: float = 0.3
    bt: bytes = b"abc"


DICT_NESTED_CONFIG = {
    "a": 1,
    "b": "ABC",
    "dummy": DICT_DUMMY_CONFIG,
    "pth": "c:\\temp",
    "dct": {"a": 10, "value": True},
    "result": False,
    "flt": 0.3,
    "bt": "abc",
}

CONFIG: SomeConfig


class ConfigWithNone(PydanticConfig):
    a: Optional[int] = None


class ConfigWithSet(PydanticConfig):
    a: set = {1, 2, 3}


class TomlFailConfig(PydanticConfig):
    """this config will fail as it has an inhomogenous array."""

    a: int = 1
    a_list: list = [
        1,
        2,
        3,
        "contents",
    ]
