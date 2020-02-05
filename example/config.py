"""App config file.

Usage:

- Define your pydantic config objects here.
- Set a parameter to which the config will be instantiated. Actual assignment will
  take place in -for example- the app.py file.
"""

from pydantic import BaseSettings


class DummyConfig(BaseSettings):
    """An app configuration class"""

    a: int = 1
    b: str = "ABC"


# The parameter to which the above instance will be assigned to.
CONFIG: DummyConfig
