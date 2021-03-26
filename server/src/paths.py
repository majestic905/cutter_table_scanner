import os
import shutil
from pathlib import Path
from app import app


ROOT_PATH = Path(app.root_path)
STATIC_FOLDER = Path(app.static_folder)
SCAN_PATH = STATIC_FOLDER / 'scan'
SCAN_INFO_PATH = STATIC_FOLDER / 'scan.json'

DUMMY_CAPTURES_DIR_PATH = ROOT_PATH / 'misc' / 'dummy_captures'

SETTINGS_FILE_PATH = ROOT_PATH / 'settings.json'
SETTINGS_SCHEMA_PATH = ROOT_PATH / 'settings.schema.json'


def _mkdir_scan_path():
    if not SCAN_PATH.exists():
        SCAN_PATH.mkdir()


# copy server/files/_cameras.xml to ~/AppData/Local/lensfun/cameras.xml or ~/.local/share/lensfun/cameras.xml
def _copy_lensfun_xml():
    if os.name == "nt":
        lf_dir_path = Path.home() / 'AppData' / 'Local' / 'lensfun'
    else:
        lf_dir_path = Path.home() / '.local' / 'share' / 'lensfun'

    if not lf_dir_path.exists():
        lf_dir_path.mkdir()

    lf_file_path = lf_dir_path / 'cutter_table_scanner.xml'
    if not lf_file_path.exists():
        shutil.copy(ROOT_PATH / 'misc' / '_cameras.xml', lf_file_path)


# _create_static_folder()
_mkdir_scan_path()
_copy_lensfun_xml()