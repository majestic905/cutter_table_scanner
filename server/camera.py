import os.path
import shutil
import lensfunpy


class Camera:
    def __init__(self, usb: str, manufacturer: str, model: str, calibration_data=None, projection_points=None):
        self.usb = usb
        self.manufacturer = manufacturer
        self.model = model
        self.calibration_data = calibration_data
        self.projection_points = projection_points

        # search in lensfunpy
        # check for opencv params presence
        # initialize in gphoto2?

    def present_in_lensfun(self):
        db = lensfunpy.Database()
        cameras = db.find_cameras(self.manufacturer, self.model)
        return len(cameras) > 0

    def capture_to_path(self, path):
        src_path = os.path.join(__file__, '..', 'eggs', 'sample_scan', os.path.basename(path))
        shutil.copy(src_path, path)

    def __repr__(self):
        return f'Camera({self.usb}, {self.manufacturer}, {self.model})'