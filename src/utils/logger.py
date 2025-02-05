from loguru import logger
import sys

log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

logger.remove
logger.add(sys.stdout, level="DEBUG", format=log_format, colorize=True)
logger.add(sys.stderr, level="ERROR", format=log_format, colorize=True)
logger.add("logs/app.log", rotation="1 MB", level="DEBUG", format=log_format)

LOG = logger

__all__ = ["LOG"]