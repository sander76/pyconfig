import json
import logging
from pathlib import Path

import pytest

from pydantic_loader import config
from pydantic_loader import toml_config
from pydantic_loader import yaml_config
from tests import conf

_LOGGER = logging.getLogger(__name__)


def non_existing_config_file(tmp_path):
    """Return a non-existing config file and its pydantic object."""
    return tmp_path / "non_exist.json", conf.SomeConfig


def invalid_json_file(tmp_path):
    """Return a config file and its pydantic object.

    The config file will fail pydantic loading.
    """
    false_dict = {"invalid_key": "abc"}
    file = tmp_path / "false_json.json"
    with open(file, "w") as fl:
        json.dump(false_dict, fl)
    return file, conf.SomeConfig


def invalid_toml_file(tmp_path):
    """Return a config file which makes pydantic fail and its pydantic object."""

    invalid_toml_sting = 'invalid_key= "invalid_value"'

    file = tmp_path / "false.toml"
    with open(file, "w") as fl:
        fl.write(invalid_toml_sting)
    return file, conf.SomeConfig


def invalid_yaml_file(tmp_path):
    """Return a config file which makes pydantic fail and its pydantic object."""

    invalid_yaml_sting = "invalid_key: invalid_value"

    file = tmp_path / "false.yaml"
    with open(file, "w") as fl:
        fl.write(invalid_yaml_sting)
    return file, conf.SomeConfig


@pytest.mark.parametrize(
    "config_file_name,loader,saver",
    [
        ("config.json", config.load_config, config.save_json),
        (Path("nested/config.json"), config.load_config, config.save_json),
        ("config.toml", toml_config.load_toml, toml_config.save_toml),
        (Path("nested/config.toml"), toml_config.load_toml, toml_config.save_toml),
        ("config.yaml", yaml_config.load_yaml, yaml_config.save_yaml),
        (Path("nested/config.yaml"), yaml_config.load_yaml, yaml_config.save_yaml),
    ],
)
def test_save_load_config(config_file_name, loader, saver, pydantic_config, tmp_path):
    output_path = tmp_path / config_file_name

    saver(pydantic_config, output_path, make_path=True)
    loaded_config = loader(pydantic_config.__class__, output_path)

    assert loaded_config == pydantic_config


@pytest.mark.parametrize(
    "config_file_name,saver",
    [
        (Path("nested/config.json"), config.save_json),
        (Path("nested/config.toml"), toml_config.save_toml),
        (Path("nested/config.yaml"), yaml_config.save_yaml),
    ],
)
def test_save_config_nested_folder(config_file_name, saver, pydantic_config, tmp_path):
    output_path = tmp_path / config_file_name

    with pytest.raises(FileNotFoundError):
        saver(pydantic_config, output_path)


def get_config_file_and_loader():
    return [
        (non_existing_config_file, config.load_config),
        (invalid_json_file, config.load_config),
        (invalid_toml_file, toml_config.load_toml),
        (non_existing_config_file, toml_config.load_toml),
        (invalid_yaml_file, yaml_config.load_yaml),
        (non_existing_config_file, yaml_config.load_yaml),
    ]


@pytest.mark.parametrize(
    "config_file_function,config_loader", get_config_file_and_loader()
)
def test_load_config_fail_return_default(config_file_function, config_loader, tmp_path):
    config_file, pydantic_object = config_file_function(tmp_path)

    cfg = config_loader(
        pydantic_object, config_file=config_file, on_error_return_default=True
    )

    assert isinstance(cfg, pydantic_object)


@pytest.mark.parametrize(
    "config_file_function,config_loader", get_config_file_and_loader()
)
def test_load_config_fail_raise(config_file_function, config_loader, tmp_path):
    """False config is provided. Should raise CfgError."""
    config_file, pydantic_object = config_file_function(tmp_path)

    with pytest.raises(config.CfgError):
        config_loader(pydantic_object, config_file=config_file)
