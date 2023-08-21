import logging
import sys

from core.configs import settings

FORMAT = '%(asctime)s  %(name)s:%(lineno)s -> (%(levelname)s)  %(message)s'

logging.getLogger("urllib3").setLevel(logging.INFO)


def get_logger(n=__name__):
    formatter = logging.Formatter(FORMAT)
    logger = logging.getLogger(n)
    logger.setLevel(settings.LOG_LEVEL)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(settings.LOG_LEVEL)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = 0
    return logger
