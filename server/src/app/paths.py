from pathlib import Path
from . import app


ROOT_PATH = Path(app.root_path)
STATIC_FOLDER = Path(app.static_folder)

BUSY_FILE_PATH = ROOT_PATH / '.busy'

SCAN_IMAGES_PATH = STATIC_FOLDER / 'scan'
SCAN_INFO_PATH = STATIC_FOLDER / 'scan.json'
SCAN_LOG_PATH = STATIC_FOLDER / 'scan.log'

CAMERAS_DATA_PATH = ROOT_PATH / 'cameras.json'
CAMERAS_SCHEMA_PATH = ROOT_PATH / 'cameras.schema.json'
CAMERAS_MAPPINGS_PATH = ROOT_PATH / 'cameras.mappings.npz'

DUMMY_CAPTURES_PATH = ROOT_PATH.parent / 'eggs' / 'dummy_captures'

if not SCAN_IMAGES_PATH.exists():
    SCAN_IMAGES_PATH.mkdir()
