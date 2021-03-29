import shutil
import lensfunpy
import gphoto2 as gp
from pathlib import Path
from server.src.app.logger import log_timing
from server.src.app.paths import DUMMY_CAPTURES_PATH
from .position import CameraPosition



class Camera:
    def __init__(self, data: dict):
        self.projected_image_size = data['projected_image_size']
        self.projection_points = data['projection_points']

        self.serial_number = data.get('serial_number')
        self.maker = data['maker']
        self.model = data['model']

        db = lensfunpy.Database()
        self.lf_cam = db.find_cameras(self.maker, self.model)[0]
        self.lf_lens = db.find_lenses(self.lf_cam)[0]

    def capture_to_path(self, path: Path):
        raise NotImplementedError


class RealCamera(Camera):
    """capture_to_path tells the real camera to capture image and the downloads it"""

    def __init__(self, camera_data: dict, gp_camera: gp.Camera):
        super().__init__(camera_data)
        self._gp_camera = gp_camera

    @log_timing
    def capture_to_path(self, dst_path: Path):
        camera, serial_number = self._gp_camera, self.serial_number

        file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
        camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        camera_file.save(str(dst_path))
        camera.file_delete(file_path.folder, file_path.name)

    def __repr__(self):
        args = {'maker': self.maker, 'model': self.model, 'serial_number': self.serial_number}
        return f'RealCamera({args})'


class DummyCamera(Camera):
    """capture_to_path copies image from predefined position (from DUMMY_CAPTURES_DIR_PATH directory)"""

    def __init__(self, camera_data: dict, position: CameraPosition):
        super().__init__(camera_data)
        self._position = position

    def capture_to_path(self, dst_path: Path):
        src_path = DUMMY_CAPTURES_PATH / f'{self._position.value}.jpg'
        shutil.copy(src_path, dst_path)

    def __repr__(self):
        return f'DummyCamera({self._position})'
