import json
import logging
from json import JSONDecodeError
from os import PathLike
from pathlib import Path
from typing import Optional, Union

import toml
from pydantic import BaseSettings, ValidationError
from toml.decoder import TomlDecodeError

from pydantic_loader.encode import encode_pydantic_obj

_LOGGER = logging.getLogger(__name__)

__all__ = ["CfgError", "PydanticConfig", "save_config"]


class CfgError(Exception):
    pass


def _load(config_file: Union[Path, PathLike]) -> dict:
    if not config_file.exists():
        raise CfgError(f"Load failed. Config file {config_file} does not exist.")
    if config_file.suffix == ".json":
        return _load_json(config_file)
    elif config_file.suffix in (".toml", ".tml"):
        return _load_toml(config_file)

    raise CfgError("Unable to determine type of config file (Json or Toml)")


def _load_json(config_file: Union[Path, PathLike]) -> dict:
    with open(config_file) as fl:
        try:
            dct = json.load(fl)
            return dct
        except JSONDecodeError as err:
            _LOGGER.exception(err)
            raise CfgError(f"Error parsing json file {config_file}")


def _load_toml(config_file: Union[Path, PathLike]) -> dict:
    try:
        with open(config_file) as fl:
            dct = toml.load(fl)
            return dct
    except TomlDecodeError as err:
        raise CfgError(str(err))


class PydanticConfig(BaseSettings):
    """Base class for config settings."""

    @classmethod
    def load_config(
        cls, config_file: Optional[Path] = None, on_error_return_default=False
    ):
        """Load a json config file and merge it into the config class.

        Args:
            config_file: An optional config json file location.
            on_error_return_default: By default loading is forgiving. On failure it will load
                default settings. Otherwise it will raise CfgError.

        Returns:
            A config instance

        raises:
            CfgError when loading fails and on_error_return_default is False.
        """
        conf_data = {}
        if config_file is not None:
            try:
                conf_data = _load(config_file)
            except CfgError as err:
                if not on_error_return_default:
                    raise
                else:
                    _LOGGER.error(f"{err} LOADING DEFAULTS ")
        try:
            instance = cls(**conf_data)
        except ValidationError as err:
            _LOGGER.error(err)
            if not on_error_return_default:
                raise CfgError(str(err))
            instance = cls()
        return instance

    def toml(self) -> str:
        """
        Generate a TOML representation of the model.

        Raises:
            CfgError when object cannot be serialized.
        """
        dct = encode_pydantic_obj(self)
        try:
            val = toml.dumps(dct)
            return val
        except Exception as err:
            print(err)
        except TomlDecodeError as err:
            raise CfgError(err)


def save_config(config: PydanticConfig, config_file: Path):
    """Serialize the config class and save it."""

    config_file.parent.mkdir(exist_ok=True)

    if config_file.suffix in (".toml", ".tml"):
        save_toml(config, config_file)
    else:
        with open(config_file, "w") as fl:
            fl.write(config.json(indent=4))


def save_toml(config: PydanticConfig, config_file: Path):
    """Serialize the config class and save it as a toml file."""
    config_file.parent.mkdir(exist_ok=True)
    with open(config_file, "w") as fl:
        fl.write(config.toml())
