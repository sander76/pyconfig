import json
import logging
from json import JSONDecodeError
from pathlib import Path
from typing import Type, Optional, TypeVar

from pydantic import BaseSettings, ValidationError

_LOGGER = logging.getLogger(__name__)


class CfgError(Exception):
    pass


class Cfg:
    """A config util wrapper around a pydantic BaseSetting app config.

    """

    instance: BaseSettings

    def __init__(self, config: Type[BaseSettings]):
        self._config_type = config
        self._tp = type(config)

    def _load_json(self, config_file: Path) -> dict:
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
        self, config_file: Optional[Path] = None, on_error_return_default=True
    ):
        """Load a json config file and merge it into the config class

        raises:
            CfgError when loading fails.
            pydantic.ValidationError when validation fails
        """
        conf_data = {}
        if config_file is not None:
            try:
                conf_data = self._load_json(config_file)
            except CfgError as err:
                _LOGGER.error(err)
                if not on_error_return_default:
                    raise
        tp = type(self._config_type)
        _tp = self._config_type
        try:
            self.instance = self._config_type(**conf_data)
        except ValidationError as err:
            _LOGGER.error(err)
            if not on_error_return_default:
                raise
            self.instance = self._config_type()
        return self.instance

    def save_config(self, config_file: Path):
        """Serialize the config class and save it.

        Raises
            - CfgError when pydantic model is not loaded yet.
        """
        try:
            self.instance
        except AttributeError:
            raise CfgError("Error saving. Pydantic config not instantiated")

        config_file.parent.mkdir(exist_ok=True)

        with open(config_file, "w") as fl:
            fl.write(self.instance.json(indent=4))

    def get(self) -> BaseSettings:
        """Return the instantiated pydantic config instance."""
        try:
            self.instance
        except AttributeError:
            _LOGGER.error("Instance not created yet")

        raise CfgError("Config not loaded")
