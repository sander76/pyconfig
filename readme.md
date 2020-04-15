[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# PyConfig

Configuration management using pydantic and a bit of sugar.

This library provides a load and save method for pydantic config settings.


```python
"""Small example"""
from pydantic_loader import PydanticConfig


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
```
