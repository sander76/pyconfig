"""Pydantic config handling."""

import json
import logging
from json import JSONDecodeError
from os import PathLike
from pathlib import Path
from typing import Optional, Union, Callable
from pydantic import ValidationError, BaseSettings

_LOGGER = logging.getLogger(__name__)

__all__ = ["CfgError", "load_json", "save_json"]


class CfgError(Exception):
    """Config error."""


def _load_json(config_file: Union[Path, PathLike]) -> dict:
    """JSON loader."""
    with open(config_file) as json_file:
        try:
            dct = json.load(json_file)
            return dct
        except JSONDecodeError as err:
            _LOGGER.exception(err)
            raise CfgError(f"Error parsing json file {config_file}")


def load_json(pydantic_obj, config_file: Optional[Path], on_error_return_default=False):
    """Load a config file and merge it into the config class.

        Args:
            pydantic_obj: A pydantic class to instantiate
            config_file: An optional config file location.
            loader: which loader to use for deserialization. (json, toml or yaml)
            on_error_return_default: By default loading is forgiving: On failure it will load
                default settings. Otherwise it will raise CfgError.


        Returns:
            A config instance

        raises:
            CfgError when loading fails and on_error_return_default is False.
        """
    return load_config(
        pydantic_obj,
        config_file=config_file,
        loader=_load_json,
        on_error_return_default=on_error_return_default,
    )


def load_config(
    pydantic_obj,
    config_file: Optional[Path],
    loader: Callable = _load_json,
    on_error_return_default=False,
):
    """Load a config file and merge it into the config class.

    Args:
        pydantic_obj: A pydantic class to instantiate
        config_file: An optional config file location.
        loader: which loader to use for deserialization. (json, toml or yaml)
        on_error_return_default: By default loading is forgiving: On failure it will load
            default settings. Otherwise it will raise CfgError.


    Returns:
        A config instance

    raises:
        CfgError when loading fails and on_error_return_default is False.
    """
    if config_file is None:
        return pydantic_obj()

    conf_data = {}
    try:
        conf_data = loader(config_file)
    except FileNotFoundError:
        if not on_error_return_default:
            raise CfgError(f"Config file not found ({config_file})")
        _LOGGER.error("Config file not found. LOADING DEFAULTS. %s", config_file)

    except CfgError as err:
        if not on_error_return_default:
            raise CfgError(str(err))
        _LOGGER.error(f"{err} LOADING DEFAULTS ")
    try:
        instance = pydantic_obj(**conf_data)
    except ValidationError as err:
        _LOGGER.error(err)
        if not on_error_return_default:
            raise CfgError(str(err))
        instance = pydantic_obj()
    return instance


def save_json(config: BaseSettings, config_file: Path, make_path=False):
    """Serialize the config class and save it to a json file.

    Args:
        config: Pydantic config instance
        config_file: The output file
        make_path: If True the path will be created.

    Raises:
        FileNotFoundError: If make_path=False and the folder does not consist.
    """
    if make_path:
        config_file.parent.mkdir(exist_ok=True)

    with open(config_file, "w") as json_file:
        json_file.write(config.json(indent=4))
