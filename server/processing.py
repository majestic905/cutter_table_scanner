import numpy as np
from camera import CameraPosition


def undistort(original_cv2_image, camera):
    # use camera methods, which use lensfunpy methods or opencv methods
    return original_cv2_image


def project(undistorted_cv2_image, camera):
    return undistorted_cv2_image


def compose(projected_cv2_images):
    lu = projected_cv2_images[CameraPosition.LU]
    ru = projected_cv2_images[CameraPosition.RU]
    rl = projected_cv2_images[CameraPosition.RL]
    ll = projected_cv2_images[CameraPosition.LL]

    # horizontally
    upper = np.concatenate((lu, ru), axis=1)
    lower = np.concatenate((ll, rl), axis=1)

    # vertically
    return np.concatenate((upper, lower), axis=0)