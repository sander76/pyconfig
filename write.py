import logging
from pathlib import Path

from pydantic_loader import save_config
from tests.conf import NestedConfig, TableArray

_LOGGER = logging.getLogger(__name__)

config = TableArray()
output_toml = Path.home() / "config.toml"
save_config(config, output_toml)
