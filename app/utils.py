from app import logging
from app import settings

LOGGER = logging.setup_logger(
    'admin',
    level=settings.LOG_LEVEL
)