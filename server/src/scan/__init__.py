from shutil import rmtree
from server.src.app.logger import logger, log_timing, clear_log
from server.src.camera import get_cameras
from server.src.processing import capture_photos, disorient_images, interpolate, compose
from server.src.app.paths import SCAN_IMAGES_PATH
from .grid import FullImage, Grid
from .uris import url_for, urls_for, path_for, paths_for
from .info import write_scan_info


class Scan:
    def build(self):
        raise NotImplementedError

    @property
    def json_urls(self):
        raise NotImplementedError

    @staticmethod
    def get_class(scan_type: str):
        if scan_type == SnapshotScan.type:
            return SnapshotScan
        elif scan_type == CaptureScan.type:
            return CaptureScan
        else:
            raise ValueError('Wrong `scan_type` value')

    def do_chores(self):
        rmtree(SCAN_IMAGES_PATH)
        SCAN_IMAGES_PATH.mkdir()
        (SCAN_IMAGES_PATH / 'thumbs').mkdir()  # must be created beforehand for Grid
        write_scan_info(self.type)
        clear_log()


class SnapshotScan(Scan):
    type = "snapshot"

    def __init__(self):
        self.original = Grid('original')
        self.projected = Grid('projected')
        self.result = FullImage('result')

    @log_timing
    def build(self):
        try:
            cameras = get_cameras()

            self.do_chores()

            original_images_paths = paths_for(self.original, only='image')
            capture_photos(original_images_paths, cameras)
            disorient_images(original_images_paths)

            self.original.read_from(original_images_paths)
            original_thumb_paths = paths_for(self.original, only='thumb')
            self.original.persist_thumbnails_to(original_thumb_paths)

            self.projected.images = interpolate(self.original.images, cameras)
            projected_paths = paths_for(self.projected)
            self.projected.persist_to(projected_paths)

            self.result.image = compose(self.projected.images)
            result_path = path_for(self.result)
            self.result.persist_to(result_path)
        except Exception:
            logger.exception("Exception was raised inside SnapshotScan.build")
            raise

    @property
    def json_urls(self):
        return {
            'original': urls_for(self.original),
            'projected': urls_for(self.projected),
            'result': url_for(self.result)
        }


class CaptureScan(Scan):
    type = "capture"

    def __init__(self):
        self.original = Grid('original')

    @log_timing
    def build(self):
        try:
            cameras = get_cameras()

            self.do_chores()

            original_images_paths = paths_for(self.original, only='image')
            capture_photos(original_images_paths, cameras)
            disorient_images(original_images_paths)

            self.original.read_from(original_images_paths)
            original_thumb_paths = paths_for(self.original, only='thumb')
            self.original.persist_thumbnails_to(original_thumb_paths)
        except Exception:
            logger.exception("Exception was raised inside CaptureScan.build")
            raise

    @property
    def json_urls(self):
        return {
            'original': urls_for(self.original)
        }