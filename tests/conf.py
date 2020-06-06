"""Helper."""

import logging
from enum import Enum
from pathlib import Path
from typing import Optional, Set
from uuid import UUID
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from pydantic import BaseSettings, SecretStr
from pydantic.color import Color
import datetime


_LOGGER = logging.getLogger(__name__)


class TableArray(BaseSettings):
    a: int = 1
    a_list: list = [{"a": 1}, {"b": True}]


class SimpleConfig(BaseSettings):
    a: int = 1
    b: str = "A string"


class SomeConfig(BaseSettings):
    a: int = 1
    b: str = "ABC"
    a_list: list = [
        1,
        2,
        3,
    ]


DICT_DUMMY_CONFIG = {"a": 1, "b": "ABC", "a_list": [1, 2, 3]}


class NestedConfig(BaseSettings):
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


class ConfigWithNone(BaseSettings):
    a: Optional[int] = None


class ConfigWithSet(BaseSettings):
    a: set = {1, 2, 3}


class TomlFailConfig(BaseSettings):
    """this config will fail as it has an inhomogenous array."""

    a: int = 1
    a_list: list = [
        1,
        2,
        3,
        "contents",
    ]


class MyEnum(Enum):
    foo = "bar"
    snap = "crackle"


class ConfigWithPydanticTypes(BaseSettings):
    uuid: UUID = "ebcdab58-6eb8-46fb-a190-d07a33e9eac8"
    ip_4_address: IPv4Address = IPv4Address("192.168.0.1")
    # color: Color = Color("#000")
    # color1: Color = Color((1, 12, 123))
    ip_v_6_address: IPv6Address = IPv6Address("::1:0:1")
    ip_v_4_interface: IPv4Interface = IPv4Interface("192.168.0.0/24")
    ip_v6_interface: IPv6Interface = IPv6Interface("2001:db00::/120")
    ip_v4_network: IPv4Network = IPv4Network("192.168.0.0/24")
    ip_v6_network: IPv6Network = IPv6Network("2001:db00::/120")
    date_time_1: datetime.datetime = datetime.datetime(2032, 1, 1, 1, 1)
    date_time_2: datetime.datetime = datetime.datetime(
        2032, 1, 1, 1, 1, tzinfo=datetime.timezone.utc
    )
    date_time_3: datetime.datetime = datetime.datetime(2032, 1, 1)
    date_time_4: datetime.time = datetime.time(12, 34, 56)
    date_time_5: datetime.timedelta = datetime.timedelta(
        days=12, seconds=34, microseconds=56
    )
    a_set: set = {1, 2, 3}
    # frozen_set: frozenset = frozenset([1, 2, 3])
    my_enum: MyEnum = MyEnum.foo
