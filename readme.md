[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/sander76/pyconfig/branch/master/graph/badge.svg)](https://codecov.io/gh/sander76/pyconfig)

# PyConfig

Configuration management using pydantic and a bit of sugar.

This library provides a load and save method for pydantic config settings.

Settings can be saved in `.json` and `.toml` format. The latter is experimental.

```python
"""Small example"""
from pydantic_loader import PydanticConfig,load_config


class DummyConfig(PydanticConfig):
    """An app configuration class
    
    Define this class according to pydantic BaseSettings.
    """

    a: int = 1
    b: str = "ABC"

# Load a json file with config data and include it in the DummyConfig.
config = DummyConfig.load_config("a json config file.json")

# Providing a non existing file will raise a CfgError
# It will return a default instance of the config class when on_error_return_default=True
config = DummyConfig.load_config("invalid_file.json", on_error_return_default=True)

# Using the load_config allows for loading pydantic `BaseSettings` class
config = load_config(DummyConfig,"Json or Toml config file.")

# SAVE A CONFIG

from pydantic_loader import save_config

# Your config file should have the extension .toml, .tml or .json to determine how to encode
# the pydantic instance.
save_config(config,"a json or toml config file")
```