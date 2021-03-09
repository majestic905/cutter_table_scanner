import os
import shutil
from server.app import app
from server.constants.enums import ScanFile, CameraPosition

DATA_DIR_PATH = os.path.join(app.static_folder, 'data')
SETTINGS_FILE_PATH = os.path.join(DATA_DIR_PATH, ScanFile.SETTINGS.value)
SETTINGS_SCHEMA_PATH = os.path.join(app.root_path, 'files', 'settings.schema.json')
SCANS_DIR_PATH = os.path.join(DATA_DIR_PATH, 'scans')

_DEFAULT_SETTINGS_FILE_PATH = os.path.join(app.root_path, 'files', '_settings.json')
_DEFAULT_CAMERAS_XML_PATH = os.path.join(app.root_path, 'files', '_cameras.xml')
_WINDOWS_LF_DIR_PATH = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'lensfun')
_LINUX_LF_DIR_PATH = os.path.join(os.path.expanduser('~'), '.local', 'share', 'lensfun')


# create server/static
def _create_static_folder():
    if not os.path.exists(app.static_folder):
        os.mkdir(app.static_folder)


# create server/static/data
def _create_static_data_folder():
    if not os.path.exists(DATA_DIR_PATH):
        os.mkdir(DATA_DIR_PATH)


# create server/static/data/scans
def _create_static_data_scans_folder():
    if not os.path.exists(SCANS_DIR_PATH):
        os.mkdir(SCANS_DIR_PATH)


# copy server/files/_settings.json to server/static/data/settings.json
def _copy_settings_to_static_data():
    if not os.path.exists(SETTINGS_FILE_PATH):
        shutil.copy(_DEFAULT_SETTINGS_FILE_PATH, SETTINGS_FILE_PATH)


# copy server/files/_cameras.xml to ~/AppData/Local/lensfun/cameras.xml or ~/.local/share/lensfun/cameras.xml
def _copy_lensfun_xml_to_system_user():
    lf_dir_path = _WINDOWS_LF_DIR_PATH if os.name == "nt" else _LINUX_LF_DIR_PATH

    if not os.path.exists(lf_dir_path):
        os.mkdir(lf_dir_path)

    cameras_file = os.path.join(lf_dir_path, 'cutter_table_scanner.xml')

    if not os.path.exists(cameras_file):
        shutil.copy(_DEFAULT_CAMERAS_XML_PATH, cameras_file)


_create_static_folder()
_create_static_data_folder()
_create_static_data_scans_folder()
_copy_settings_to_static_data()
_copy_lensfun_xml_to_system_user()