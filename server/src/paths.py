import os
import shutil
from pathlib import Path
from app import app


ROOT_PATH = Path(app.root_path)
STATIC_FOLDER = Path(app.static_folder)

SCAN_IMAGES_PATH = STATIC_FOLDER / 'scan'
SCAN_INFO_PATH = STATIC_FOLDER / 'scan.json'
SCAN_LOG_PATH = STATIC_FOLDER / 'scan.log'

CAMERAS_DATA_PATH = ROOT_PATH / 'cameras.json'
CAMERAS_SCHEMA_PATH = ROOT_PATH / 'cameras.schema.json'

DEFAULT_LENSFUN_XML_PATH = ROOT_PATH / 'lensfun.xml'
DUMMY_CAPTURES_PATH = ROOT_PATH.parent / 'eggs' / 'dummy_captures'


if not SCAN_IMAGES_PATH.exists():
    SCAN_IMAGES_PATH.mkdir()