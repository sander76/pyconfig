import json
import logging

import pytest
from pydantic import ValidationError

from pydantic_loader.config import CfgError, load_config, save_config
from tests import conf

from importlib import reload

_LOGGER = logging.getLogger(__name__)


def validate_equivalence(value: conf.DummyConfig):
    expected = conf.DummyConfig()
    assert expected.a == value.a
    assert expected.b == value.b


dummy_js = {"a": 2, "b": "DEF"}
invalid_dummy_js = {"a": 10, "c": 5}


@pytest.fixture
def config_file(tmp_path):
    conf_file = tmp_path / "config_file.json"
    with open(conf_file, "w") as fl:
        json.dump(dummy_js, fl)
    return conf_file


@pytest.fixture
def invalid_config_file(tmp_path):
    conf_file = tmp_path / "config_file.json"
    with open(conf_file, "w") as fl:
        json.dump(invalid_dummy_js, fl)
    return conf_file


def test_unspecified_config():
    # todo: reloading does not work. once conf.CONFIG is defined it does not get reset.
    reload(conf)
    with pytest.raises(AttributeError):
        config = conf.CONFIG


def test_load_config_success(config_file):
    conf.CONFIG = load_config(conf.DummyConfig, config_file)
    assert isinstance(conf.CONFIG, conf.DummyConfig)


def test_load_config_not_found(tmp_path):
    """A non existing file is provided. Should return default config"""

    non_existing_config = tmp_path / "non_exist.json"

    _cfg = load_config(conf.DummyConfig, non_existing_config)

    validate_equivalence(_cfg)


def test_load_config_not_found_throw(tmp_path):
    """A non existing file is provided. Should raise exceptoin"""

    non_existing_config = tmp_path / "non_exist.json"

    with pytest.raises(CfgError):
        load_config(
            conf.DummyConfig, non_existing_config, on_error_return_default=False
        )


def test_load_config_file_success(config_file):
    _cfg = load_config(conf.DummyConfig, config_file)
    assert _cfg.a == dummy_js["a"]
    assert _cfg.b == dummy_js["b"]


def test_load_invalid_config(invalid_config_file):
    """Load an invalid config. Should return a default value"""
    _cfg = load_config(conf.DummyConfig, invalid_config_file)
    validate_equivalence(_cfg)


def test_load_invalid_config_raise(invalid_config_file):
    """Load an invalid config. Should raise a vaildation error."""
    with pytest.raises(CfgError):
        load_config(
            conf.DummyConfig, invalid_config_file, on_error_return_default=False
        )


def test_save_pydantic(tmp_path):
    """Saving a config and checking file existence"""

    new_file = tmp_path / "config.json"
    assert not new_file.exists()

    config = load_config(conf.DummyConfig)

    save_config(config, new_file)
    assert new_file.exists()
