import os
from datetime import datetime

SCANS_DIRECTORY_PATH = os.path.join(os.path.dirname(__file__), 'scans')

if not os.path.exists(SCANS_DIRECTORY_PATH):
    os.mkdir(SCANS_DIRECTORY_PATH)


def path_to_dict(path):
    name = os.path.basename(path)

    if os.path.isdir(path):
        return {
            'type': 'D',
            'name': name,
            'children': [path_to_dict(os.path.join(path, x)) for x in os.listdir(path)]
        }
    else:
        stat_result = os.lstat(path)

        return {
            'type': 'F',
            'name': name,
            'mtime': stat_result.st_mtime,
            'size': stat_result.st_size
        }


def get_scans_directory_tree():
    tree = path_to_dict(SCANS_DIRECTORY_PATH)

    directories = tree['children']  # omit root directory and return list of subdirectories
    for item in directories:
        when = datetime.fromtimestamp(int(item['name'][:-3]))
        item['name'] = when.strftime('%d %B %Y, %H:%M')

    return directories
