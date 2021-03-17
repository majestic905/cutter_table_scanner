import numpy as np
import os
import cv2
from flask import url_for as flask_url_for
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

    def persist_to(self, path: dict):
        self.persist_image_to(path['image'])
        self.persist_thumbnail_to(path['thumb'])

    def persist_image_to(self, path: str):
        cv2.imwrite(path, self._image)

    def persist_thumbnail_to(self, path: str):
        cv2.imwrite(path, self._thumb)


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

        # filenames are not subject to change, images are, hence images comprehension sits inside property method
        self._filenames = {position: self._items[position].filename for position in CameraPosition}
        self._thumb_filenames = {position: self._items[position].thumb_filename for position in CameraPosition}

    @property
    def filenames(self):
        return self._filenames

    @property
    def thumb_filenames(self):
        return self._thumb_filenames

    @property
    def items(self):
        return self._items

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

    def persist_to(self, paths: dict):
        for position in CameraPosition:
            self._items[position].persist_to(paths[position])

    def persist_thumbnails_to(self, paths: PathsType):
        for position in CameraPosition:
            self._items[position].persist_thumbnail_to(paths[position])


class PathBuilder:
    def __init__(self, scan_id: str, root_directory: str):
        self._scan_id = scan_id
        self._scan_dir_path = root_directory

    def _uri_for(self, image: ThumbedImage, type: str, only: str = None):
        if type == 'url':
            image_uri = flask_url_for('get_scan_image', scan_id=self._scan_id, filename=image.filename)
            thumb_uri = flask_url_for('get_scan_image', scan_id=self._scan_id, filename=image.thumb_filename)
        elif type == 'path':
            image_uri = os.path.join(self._scan_dir_path, image.filename)
            thumb_uri = os.path.join(self._scan_dir_path, image.thumb_filename)
        else:
            raise ValueError('Possible values for `type` are "path" and "url"')

        if only is None:
            return {'image': image_uri, 'thumb': thumb_uri}
        elif only == 'image':
            return image_uri
        elif only == 'thumb':
            return thumb_uri
        else:
            raise ValueError('Possible values for `only` are "image", "thumb" or None')

    def path_for(self, image: ThumbedImage, only: str = None):
        return self._uri_for(image, 'path', only)

    def url_for(self, image: ThumbedImage, only: str = None):
        return self._uri_for(image, 'url', only)

    def paths_for(self, grid: Grid, only: str = None):
        return {position: self.path_for(grid.items[position], only) for position in CameraPosition}

    def urls_for(self, grid: Grid, only: str = None):
        return {position.name: self.url_for(grid.items[position], only) for position in CameraPosition}
