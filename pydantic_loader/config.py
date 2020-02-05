import json
import logging
from json import JSONDecodeError
from os import PathLike
from pathlib import Path
from typing import Type, Optional, Union

from pydantic import BaseSettings, ValidationError

_LOGGER = logging.getLogger(__name__)


class CfgError(Exception):
    pass


def _load_json(config_file: Union[Path, PathLike]) -> dict:
    if not config_file.exists():
        raise CfgError(f"Load failed. Config file {config_file} does not exist.")

    with open(config_file) as fl:
        try:
            dct = json.load(fl)
            return dct
        except JSONDecodeError as err:
            _LOGGER.exception(err)
            raise CfgError(f"Error parsing json file {config_file}")


def load_config(
    config: Type[BaseSettings],
    config_file: Optional[Path] = None,
    on_error_return_default=True,
):
    """Load a json config file and merge it into the config class

    Args:
        config: The config object to instantiate
        config_file: An optional config json file location
        on_error_return_default: By default loading is forgiving. On failure it will load
            default settings. Otherwise it will raise CfgError.

    Returns:
        A config instance


    raises:
        CfgError when loading fails.
    """
    conf_data = {}
    if config_file is not None:
        try:
            conf_data = _load_json(config_file)
        except CfgError as err:
            if not on_error_return_default:
                raise
            else:
                _LOGGER.error(f"{err} LOADING DEFAULTS ")
    try:
        instance = config(**conf_data)
    except ValidationError as err:
        _LOGGER.error(err)
        if not on_error_return_default:
            raise CfgError(str(err))
        instance = config()
    return instance


def save_config(config: BaseSettings, config_file: Path):
    """Serialize the config class and save it."""

    config_file.parent.mkdir(exist_ok=True)

    with open(config_file, "w") as fl:
        fl.write(config.json(indent=4))
