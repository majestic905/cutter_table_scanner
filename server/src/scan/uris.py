from flask import url_for as flask_url_for
from server.src.app.paths import SCAN_IMAGES_PATH
from server.src.camera import CameraPosition
from typing import Dict
from .grid import ThumbedImage, Grid, PathOrPaths, StrOrStrs


def _uri_for(image: ThumbedImage, type: str, only: str = None):
    if type == 'url':
        image_uri = flask_url_for('static', filename=f'scan/{image.filename}')
        thumb_uri = flask_url_for('static', filename=f'scan/thumbs/{image.thumb_filename}')
    elif type == 'path':
        image_uri = SCAN_IMAGES_PATH / image.filename
        thumb_uri = SCAN_IMAGES_PATH / 'thumbs' / image.thumb_filename
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


def path_for(image: ThumbedImage, only: str = None) -> PathOrPaths:
    return _uri_for(image, 'path', only)


def url_for(image: ThumbedImage, only: str = None) -> StrOrStrs:
    return _uri_for(image, 'url', only)


def paths_for(grid: Grid, only: str = None) -> Dict[CameraPosition, PathOrPaths]:
    return {position: path_for(grid.items[position], only) for position in CameraPosition}


def urls_for(grid: Grid, only: str = None) -> Dict[CameraPosition, StrOrStrs]:
    return {position.name: url_for(grid.items[position], only) for position in CameraPosition}

