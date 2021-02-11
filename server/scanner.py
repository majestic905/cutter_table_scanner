from scan import Scan
from camera import Camera, CameraPosition
from processing import undistort, project, compose


cameras = {
    CameraPosition.RU: Camera('/dev/usb1', 'Canon', 'Canon Powershot S50'),
    CameraPosition.RL: Camera('/dev/usb2', 'Canon', 'Canon Powershot S50'),
    CameraPosition.LL: Camera('/dev/usb3', 'Nikon', 'Nikon Coolpix S9400'),
    CameraPosition.LU: Camera('/dev/usb4', 'Canon', 'Canon Powershot S50'),
}


def perform_scan():
    scan = Scan()
    # initialize logger connected to scan?

    scan.capture_photos(cameras)
    scan.build_undistorted_images(undistort, cameras)
    scan.build_projected_images(project, cameras)
    scan.build_result_image(compose)