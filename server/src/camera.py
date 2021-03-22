import shutil
import cv2
import numpy as np
import lensfunpy
import gphoto2 as gp
from pathlib import Path
from enum import Enum
from timeit import default_timer as timer
from app_logger import logger
from paths import DUMMY_CAPTURES_DIR_PATH


class CameraPosition(Enum):
    LU = 'left_upper'
    RU = 'right_upper'
    RL = 'right_lower'
    LL = 'left_lower'


class Camera:
    def __init__(self, data: dict):
        self.type = data['type']
        self.projectied_image_size = data['projectied_image_size']
        self.projection_points = data['projection_points']

    def capture_to_path(self, path: Path):
        raise NotImplementedError


class BlankCamera(Camera):
    """capture_to_path saves blank image with dimensions specified in constructor"""

    def __init__(self, camera_data: dict, width: int, height: int):
        super().__init__(camera_data)
        self._width = width
        self._height = height

    def capture_to_path(self, dst_path: Path):
        shape = (self._height, self._width, 3)
        image = np.zeros(shape, np.uint8)
        cv2.imwrite(str(dst_path), image)

    def __repr__(self):
        args = {'width': self._width, 'height': self._height}
        return f'BlankCamera({args})'


class RealCamera(Camera):
    """capture_to_path tells the real camera to capture image and the downloads it"""

    def __init__(self, camera_data: dict, gp_camera: gp.Camera):
        super().__init__(camera_data)

        self._serial_number = camera_data['serial_number']
        self._maker = camera_data['maker']
        self._model = camera_data['model']

        self._gp_camera = gp_camera

        db = lensfunpy.Database()
        self.lf_cam = db.find_cameras(self._maker, self._model)[0]
        self.lf_lens = db.find_lenses(self.lf_cam)[0]

    def capture_to_path(self, dst_path: Path):
        camera, serial_number = self._gp_camera, self._serial_number

        start = timer()
        logger.debug(f'[capture_to_path] {serial_number} capture start')
        file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
        logger.debug(f'[capture_to_path] {serial_number} capture end: {file_path.folder}/{file_path.name}')

        logger.debug(f'[capture_to_path] {serial_number} file_get start')
        camera_file: gp.CameraFile = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        logger.debug(f'[capture_to_path] {serial_number} file_get end')

        logger.debug(f'[capture_to_path] {serial_number} save start')
        camera_file.save(str(dst_path))
        logger.debug(f'[capture_to_path] {serial_number} save end')

        logger.debug(f'[capture_to_path] {serial_number} delete start: {file_path.folder}/{file_path.name}')
        camera.file_delete(file_path.folder, file_path.name)
        logger.debug(f'[capture_to_path] {serial_number} delete end')

        end = timer()
        logger.debug(f'[capture_to_path] {serial_number} capture_to_path took {round(end - start, 2)} seconds')

    def __repr__(self):
        args = {'maker': self._maker, 'model': self._model, 'serial_number': self._serial_number}
        return f'RealCamera({args})'


class DummyCamera(RealCamera):
    """capture_to_path copies image from predefined position (from DUMMY_CAPTURES_DIR_PATH directory)"""

    def __init__(self, camera_data: dict, position: CameraPosition):
        super().__init__(camera_data, None)
        self._position = position

    def capture_to_path(self, dst_path: Path):
        src_path = DUMMY_CAPTURES_DIR_PATH / f'{self._position.value}.jpg'
        shutil.copy(src_path, dst_path)

    def __repr__(self):
        return f'DummyCamera({self._position})'
