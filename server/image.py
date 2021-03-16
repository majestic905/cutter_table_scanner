import numpy as np
import os
import cv2
from processing import ImagesType, PathsType, create_thumbnail
from camera_position import CameraPosition


class ThumbedImage:
    def __init__(self, thumb_width: int = None):
        self._thumb_width = thumb_width
        self._image = None
        self._thumb = None

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value: np.ndarray):
        self._image = value
        self._thumb = create_thumbnail(self._image, self._thumb_width)

    #######

    @property
    def filename(self):
        raise NotImplementedError

    @property
    def thumb_filename(self):
        raise NotImplementedError

    def read_from(self, path: str):
        self.image = cv2.imread(path)

    def persist_to(self, dir_path: str):
        self.persist_image_to(dir_path)
        self.persist_thumbnail_to(dir_path)

    def persist_image_to(self, dir_path: str):
        file_path = os.path.join(dir_path, self.filename)
        cv2.imwrite(file_path, self._image)

    def persist_thumbnail_to(self, dir_path: str):
        file_path = os.path.join(dir_path, self.thumb_filename)
        cv2.imwrite(file_path, self._thumb)


class FullImage(ThumbedImage):
    def __init__(self, name: str):
        super().__init__(500)
        self._name = name

    @property
    def filename(self):
        return f'{self._name}.jpg'

    @property
    def thumb_filename(self):
        return f'thumb_{self._name}.jpg'


class GridItem(ThumbedImage):
    def __init__(self, name: str, position: CameraPosition):
        super().__init__(250)
        self._name = name
        self._position = position

    @property
    def filename(self):
        return f'{self._position.value}_{self._name}.jpg'

    @property
    def thumb_filename(self):
        return f'thumb_{self._position.value}_{self._name}.jpg'


class Grid:
    def __init__(self, name: str):
        self._items = {position: GridItem(name, position) for position in CameraPosition}

        # filenames are not subject to change, images are, hence images comprehension sits inside method
        self._filenames = {position: self._items[position].filename for position in CameraPosition}
        self._thumb_filenames = {position: self._items[position].thumb_filename for position in CameraPosition}

    @property
    def filenames(self):
        return self._filenames

    @property
    def thumb_filenames(self):
        return self._thumb_filenames

    @property
    def images(self):
        return {position: self._items[position].image for position in CameraPosition}

    @images.setter
    def images(self, images: ImagesType):
        for position in CameraPosition:
            self._items[position].image = images[position]

    def read_from(self, paths: PathsType):
        for position in CameraPosition:
            self._items[position].read_from(paths[position])

    def persist_to(self, dir_path: str):
        for position in CameraPosition:
            self._items[position].persist_to(dir_path)

    def persist_thumbnails_to(self, dir_path: str):
        for position in CameraPosition:
            self._items[position].persist_thumbnail_to(dir_path)
