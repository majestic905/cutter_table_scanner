#!/usr/bin/env python

# python-gphoto2 - Python interface to libgphoto2
# http://github.com/jim-easterbrook/python-gphoto2
# Copyright (C) 2014-20  Jim Easterbrook  jim@jim-easterbrook.me.uk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# "object oriented" version of camera-summary.py

from __future__ import print_function

import logging
import gphoto2 as gp
from operator import itemgetter
from threading import Thread

logging.basicConfig(format='%(levelname)s: %(asctimeS)s: %(message)s', level=logging.WARNING)
callback_obj = gp.check_result(gp.use_python_logging())


def get_cameras():
    port_info_list = gp.PortInfoList()
    port_info_list.load()

    def get_port_info(addr):
        index = port_info_list.lookup_path(addr)
        return port_info_list[index]

    def get_camera(addr):
        camera = gp.Camera()
        camera.set_port_info(get_port_info(addr))
        camera.init()

        serial_number = camera.get_single_config('serialnumber').get_value()
        logging.warning(f'Port {addr} is taken by serial number {serial_number}')
        return (serial_number, camera)

    return {
        serial_number: camera for serial_number, camera in
        map(get_camera, map(itemgetter(1), gp.Camera.autodetect()))
    }


def capture(serial_number: str, camera: gp.Camera):
    logging.warning(f'{serial_number} capture start')
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    logging.warning(f'{serial_number} capture end: {file_path.folder}/{file_path.name}')

    logging.warning(f'{serial_number} file_get start')
    camera_file: gp.CameraFile = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    logging.warning(f'{serial_number} file_get end')

    logging.warning(f'{serial_number} save start')
    camera_file.save(f'./{file_path.name}')
    logging.warning(f'{serial_number} save end')

    logging.warning(f'{serial_number} delete start')
    camera.file_delete(file_path.folder, file_path.name)
    logging.warning(f'{serial_number} delete end')


def main():
    cameras = get_cameras()

    for serial_number, camera in cameras.items():
        capture(serial_number, camera)


    # threads = []
    # for serial_number, camera in cameras.items():
    #     thread = Thread(target=capture, args=(serial_number, camera))
    #     threads.append(thread)
    #
    # for thread in threads:
    #     thread.start()
    #
    # for thread in threads:
    #     thread.join()

if __name__ == "__main__":
    main()