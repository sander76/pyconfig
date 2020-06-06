from pydantic import BaseSettings[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/sander76/pyconfig/branch/master/graph/badge.svg)](https://codecov.io/gh/sander76/pyconfig)

# PyConfig

Configuration management using pydantic and a bit of sugar.

This library provides a load and save method for pydantic config settings.

Settings can be saved in `.json` and `.toml` format. The latter is experimental.

# Installation

`pip install pydantic_loader` for loading and saving json files.

`pip install pydantic_loader[yaml]` for loading and saving yaml and json files.

`pip install pydantic_loader[toml]` for loading and saving toml and json.


```python
"""Simple example."""
from pathlib import Path

from pydantic_loader import load_json, save_json
from pydantic import BaseSettings


class DummyConfig(BaseSettings):
    """An app configuration class"""

    a: int = 1
    b: str = "ABC"


config = DummyConfig()

save_json(config, Path("config.json"))

config = load_json(DummyConfig, Path("config.json"))
```