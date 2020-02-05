import logging

from pydantic import BaseSettings

_LOGGER = logging.getLogger(__name__)


class DummyConfig(BaseSettings):
    a: int = 1
    b: str = "ABC"


CONFIG: DummyConfig
