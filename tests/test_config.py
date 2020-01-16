import json
import logging

import pytest
from pydantic import BaseSettings, ValidationError

from pyconfig.config import Cfg, CfgError

_LOGGER = logging.getLogger(__name__)


class DummyConfig(BaseSettings):
    a: int = 1
    b: str = "ABC"


def validate_equivalence(value: DummyConfig):
    expected = DummyConfig()
    assert expected.a == value.a
    assert expected.b == value.b


dummy_js = {"a": 2, "b": "DEF"}
invalid_dummy_js = {"a": 10, "c": 5}


class TestConfig(Cfg):
    instance: DummyConfig


@pytest.fixture
def dummy_config():
    return TestConfig(DummyConfig)


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


def test_get_config(dummy_config):
    _cfg = dummy_config.load_config()
    assert isinstance(_cfg, DummyConfig)


def test_get_config_not_loaded(dummy_config):

    with pytest.raises(CfgError):
        dummy_config.get()


def test_load_config_not_found(tmp_path, dummy_config):
    """A non existing file is provided. Should return default config"""

    non_existing_config = tmp_path / "non_exist.json"

    _cfg = dummy_config.load_config(non_existing_config)

    validate_equivalence(_cfg)


def test_load_config_not_found_throw(tmp_path, dummy_config):
    """A non existing file is provided. Should raise exceptoin"""

    non_existing_config = tmp_path / "non_exist.json"

    with pytest.raises(CfgError):
        dummy_config.load_config(non_existing_config, on_error_return_default=False)


def test_load_config_file_success(config_file, dummy_config):
    _cfg = dummy_config.load_config(config_file)
    assert _cfg.a == dummy_js["a"]
    assert _cfg.b == dummy_js["b"]


def test_load_invalid_config(invalid_config_file, dummy_config):
    """Load an invalid config. Should return a default value"""
    _cfg = dummy_config.load_config(invalid_config_file)
    validate_equivalence(_cfg)


def test_load_invalid_config_raise(invalid_config_file, dummy_config):
    """Load an invalid config. Should raise a vaildation error."""
    with pytest.raises(ValidationError):
        dummy_config.load_config(invalid_config_file, on_error_return_default=False)


def test_save_pydantic(tmp_path, dummy_config):
    """Saving a config and checking file existence"""

    new_file = tmp_path / "config.json"
    assert not new_file.exists()

    dummy_config.load_config()

    dummy_config.save_config(new_file)
    assert new_file.exists()


def test_save_pydantic_fail(tmp_path, dummy_config):
    new_file = tmp_path / "config.json"

    with pytest.raises(CfgError):
        dummy_config.save_config(new_file)
