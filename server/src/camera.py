import lensfunpy
import shutil
import os
import gphoto2 as gp
from pathlib import Path
from enum import Enum
from typing import Dict
from paths import FAKE_CAPTURES_DIR_PATH


class CameraPosition(Enum):
    LU = 'left_upper'
    RU = 'right_upper'
    RL = 'right_lower'
    LL = 'left_lower'


class Camera:
    def __init__(self, data: dict):
        self.usb_port = data['usb_port']
        self.maker = data['maker']
        self.model = data['model']
        self.projection_image_size = data['projection_image_size']
        self.projection_points = data['projection_points']
        self.get_lensfun_handlers()

    def get_lensfun_handlers(self):
        db = lensfunpy.Database()
        self.lf_cam = db.find_cameras(self.maker, self.model)[0]
        self.lf_lens = db.find_lenses(self.lf_cam)[0]

    def capture_to_path(self, path):
        src_path = FAKE_CAPTURES_DIR_PATH / os.path.basename(path)
        shutil.copy(src_path, path)

    def __repr__(self):
        return f'Camera({self.usb_port}, {self.maker}, {self.model})'


# class RealCamera(Camera):
#     def __init__(self, serial_number: str, gp_obj: gp.Camera, camera_data: dict):
#         super().__init__(camera_data)
#         self._serial_number = serial_number
#         self._gp_obj = gp_obj
#
#     def capture_to_path(self, dst_path: Path):
#         self.gp_obj.capture(gp.GP_CAPTURE_IMAGE)


class FakeCamera(Camera):
    def __init__(self, capture_file_path: Path, camera_data: dict):
        super().__init__(camera_data)
        self._capture_file_path = capture_file_path

    def capture_to_path(self, dst_path: Path):
        shutil.copy(self._capture_file_path, dst_path)


CamerasType = Dict[CameraPosition, Camera]