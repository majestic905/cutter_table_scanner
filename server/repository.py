import os
import shutil
from enum import Enum
from datetime import datetime


ROOT_PATH = os.path.join(os.path.dirname(__file__), 'scans')

if not os.path.exists(ROOT_PATH):
    os.mkdir(ROOT_PATH)


class File(Enum):
    LEFT_UPPER = 'left_upper.jpg'
    RIGHT_UPPER = 'right_upper.jpg'
    RIGHT_LOWER = 'right_lower.jpg'
    LEFT_LOWER = 'left_lower.jpg'
    RESULT = 'result.jpg'


def index():
    return [
        {
            'name': name,
            'createdAt': datetime.fromtimestamp(int(name)).strftime('%d %B %Y, %H:%M')
        } for name in os.listdir(ROOT_PATH)
    ]


def get(scan_id):
    file_path = os.path.join(ROOT_PATH, scan_id, File.RESULT.value)

    if not os.path.exists(file_path):
        raise FileNotFoundError

    return file_path


def create():
    ts = datetime.now().timestamp()
    scan_id = str(int(ts))
    path = os.path.join(ROOT_PATH, scan_id)
    os.mkdir(path)

    return {
        File.LEFT_UPPER: os.path.join(path, File.LEFT_UPPER.value),
        File.RIGHT_UPPER: os.path.join(path, File.RIGHT_UPPER.value),
        File.RIGHT_LOWER: os.path.join(path, File.RIGHT_LOWER.value),
        File.LEFT_LOWER: os.path.join(path, File.LEFT_LOWER.value),
        File.RESULT: os.path.join(path, File.RESULT.value),
    }


def clear():
    shutil.rmtree(ROOT_PATH)
    os.mkdir(ROOT_PATH)