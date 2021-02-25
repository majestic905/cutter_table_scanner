import os.path
import shutil
import lensfunpy


class Camera:
    def __init__(self, usb: str, maker: str, model: str, projection_points=None):
        self.usb = usb
        self.maker = maker
        self.model = model
        self.projection_points = projection_points

        lf_db = lensfunpy.Database()
        try:
            self.lf_cam = lf_db.find_cameras(maker, model)[0]
            self.lf_lens = lf_db.find_lenses(self.lf_cam)[0]
        except IndexError:
            self.lf_cam = None
            self.lf_lens = None

    @property
    def present_in_lensfun(self):
        return bool(self.lf_cam) and bool(self.lf_lens)

    def capture_to_path(self, path):
        src_path = os.path.join(__file__, '..', 'eggs', 'sample_scan', os.path.basename(path))
        shutil.copy(src_path, path)

    def __repr__(self):
        return f'Camera({self.usb}, {self.maker}, {self.model})'