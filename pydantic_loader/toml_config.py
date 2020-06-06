"""Pydantic loader using TOML serialization."""

import logging
from os import PathLike
from pathlib import Path
from typing import Union, Optional

import toml
from pydantic import BaseSettings
from toml.decoder import TomlDecodeError

import pydantic_loader
from pydantic_loader.encode import encode_pydantic_obj

_LOGGER = logging.getLogger(__name__)


def _load_toml(config_file: Union[Path, PathLike]) -> dict:
    """Load a toml file and return a dict.

    Returns:
        CfgError when something (anything) is wrong.
    """
    try:
        with open(config_file) as toml_tile:
            dct = toml.load(toml_tile)
            return dct
    except TomlDecodeError as err:
        raise pydantic_loader.CfgError(str(err))


def save_toml(config: BaseSettings, config_file: Path, make_path=False):
    """Serialize the config class and save it as a toml file.

    Args:
        config: Pydantic config instance
        config_file: The output file
        make_path: If True the path will be created.

    Raises:
        FileNotFoundError: If make_path=False and the folder does not consist.
    """
    if make_path:
        config_file.parent.mkdir(exist_ok=True)

    dct = encode_pydantic_obj(config)
    try:
        val = toml.dumps(dct)
    except TomlDecodeError as err:
        raise pydantic_loader.CfgError(err)
    except Exception as err:
        raise pydantic_loader.CfgError(err)

    with open(config_file, "w") as toml_file:
        toml_file.write(val)


def load_toml(pydantic_obj, config_file: Optional[Path], on_error_return_default=False):
    """Load a config file and merge it into the config class.

    Args:
        pydantic_obj: A pydantic class to instantiate
        config_file: An optional config file location.
        on_error_return_default: If true loading is forgiving:
          On fail it will load default settings. Otherwise it will raise CfgError.


    Returns:
        A config instance

    raises:
        CfgError when loading fails and on_error_return_default is False.
    """
    return pydantic_loader.config.load_config(
        pydantic_obj,
        config_file,
        loader=_load_toml,
        on_error_return_default=on_error_return_default,
    )
