import os
from xml.etree.ElementTree import XML, ParseError
from shutil import copy
from pathlib import Path
from paths import DEFAULT_LENSFUN_XML_PATH


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
        return error.position


def read_lensfun_xml():
    return _get_lensfun_file().read_text()


def save_lensfun_xml(text: str):
    _get_lensfun_file().write_text(text)


_copy_lensfun_xml()