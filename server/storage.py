import os
import shutil
from datetime import datetime
from enum import Enum
from camera import CameraPosition


class ImageLevel(Enum):
    ORIGINAL = 'original'
    UNDISTORTED = 'undistorted'
    PROJECTED = 'projected'


class ScanFile(Enum):
    LU_ORIGINAL = 'left_upper_original.jpg'
    RU_ORIGINAL = 'right_upper_original.jpg'
    RL_ORIGINAL = 'right_lower_original.jpg'
    LL_ORIGINAL = 'left_lower_original.jpg'
    LU_UNDISTORTED = 'left_upper_undistorted.jpg'
    RU_UNDISTORTED = 'right_upper_undistorted.jpg'
    RL_UNDISTORTED = 'right_lower_undistorted.jpg'
    LL_UNDISTORTED = 'left_lower_undistorted.jpg'
    LU_PROJECTED = 'left_upper_projected.jpg'
    RU_PROJECTED = 'right_upper_projected.jpg'
    RL_PROJECTED = 'right_lower_projected.jpg'
    LL_PROJECTED = 'left_lower_projected.jpg'
    RESULT = 'result.jpg'
    PARAMS = 'params.json'
    LOG = 'log.txt'

    @classmethod
    def image(cls, camera_position: CameraPosition, image_level: ImageLevel):
        return cls[f'{camera_position.value}_{image_level.value}.jpg']


DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), 'data')
PARAMS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', ScanFile.PARAMS.value)
SCANS_DIR_PATH = os.path.join(os.path.dirname(__file__), 'data', 'scans')


if not os.path.exists(DATA_DIR_PATH):
    os.mkdir(DATA_DIR_PATH)

if not os.path.exists(SCANS_DIR_PATH):
    os.mkdir(SCANS_DIR_PATH)


def path_for_scan_file(scan_id: str, file: ScanFile) -> str:
    return os.path.join(SCANS_DIR_PATH, scan_id, file.value)


def paths_for_image_level(scan_id: str, level: ImageLevel):
    return {level: path_for_scan_file(scan_id, ScanFile.image(position, level)) for position in CameraPosition}


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
