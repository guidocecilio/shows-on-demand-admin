from admin import logging
from admin import settings

LOGGER = logging.setup_logger(
    'admin',
    level=settings.LOG_LEVEL
)