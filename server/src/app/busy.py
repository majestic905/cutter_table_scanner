from functools import wraps
from http import HTTPStatus as status
from .paths import BUSY_FILE_PATH


def is_busy():
    return BUSY_FILE_PATH.exists()


def acquire_busy_state():
    BUSY_FILE_PATH.touch()


def release_busy_state():
    if BUSY_FILE_PATH.exists():
        BUSY_FILE_PATH.unlink()


def check_is_busy(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if is_busy():
            return {'message': 'Scan task is running!'}, status.SERVICE_UNAVAILABLE
        return f(*args, **kwargs)
    return wrap


# since server can shutdown totally unexpectedly, delete file on server startup, if exists
release_busy_state()
