import os
import lensfunpy
from xml.etree.ElementTree import XML, ParseError
from shutil import copy
from pathlib import Path
from server.src.app.paths import DEFAULT_LENSFUN_XML_PATH
from server.src.camera import Camera


LENSFUN_XML_FILE_NAME = 'cutter_table_scanner.xml'


def _get_lensfun_dir():
    if os.name == "nt":
        return Path.home() / 'AppData' / 'Local' / 'lensfun'
    else:
        return Path.home() / '.local' / 'share' / 'lensfun'


def _get_lensfun_file():
    return _get_lensfun_dir() / LENSFUN_XML_FILE_NAME


def _copy_lensfun_xml():
    lensfun_dir = _get_lensfun_dir()
    lensfun_file = _get_lensfun_file()

    if not lensfun_dir.exists():
        lensfun_dir.mkdir()

    if not lensfun_file.exists():
        copy(DEFAULT_LENSFUN_XML_PATH, lensfun_file)


def validate_xml(text: str):
    try:
        XML(text)
    except ParseError as error:
        return str(error)


def read_lensfun_xml():
    return _get_lensfun_file().read_text()


def save_lensfun_xml(text: str):
    _get_lensfun_file().write_text(text)


def get_undist_coords(camera: Camera, image_size: tuple):
    width, height = image_size
    key = (camera.maker, camera.model, width, height)

    if key not in _undist_coords_repo:
        db = lensfunpy.Database()
        lf_cam = db.find_cameras(camera.maker, camera.model)[0]
        lf_lens = db.find_lenses(lf_cam)[0]

        mod = lensfunpy.Modifier(lf_lens, lf_cam.crop_factor, width, height)
        mod.initialize(lf_lens.min_focal, 0, 0)  # aperture and focus distance are not used for distortion

        _undist_coords_repo[key] = mod.apply_geometry_distortion()

    return _undist_coords_repo[key]


_copy_lensfun_xml()
_undist_coords_repo = {}
