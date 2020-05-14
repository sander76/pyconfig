import logging
from typing import Any
from collections import abc
from pydantic.json import pydantic_encoder

_LOGGER = logging.getLogger(__name__)


def loop_over_list(lst) -> list:
    new_list = []
    for itm in lst:
        new_list.append(encode_pydantic_obj(itm))
    return new_list


def loop_over_dict(obj) -> dict:
    new_dict = {}
    for key, value in obj.items():
        new_dict[key] = encode_pydantic_obj(value)
    return new_dict


def encode_pydantic_obj(obj: Any) -> Any:
    """Take an object and encode it to basic python types iteratively.

    The result should be ready to be encoded to TOML. (Or another data type)"""
    try:
        result = pydantic_encoder(obj)
    except TypeError:
        result = obj

    if isinstance(result, abc.Mapping):
        return loop_over_dict(result)
    if isinstance(result, abc.Iterable) and not isinstance(result, str):
        return loop_over_list(result)
    return result
