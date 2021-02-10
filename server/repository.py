import os
import shutil
import cv2
from datetime import datetime
from storage import ScanFile


ROOT_PATH = os.path.join(os.path.dirname(__file__), 'scans')

if not os.path.exists(ROOT_PATH):
    os.mkdir(ROOT_PATH)

def index():
    return [
        {
            'name': name,
            'createdAt': datetime.fromtimestamp(int(name)).strftime('%d %B %Y, %H:%M')
        } for name in os.listdir(ROOT_PATH)
    ]


def get(scan_id):
    file_path = os.path.join(ROOT_PATH, scan_id, ScanFile.RESULT.value)

    if not os.path.exists(file_path):
        raise FileNotFoundError

    return file_path


def put_cv2_image(scan_id, file_name, image):
    file_path = os.path.join(ROOT_PATH, scan_id, file_name)
    cv2.imwrite(file_path, image)


def put_copy(scan_id, file_name, src_file_path):
    dst_file_path = os.path.join(ROOT_PATH, scan_id, file_name)
    shutil.copy(src_file_path, dst_file_path)


def create_storage(scan_id: str):
    path = os.path.join(ROOT_PATH, scan_id)
    os.mkdir(path)


def clear():
    shutil.rmtree(ROOT_PATH)
    os.mkdir(ROOT_PATH)