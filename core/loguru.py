from loguru import logger

from core.config import settings

logger.add(settings.LOGGING_FILE, rotation='1 day', level='INFO')
