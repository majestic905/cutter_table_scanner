import cv2
import storage
import shutil
import json
from __future__ import annotations
from enum import Enum
from datetime import datetime
from camera import CameraPosition, Camera
from typing import Dict, Callable


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

    def path_for(self, scan_id):
        return storage.path_for_scan_file(scan_id, self)


class Scan:
    def __init__(self, scan_id: str = None):
        if scan_id is None:
            scan_id = str(datetime.now().timestamp())
            storage.create_scan_dir(scan_id)
            storage.copy_params_file(scan_id)

        self.scan_id = scan_id
        self._params = None
        self._log = None

    def _path_for(self, file: ScanFile):
        return storage.path_for_scan_file(self.scan_id, file)

    def capture_photos(self, cameras: Dict[CameraPosition, Camera]):
        for position, camera in cameras.items():
            path = ScanFile.image(position, ImageLevel.ORIGINAL).path_for(self.scan_id)
            camera.capture_to_path(path)

    def build_undistorted_images(self, undistort_fn: Callable, cameras: Dict[CameraPosition, Camera]):
        for position in CameraPosition:
            path = ScanFile.image(position, ImageLevel.ORIGINAL).path_for(self.scan_id)
            cv2_image = cv2.imread(path)

            path = ScanFile.image(position, ImageLevel.UNDISTORTED).path_for(self.scan_id)
            cv2_image = undistort_fn(cv2_image, cameras[position])
            cv2.imwrite(path, cv2_image)

    def build_projected_images(self, project_fn: Callable, cameras: Dict[CameraPosition, Camera]):
        for position in CameraPosition:
            path = ScanFile.image(position, ImageLevel.UNDISTORTED).path_for(self.scan_id)
            cv2_image = cv2.imread(path)

            path = ScanFile.image(position, ImageLevel.PROJECTED).path_for(self.scan_id)
            cv2_image = project_fn(cv2_image, cameras[position])
            cv2.imwrite(path, cv2_image)

    def build_result_image(self, compose_fn):
        images = {
            position: cv2.imread(
                ScanFile.image(position, ImageLevel.PROJECTED).path_for(self.scan_id)
            ) for position in CameraPosition
        }

        path = ScanFile.RESULT.path_for(self.scan_id)
        cv2_image = compose_fn(images)
        cv2.imwrite(path, cv2_image)

    @property
    def params(self):
        if self._params:
            return self._params

        path = ScanFile.PARAMS.path_for(self.scan_id)
        with open(path) as json_file:
            self._params = json.load(json_file)

    @property
    def log(self):
        if self._log:
            return self._log

        path = ScanFile.LOG.path_for(self.scan_id)
        with open(path) as file:
            self._log = file.read()
