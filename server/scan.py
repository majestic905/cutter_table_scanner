import os.path
import logging
import shutil
from datetime import datetime
from typing import Optional

from enums import ScanType, ScanFile, ImageLevel, CameraPosition


DEFAULT_LOGGER = logging.getLogger(__name__)

DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), 'data')
PARAMS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', ScanFile.PARAMS.value)
SCANS_DIR_PATH = os.path.join(os.path.dirname(__file__), 'data', 'scans')

if not os.path.exists(DATA_DIR_PATH):
    os.mkdir(DATA_DIR_PATH)

if not os.path.exists(SCANS_DIR_PATH):
    os.mkdir(SCANS_DIR_PATH)


class Scan:
    def __init__(self, scan_id: Optional[str], scan_type: ScanType, logger: logging.Logger = None, **kwargs):
        self.id = scan_id or str(datetime.now().timestamp())
        self.type = scan_type

        self.logger = logger or DEFAULT_LOGGER
        self.logger_handler = None

        self.paths = {level: self.paths_for_image_level(level) for level in ImageLevel}
        self.images = {level: dict.fromkeys(list(CameraPosition)) for level in ImageLevel}

    @staticmethod
    def new(scan_type: ScanType):
        scan = Scan(None, scan_type)
        os.mkdir(scan.directory)
        shutil.copy(PARAMS_FILE_PATH, scan.path_for(ScanFile.PARAMS))
        return scan

    @staticmethod
    def find(scan_id: str):
        dir_name = next((name for name in os.listdir() if name.startswith(scan_id)), None)

        if dir_name is not None:
            scan_id, scan_type = dir_name.split('_')
            scan_type = ScanType[scan_type]
            return Scan(scan_id, scan_type)

    def log(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def setup_logger(self):
        log_file_path = self.path_for(ScanFile.LOG)
        self.logger_handler = logging.FileHandler(log_file_path)
        self.logger.addHandler(self.logger_handler)

    def cleanup_logger(self):
        self.logger.removeHandler(self.logger_handler)
        self.logger_handler = None

    @property
    def directory(self):
        return os.path.join(SCANS_DIR_PATH, f'{self.id}_{self.type.value}')

    def path_for(self, scan_file: ScanFile):
        return os.path.join(self.directory, scan_file.value)

    def paths_for_image_level(self, level: ImageLevel):
        return {position: self.path_for(ScanFile.image(position, level)) for position in CameraPosition}

    @staticmethod
    def list_all():
        result = []

        for name in os.listdir(SCANS_DIR_PATH):
            scan_id, scan_type = name.split('_')
            scan_type = ScanType[scan_type]

            item = {
                'scanId': scan_id,
                'scanType': scan_type,
                'createdAt': datetime.fromtimestamp(int(name)).strftime('%d %B %Y, %H:%M'),
            }

            if scan_type == ScanType.SNAPSHOT:
                item['images'] = {level: Scan.paths_for_image_level(scan_id, level) for level in ImageLevel}
            elif scan_type == ScanType.CALIBRATION:
                item['images'] = {level: Scan.paths_for_image_level(scan_id, level) for level in
                                  [ImageLevel.ORIGINAL, ImageLevel.UNDISTORTED]}

            result.append(item)

        return result

    @staticmethod
    def delete_all():
        shutil.rmtree(SCANS_DIR_PATH)
        os.mkdir(SCANS_DIR_PATH)
