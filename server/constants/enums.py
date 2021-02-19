from __future__ import annotations
from enum import Enum


class CameraPosition(Enum):
    LU = 'left_upper'
    RU = 'right_upper'
    RL = 'right_lower'
    LL = 'left_lower'


class ImageLevel(Enum):
    ORIGINAL = 'original'
    UNDISTORTED = 'undistorted'
    PROJECTED = 'projected'


class ScanFile(Enum):
    LU_ORIGINAL = 'left_upper_original.jpg'
    RU_ORIGINAL = 'right_upper_original.jpg'
    RL_ORIGINAL = 'right_lower_original.jpg'
    LL_ORIGINAL = 'left_lower_original.jpg'
    LU_UNDISTORTED = 'left_upper_undistorted.jpg'
    RU_UNDISTORTED = 'right_upper_undistorted.jpg'
    RL_UNDISTORTED = 'right_lower_undistorted.jpg'
    LL_UNDISTORTED = 'left_lower_undistorted.jpg'
    LU_PROJECTED = 'left_upper_projected.jpg'
    RU_PROJECTED = 'right_upper_projected.jpg'
    RL_PROJECTED = 'right_lower_projected.jpg'
    LL_PROJECTED = 'left_lower_projected.jpg'
    RESULT = 'result.jpg'
    CAMERAS = 'cameras.json'
    LOG = 'log.txt'

    @classmethod
    def image(cls, camera_position: CameraPosition, image_level: ImageLevel):
        return cls[f'{camera_position.name}_{image_level.name}']


class ScanType(Enum):
    SNAPSHOT = 'snapshot'
    CALIBRATION = 'calibration'
