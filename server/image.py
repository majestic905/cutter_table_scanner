import numpy as np
import os
import cv2
from camera_position import CameraPosition


def _create_thumbnail(image: np.ndarray, width: int):
    if image is None:
        return None

    if width is None:
        raise ValueError('`width` is None')

    (h, w) = image.shape[:2]
    ratio = width / float(w)
    height = int(h * ratio)

    return cv2.resize(image, (width, height))


class ThumbedImage:
    def __init__(self, name: str, position: CameraPosition = None, ndarray: np.ndarray = None, thumb_width: int = None):
        self.name = name
        self.position = position
        self.thumb_width = thumb_width

        self._thumbnail = None
        self._original = None

        if ndarray is not None:
            self.original = ndarray

    @property
    def filename(self):
        if self.position is None:
            return f'{self.name}.jpg'
        else:
            return f'{self.position.value}_{self.name}.jpg'

    @property
    def thumbnail_filename(self):
        return f'thumb_{self.filename}'

    @property
    def original(self):
        return self._original

    @original.setter
    def original(self, value: np.ndarray):
        self._original = value
        self._thumbnail = _create_thumbnail(self._original, self.thumb_width)

    def persist(self, path):
        cv2.imwrite(os.path.join(path, self.filename), self._original)
        cv2.imwrite(os.path.join(path, self.thumbnail_filename), self._thumbnail)