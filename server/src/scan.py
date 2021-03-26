from app_logger import logger
from cameras import get_cameras
from processing import capture_photos, disorient_images, undistort, draw_polygons, project, compose
from image import FullImage, Grid, PathBuilder
from paths import SCAN_PATH


class Scan:
    def build(self):
        raise NotImplementedError

    @property
    def json_urls(self):
        raise NotImplementedError

    @property
    def log_path(self):
        return SCAN_PATH / 'log.txt'

    @staticmethod
    def get_class(scan_type: str):
        if scan_type == 'snapshot':
            return SnapshotScan
        elif scan_type == 'calibration':
            return CalibrationScan
        else:
            raise ValueError('Wrong `scan_type` value')


class SnapshotScan(Scan):
    def __init__(self):
        self.original = Grid('original')
        self.undistorted = Grid('undistorted')
        self.projected = Grid('projected')
        self.result = FullImage('result')

        self.path_builder = PathBuilder(SCAN_PATH)

    def build(self):
        try:
            cameras = get_cameras()

            original_images_paths = self.path_builder.paths_for(self.original, only='image')
            logger.info('Capturing photos...')
            capture_photos(original_images_paths, cameras)

            logger.info('Setting Exif.Image.Orientation=1 to disable undesired auto-rotation...')
            disorient_images(original_images_paths)

            logger.info('Reading captured photos...')
            self.original.read_from(original_images_paths)

            original_thumb_paths = self.path_builder.paths_for(self.original, only='thumb')
            logger.info('Writing original photos thumbnails...')
            self.original.persist_thumbnails_to(original_thumb_paths)

            logger.info('Undistorting original images...')
            undistorted_images = undistort(self.original.images, cameras)

            logger.info('Projecting undistorted images...')
            self.projected.images = project(undistorted_images, cameras)

            projected_paths = self.path_builder.paths_for(self.projected)
            logger.info('Writing projected images with thumbnails...')
            self.projected.persist_to(projected_paths)

            logger.info('Composing result image...')
            self.result.image = compose(self.projected.images)

            result_path = self.path_builder.path_for(self.result)
            logger.info('Writing result image with thumbnail...')
            self.result.persist_to(result_path)

            logger.info('Drawing polygons on undistorted images...')
            self.undistorted.images = draw_polygons(undistorted_images, cameras)

            undistorted_paths = self.path_builder.paths_for(self.undistorted)
            logger.info('Writing undistorted images with thumbnails...')
            self.undistorted.persist_to(undistorted_paths)
        except Exception:
            logger.exception(f'Unexpected error occurred...')
            raise

    @property
    def json_urls(self):
        return {
            'original': self.path_builder.urls_for(self.original),
            'undistorted': self.path_builder.urls_for(self.undistorted),
            'projected': self.path_builder.urls_for(self.projected),
            'result': self.path_builder.url_for(self.result)
        }


class CalibrationScan(Scan):
    def __init__(self):
        self.original = Grid('original')
        self.undistorted = Grid('undistorted')

        self.path_builder = PathBuilder(SCAN_PATH)

    def build(self):
        try:
            cameras = get_cameras()

            original_images_paths = self.path_builder.paths_for(self.original, only='image')
            logger.info('Capturing photos...')
            capture_photos(original_images_paths, cameras)

            logger.info('Setting Exif.Image.Orientation=1 to disable undesired auto-rotation...')
            disorient_images(original_images_paths)

            logger.info('Reading photos...')
            self.original.read_from(original_images_paths)

            original_thumb_paths = self.path_builder.paths_for(self.original, only='thumb')
            logger.info('Writing original photos thumbnails...')
            self.original.persist_thumbnails_to(original_thumb_paths)

            logger.info('Undistorting original images...')
            self.undistorted.images = undistort(self.original.images, cameras)

            undistorted_paths = self.path_builder.paths_for(self.undistorted)
            logger.info('Writing undistorted images with thumbnails...')
            self.undistorted.persist_to(undistorted_paths)
        except Exception as error:
            logger.exception(f'Unexpected error occurred...')
            raise

    @property
    def json_urls(self):
        return {
            'original': self.path_builder.urls_for(self.original),
            'undistorted': self.path_builder.urls_for(self.undistorted),
        }