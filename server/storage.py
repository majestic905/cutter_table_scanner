import os
import shutil
from datetime import datetime
from scan import ScanFile

DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), 'data')
PARAMS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', ScanFile.PARAMS.value)
SCANS_DIR_PATH = os.path.join(os.path.dirname(__file__), 'data', 'scans')


if not os.path.exists(DATA_DIR_PATH):
    os.mkdir(DATA_DIR_PATH)

if not os.path.exists(SCANS_DIR_PATH):
    os.mkdir(SCANS_DIR_PATH)


def path_for_scan_file(scan_id: str, file: ScanFile) -> str:
    return os.path.join(SCANS_DIR_PATH, scan_id, file.value)


def path_for_params_file() -> str:
    return PARAMS_FILE_PATH


def scans_list():
    return [
        {'name': name, 'createdAt': datetime.fromtimestamp(int(name)).strftime('%d %B %Y, %H:%M')}
        for name in os.listdir(SCANS_DIR_PATH)
    ]


def create_scan_dir(scan_id):
    path = os.path.join(SCANS_DIR_PATH, scan_id)

    if os.path.exists(path):
        raise FileExistsError()

    return os.mkdir(path)


def copy_params_file(scan_id):
    path = os.path.join(SCANS_DIR_PATH, scan_id, ScanFile.PARAMS.value)
    shutil.copy(PARAMS_FILE_PATH, path)


def clear_scans_dir():
    shutil.rmtree(SCANS_DIR_PATH)
    os.mkdir(SCANS_DIR_PATH)
