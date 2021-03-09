import os.path
import shutil

import settings
from server.constants.enums import CameraPosition


class Camera:
    def __init__(self, usb: str, maker: str, model: str, projection_points=None):
        self.usb = usb
        self.maker = maker
        self.model = model
        self.projection_points = projection_points

    def capture_to_path(self, path):
        src_path = os.path.join(os.path.dirname(__file__), 'files', 'demo', os.path.basename(path))
        shutil.copy(src_path, path)

    def __repr__(self):
        return f'Camera({self.usb}, {self.maker}, {self.model})'


def _create_camera(data: dict):
    projection_points = {CameraPosition[key]: value for key, value in data['projection_points'].items()}
    return Camera(data['usb_port'], data['maker'], data['model'], projection_points=projection_points)


def _create_cameras():
    cameras_data = settings.get_settings()['cameras']
    return {CameraPosition[key]: _create_camera(data) for key, data in cameras_data.items()}


_cameras = _create_cameras()


def update_cameras():
    global _cameras
    _cameras = _create_cameras()


def get_cameras():
    return _cameras


# from pyexiv2 import Image
#
# def read_exif_data(paths: PathsType):
#     exif_data = {}
#
#     for position, file_path in paths.items():
#         with Image(file_path) as img:
#             data = img.read_exif()
#             exif_data[position] = {
#                 'focal_length': eval(data['Exif.Photo.FocalLength']),  # eval('3520/1000')
#                 'aperture': eval(data['Exif.Photo.FNumber'])  # eval('180/100')
#             }
#
#     return exif_data