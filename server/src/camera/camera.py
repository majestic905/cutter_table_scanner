import gphoto2 as gp
import cv2
from datetime import datetime
from pathlib import Path
from server.src.app.paths import DUMMY_CAPTURES_PATH
from .position import CameraPosition


class Camera:
    def __init__(self, camera_data: dict):
        self.mapping = camera_data['mapping']

    def capture_to_path(self, path: Path):
        raise NotImplementedError


class RealCamera(Camera):
    """capture_to_path tells the real camera to capture image and the downloads it"""

    def __init__(self, camera_data: dict, gp_camera: gp.Camera):
        super().__init__(camera_data)
        self.serial_number = camera_data['serial_number']
        self._gp_camera = gp_camera

    def capture_to_path(self, dst_path: Path):
        camera, serial_number = self._gp_camera, self.serial_number

        file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
        camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        camera_file.save(str(dst_path))
        camera.file_delete(file_path.folder, file_path.name)


class DummyCamera(Camera):
    """capture_to_path copies image from predefined position (from DUMMY_CAPTURES_DIR_PATH directory)"""

    def __init__(self, camera_data: dict, position: CameraPosition):
        super().__init__(camera_data)
        self._position = position

    def capture_to_path(self, dst_path: Path):
        src_path = DUMMY_CAPTURES_PATH / f'{self._position.value}.jpg'
        image = cv2.imread(str(src_path))

        bottom_left = (600, 2435)
        text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cv2.putText(image, text, bottom_left, cv2.FONT_HERSHEY_DUPLEX, 10, (0, 0, 255), 15, cv2.LINE_AA)

        cv2.imwrite(str(dst_path), image)
