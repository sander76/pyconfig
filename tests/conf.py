"""Helper."""

import logging

from pydantic_loader.config import PydanticConfig

_LOGGER = logging.getLogger(__name__)


class DummyConfig(PydanticConfig):
    a: int = 1
    b: str = "ABC"


CONFIG: DummyConfig
