import os
import shutil
from datetime import datetime
from enums import CameraPosition, ScanFile, ImageLevel, ScanType


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
    return {position: path_for_scan_file(scan_id, ScanFile.image(position, level)) for position in CameraPosition}


def path_for_params_file() -> str:
    return PARAMS_FILE_PATH


def scans_list():
    result = []

    for name in os.listdir(SCANS_DIR_PATH):
        scan_id, scan_type = name.split('_')

        if scan_type == ScanType.SNAPSHOT.value:
            result.append({
                'scanId': scan_id,
                'scanType': scan_type,
                'images': {level: paths_for_image_level(scan_id, level) for level in ImageLevel},
                'createdAt': datetime.fromtimestamp(int(name)).strftime('%d %B %Y, %H:%M'),
            })
        elif scan_type == ScanType.CALIBRATION.value:
            result.append({
                'scanId': scan_id,
                'scanType': scan_type,
                'images': {level: paths_for_image_level(scan_id, level) for level in [ImageLevel.ORIGINAL, ImageLevel.UNDISTORTED]},
                'createdAt': datetime.fromtimestamp(int(name)).strftime('%d %B %Y, %H:%M'),
            })

    return result


def create_scan_dir(scan_id: str, scan_type: ScanType):
    dir_name = f'{scan_id}_{scan_type.value}'
    path = os.path.join(SCANS_DIR_PATH, dir_name)
    return os.mkdir(path)


def copy_params_file(scan_id: str, scan_type: ScanType):
    path = os.path.join(SCANS_DIR_PATH, scan_id, ScanFile.PARAMS.value)
    shutil.copy(PARAMS_FILE_PATH, path)


def clear_scans_dir():
    shutil.rmtree(SCANS_DIR_PATH)
    os.mkdir(SCANS_DIR_PATH)
