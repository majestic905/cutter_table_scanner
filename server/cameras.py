import os.path
import shutil
import lensfunpy
from settings import get_settings
from camera_position import CameraPosition


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


def _create_cameras():
    cameras_data = get_settings()['cameras']
    print('in _create_cameras')
    print(cameras_data)
    return {CameraPosition[key]: Camera(data) for key, data in cameras_data.items()}


_cameras = _create_cameras()


def update_cameras():
    global _cameras
    print('in update_cameras')
    _cameras = _create_cameras()


def get_cameras():
    print('in get_camerasss')
    print(_cameras[CameraPosition.LL].projection_points)
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