import logging
import pytest
from . import conf

_LOGGER = logging.getLogger(__name__)


@pytest.fixture(
    params=[
        conf.NestedConfig(a=50),
        conf.SomeConfig(),
        conf.ConfigWithNone(),
        conf.ConfigWithSet(),
        conf.ConfigWithPydanticTypes(),
    ]
)
def pydantic_config(request):
    """Return pydantic config objects."""
    return request.param
