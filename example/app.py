from example import config
from pyconfig import load_config


def app():
    """Entry point for the app. You can load your config here."""

    # Load a default config object.
    val = load_config(config.DummyConfig)
    assert isinstance(val, config.DummyConfig)
