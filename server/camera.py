import lensfunpy
import shutil
import os
from enum import Enum
from typing import Dict


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
        src_path = os.path.join(os.path.dirname(__file__), 'files', 'demo', os.path.basename(path))
        shutil.copy(src_path, path)

    def __repr__(self):
        return f'Camera({self.usb_port}, {self.maker}, {self.model})'


CamerasType = Dict[CameraPosition, Camera]