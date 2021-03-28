from shutil import rmtree
from server.src.app.logger import logger, log_timing
from server.src.camera import get_cameras
from server.src.processing import capture_photos, disorient_images, undistort, draw_polygons, project, compose
from server.src.app.paths import SCAN_IMAGES_PATH
from .grid import FullImage, Grid
from .uris import create_thumbs_folder, url_for, urls_for, path_for, paths_for


class Scan:
    def build(self):
        raise NotImplementedError

    @property
    def json_urls(self):
        raise NotImplementedError

    @staticmethod
    def get_class(scan_type: str):
        if scan_type == 'snapshot':
            return SnapshotScan
        elif scan_type == 'calibration':
            return CalibrationScan
        else:
            raise ValueError('Wrong `scan_type` value')

    def clear_folder(self):
        rmtree(SCAN_IMAGES_PATH)
        SCAN_IMAGES_PATH.mkdir()


class SnapshotScan(Scan):
    def __init__(self):
        self.original = Grid('original')
        self.undistorted = Grid('undistorted')
        self.projected = Grid('projected')
        self.result = FullImage('result')

    @log_timing
    def build(self):
        try:
            cameras = get_cameras()

            self.clear_folder()
            create_thumbs_folder()

            original_images_paths = paths_for(self.original, only='image')
            capture_photos(original_images_paths, cameras)
            disorient_images(original_images_paths)

            self.original.read_from(original_images_paths)
            original_thumb_paths = paths_for(self.original, only='thumb')
            self.original.persist_thumbnails_to(original_thumb_paths)

            undistorted_images = undistort(self.original.images, cameras)

            self.projected.images = project(undistorted_images, cameras)
            projected_paths = paths_for(self.projected)
            self.projected.persist_to(projected_paths)

            self.result.image = compose(self.projected.images)
            result_path = path_for(self.result)
            self.result.persist_to(result_path)

            self.undistorted.images = draw_polygons(undistorted_images, cameras)
            undistorted_paths = paths_for(self.undistorted)
            self.undistorted.persist_to(undistorted_paths)
        except Exception:
            logger.exception("Exception was raised inside SnapshotScan.build")
            raise

    @property
    def json_urls(self):
        return {
            'original': urls_for(self.original),
            'undistorted': urls_for(self.undistorted),
            'projected': urls_for(self.projected),
            'result': url_for(self.result)
        }


class CalibrationScan(Scan):
    def __init__(self):
        self.original = Grid('original')
        self.undistorted = Grid('undistorted')

    @log_timing
    def build(self):
        try:
            cameras = get_cameras()

            self.clear_folder()
            create_thumbs_folder()

            original_images_paths = paths_for(self.original, only='image')
            capture_photos(original_images_paths, cameras)
            disorient_images(original_images_paths)

            self.original.read_from(original_images_paths)
            original_thumb_paths = paths_for(self.original, only='thumb')
            self.original.persist_thumbnails_to(original_thumb_paths)

            self.undistorted.images = undistort(self.original.images, cameras)
            undistorted_paths = paths_for(self.undistorted)
            self.undistorted.persist_to(undistorted_paths)
        except Exception:
            logger.exception("Exception was raised inside CalibrationScan.build")
            raise

    @property
    def json_urls(self):
        return {
            'original': urls_for(self.original),
            'undistorted': urls_for(self.undistorted),
        }