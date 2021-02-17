import numpy as np
import logging
from camera import Camera
from enums import CameraPosition
from custom_types import ImagesType


def undistort(image: np.ndarray, camera: Camera):
    # use camera methods, which use lensfunpy methods or opencv methods
    return image


def project(image: np.ndarray, camera: Camera):
    return image


def compose(images: ImagesType, logger: logging.Logger = None):
    left_upper = images[CameraPosition.LU]
    right_upper = images[CameraPosition.RU]
    right_lower = images[CameraPosition.RL]
    left_lower = images[CameraPosition.LL]

    # horizontally
    upper = np.concatenate((left_upper, right_upper), axis=1)
    lower = np.concatenate((left_lower, right_lower), axis=1)

    # vertically
    return np.concatenate((upper, lower), axis=0)