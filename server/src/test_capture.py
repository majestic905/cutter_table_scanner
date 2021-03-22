import logging
import argparse
import gphoto2 as gp
from timeit import default_timer as timer
from threading import Thread

logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s', level=logging.WARNING)
callback_obj = gp.check_result(gp.use_python_logging())


def get_cameras():
    port_info_list = gp.PortInfoList()
    port_info_list.load()

    def get_port_info(addr):
        index = port_info_list.lookup_path(addr)
        return port_info_list[index]

    def get_camera(args):
        name, addr = args

        camera = gp.Camera()
        camera.set_port_info(get_port_info(addr))
        camera.init()

        serial_number = camera.get_single_config('serialnumber').get_value()
        logging.warning(f'Port {addr} is taken by camera with name `{name}` and serial number `{serial_number}`')
        return (serial_number, camera)

    return {
        serial_number: camera for serial_number, camera in
        map(get_camera, gp.Camera.autodetect())
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


def capture_serial():
    cameras = get_cameras()

    for serial_number, camera in cameras.items():
        capture(serial_number, camera)


def capture_parallel():
    cameras = get_cameras()

    threads = []
    for serial_number, camera in cameras.items():
        thread = Thread(target=capture, args=(serial_number, camera))
        threads.append(thread)
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--parallel", action="store_true")
    args = parser.parse_args()
   
    start = timer()

    try:
        if args.parallel:
            logging.warning('Capturing in parallel mode')
            capture_parallel()
        else:
            logging.warning('Capturing in serial mode')
            capture_serial()
    except Exception:
        logging.warning('Some exception occurred', exc_info=True)
    finally:
        end = timer()
        logging.warning(f'Elapsed time: {end - start}')

