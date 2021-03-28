import logging
from functools import wraps
from time import time
from .paths import SCAN_LOG_PATH


_formatter = logging.Formatter('[ %(asctime)s ]: %(message)s')
_formatter.default_msec_format = '%s.%03d'

_handler = logging.FileHandler(SCAN_LOG_PATH)
_handler.setLevel(logging.DEBUG)
_handler.setFormatter(_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(_handler)


def read_log():
    return SCAN_LOG_PATH.read_text()


def clear_log():
    open(SCAN_LOG_PATH, "w").close()


def log_timing(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        logger.info(f'[ {f.__name__} ] start')
        start = time()
        result = f(*args, **kwargs)
        end = time()
        logger.info(f'[ {f.__name__} ] end, took {round(end - start, 2)} seconds')
        return result
    return wrap
