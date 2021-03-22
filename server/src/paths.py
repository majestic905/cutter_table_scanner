import os
import shutil
from pathlib import Path
from app import app


ROOT_PATH = Path(app.root_path)
SCANS_DIR_PATH = Path(app.static_folder) / 'scans'

FAKE_CAPTURES_DIR_PATH = ROOT_PATH / 'misc' / 'fake_captures'

SETTINGS_FILE_PATH = ROOT_PATH / 'settings.json'
SETTINGS_SCHEMA_PATH = ROOT_PATH / 'settings.schema.json'

_DEFAULT_SETTINGS_FILE_PATH = ROOT_PATH / 'misc' / '_settings.json'
_DEFAULT_CAMERAS_XML_PATH = ROOT_PATH / 'misc' / '_cameras.xml'


def _get_lensfun_dir_path():
    if os.name == "nt":
        return Path.home() / 'AppData' / 'Local' / 'lensfun'
    else:
        return Path.home() / '.local' / 'share' / 'lensfun'


# create server/static
def _create_static_folder():
    static_folder = Path(app.static_folder)
    if not static_folder.exists():
        static_folder.mkdir()


# create server/static/data/scans
def _create_scans_folder():
    if not SCANS_DIR_PATH.exists():
        SCANS_DIR_PATH.mkdir()


# copy server/files/_settings.json to server/static/data/settings.json
def _copy_settings_to_static_data():
    if not SETTINGS_FILE_PATH.exists():
        shutil.copy(_DEFAULT_SETTINGS_FILE_PATH, SETTINGS_FILE_PATH)


# copy server/files/_cameras.xml to ~/AppData/Local/lensfun/cameras.xml or ~/.local/share/lensfun/cameras.xml
def _copy_lensfun_xml_to_system_user():
    lf_dir_path = _get_lensfun_dir_path()

    if not lf_dir_path.exists():
        lf_dir_path.mkdir()

    cameras_file = lf_dir_path / 'cutter_table_scanner.xml'
    exists = cameras_file.exists()
    local_is_newer = exists and _DEFAULT_CAMERAS_XML_PATH.stat().st_mtime > cameras_file.stat().st_ctime

    if not exists or local_is_newer:
        shutil.copy(_DEFAULT_CAMERAS_XML_PATH, cameras_file)


# _create_static_folder()
_create_scans_folder()
_copy_settings_to_static_data()
_copy_lensfun_xml_to_system_user()