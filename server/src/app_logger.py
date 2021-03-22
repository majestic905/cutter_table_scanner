import logging
from typing import Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

_formatter = logging.Formatter('[ %(levelname)-8s ] %(asctime)s: %(message)s')
_formatter.default_msec_format = '%s.%03d'

_handler: Optional[logging.FileHandler] = None


def setup_logger(file_path):
    global _handler

    if _handler is None:
        _handler = logging.FileHandler(file_path)
        _handler.setLevel(logging.DEBUG)
        _handler.setFormatter(_formatter)
        logger.addHandler(_handler)


def cleanup_logger():
    global _handler

    if _handler is not None:
        _handler.close()
        logger.removeHandler(_handler)
        _handler = None