[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# PyConfig

Configuration management using pydantic and a bit of sugar.

This library provides a loadconfig and saveconfig method to easily load and save python app configurations.


```python
# config.py file

from pydantic import BaseSettings


class DummyConfig(BaseSettings):
    """An app configuration class"""

    a: int = 1
    b: str = "ABC"


# The parameter to which the above instance will be assigned to.
CONFIG: DummyConfig

```

```
Load a default config

>>> import config
>>> from pyconfig.config import load_config
>>> config.CONFIG = load_config(config.DummyConfig)
>>> config.CONFIG

DummyConfig(a=1, b='ABC')
```

```
>>> import config
>>> from pyconfig.config import load_config
>>> from pathlib import Path

>>> config_file = Path("A_CONFIG_FILE.json")
>>> config.CONFIG = load_config(config.DummyConfig,config_file)

Load failed. Config file A_CONFIG_FILE.json does not exist. LOADING DEFAULTS 

>>> config.CONFIG

DummyConfig(a=1, b='ABC')

```

```
>>> config.CONFIG=load_config(config.DummyConfig,config_file,on_error_return_default=False)

Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "C:\Users\sander\Dropbox\data\aptana\pyconfig\pyconfig\config.py", line 55, in load_config
    conf_data = _load_json(config_file)
  File "C:\Users\sander\Dropbox\data\aptana\pyconfig\pyconfig\config.py", line 21, in _load_json
    raise CfgError(f"Load failed. Config file {config_file} does not exist.")
pyconfig.config.CfgError: Load failed. Config file A_CONFIG_FILE.json does not exist.

```