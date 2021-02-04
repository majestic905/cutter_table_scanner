import os
from flask import url_for
from shutil import rmtree
from random import randrange
from datetime import datetime, timedelta

SCANS_DIRECTORY_PATH = os.path.join(os.path.dirname(__file__), 'scans')


def _create_scans_directory():
    if not os.path.exists(SCANS_DIRECTORY_PATH):
        os.mkdir(SCANS_DIRECTORY_PATH)


_create_scans_directory()


def get_scans_directories_list():
    directories = []

    for name in os.listdir(SCANS_DIRECTORY_PATH):
        directories.append({
            'name': name,
            'createdAt': datetime.fromtimestamp(int(name)).strftime('%d %B %Y, %H:%M')
        })

    return directories


def perform_scan():
    def random_date(start, end):
        """
        This function will return a random datetime between two datetime
        objects.
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    start, end = datetime(2018, 1, 1, 0, 0, 0), datetime.now()
    dt = random_date(start, end)
    ts = dt.timestamp()
    name = str(int(ts))
    path = os.path.join(SCANS_DIRECTORY_PATH, name)
    os.mkdir(path)


def delete_scans_directories():
    rmtree(SCANS_DIRECTORY_PATH)
    _create_scans_directory()
