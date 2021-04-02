import cv2
import numpy as np
import argparse
import json
from pathlib import Path
from operator import itemgetter


N_ROWS, N_COLS, PX_BETWEEN = 29, 33, 100

POSITIONS = ['LL', 'RL', 'RU', 'LU']
IMAGES_DIR = Path('.') / 'images'
CAMERAS_JSON = IMAGES_DIR / 'cameras.json'


if not CAMERAS_JSON.exists():
    data = { { 'serial': 'UNKNOWN', 'interpolation_points': [] } for position in POSITIONS }
    with open(CAMERAS_JSON, 'w') as file:
        json.dump(data, file, indent=4)


def image_path(filename):
    return str(IMAGES_DIR / filename)


def get_anchor_points():
    pass

    # template = cv2.imread('target.jpg',0)
    # w, h = template.shape[::-1]
    # res = cv2.matchTemplate(threshed,template,cv2.TM_CCOEFF_NORMED)
    # threshold = 0.5
    # loc = np.where( res >= threshold)
    # aDots = [[],[],[],[]]
    # for pt in zip(*loc[::-1]):
    #     # print(pt)
    #     if pt[0]<(W/2) and pt[1]<(H/2) :
    #         aDots[0].append(pt)
    #     elif pt[0]>(W/2) and pt[1]>(H/2) :
    #         aDots[1].append(pt)
    #     elif pt[0]<(W/2) and pt[1]>(H/2) :
    #         aDots[2].append(pt)
    #     elif pt[0]>(W/2) and pt[1]<(H/2) :
    #         aDots[3].append(pt)

    # for aDot in aDots:
    #     mean = list(aDot[0])
    #     for c in aDot[1:]:
    #         mean[0] = (mean[0] + c[0])/2
    #         mean[1] = (mean[1] + c[1])/2
    #     mean[0] = int(mean[0])
    #     mean[1] = int(mean[1])
    #     cv2.rectangle(img, (mean[0], mean[1]), (mean[0] + 57, mean[1] + 57), (0,0,255), 8)
    #     print(mean)

    # cv2.imwrite('res.jpg',img)


def with_contours_drawn(image: np.ndarray, contours: list):
    image = image.copy()

    contour_idx = -1  # if it is negative, all the contours are drawn.
    color = (255, 0, 0)
    thickness = 6
    cv2.drawContours(image, contours, contour_idx, color, thickness)

    return image


def with_circles_drawn(image: np.ndarray, dots: list):
    image = image.copy()

    circle_radius = 2
    circle_color = (0, 0, 255)
    circle_thickness = -1  # -1 fills the circle with circle_color

    text_font_scale = 0.5
    text_color = (255, 0, 0)
    text_thickness = 2

    for i, dot in enumerate(dots):
        center_x, center_y = dot[0], dot[1]
        cv2.circle(image, (center_x, center_y), circle_radius, circle_color, circle_thickness)

        text = str(i)
        text_bottom_left = (center_x - 20, center_y - 20)
        cv2.putText(image, text, text_bottom_left, cv2.FONT_HERSHEY_SIMPLEX, text_font_scale, text_color, text_thickness)

    return image


def sort_dots(dots: list):
    dots = sorted(dots, key=itemgetter(1))
    dots = [dots[i:i + N_COLS] for i in range(0, len(dots), N_COLS)]
    return [dot for row in dots for dot in sorted(row)]


def save_to_json(dots: list, position: str):
    def get_src_dst(dot, row, col):
        dot_x, dot_y = dot[1], dot[0]
        dst_x, dst_y = max(0, row * PX_BETWEEN - 1), max(0, col * PX_BETWEEN - 1)
        return {'src': [dot_x, dot_y], 'dst': [dst_x, dst_y]}

    dots = [dots[i:i + N_COLS] for i in range(0, len(dots), N_COLS)]
    dots = [get_src_dst(dot, i, j) for i, row in enumerate(dots) for j, dot in enumerate(row)]

    with open(CAMERAS_JSON, 'r') as file:
        data = json.load(file)
        data[position]['interpolation_points'] = dots

    CAMERAS_JSON.unlink()

    with open(CAMERAS_JSON, 'w') as file:
        json.dump(data, file, indent=4)


def find_contour_centers(contours: list):
    moments = [cv2.moments(contour) for contour in contours]
    return [(round(M["m10"] / M["m00"]), round(M["m01"] / M["m00"])) for M in moments]


def detect_dots(position: str):
    img_path = IMAGES_DIR / f'{position}.jpg'

    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imwrite(image_path(f'{position}_01_blurred.jpg'), blurred)

    _, threshed = cv2.threshold(blurred, 100, 255, cv2.THRESH_TOZERO)
    cv2.imwrite(image_path(f'{position}_02_threshed.jpg'), threshed)

    contours = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
    print('All contours count:', len(contours))
    cv2.imwrite(image_path(f'{position}_03_contours_all.jpg'), with_contours_drawn(img, contours))

    contours = [contour for contour in contours if 20 < cv2.contourArea(contour) < 170]
    print('Threshed contours count:', len(contours))
    cv2.imwrite(image_path(f'{position}_04_contours_filtered.jpg'), with_contours_drawn(img, contours))

    dots = find_contour_centers(contours)
    dots = sort_dots(dots)
    cv2.imwrite(image_path(f'{position}_05_dots.jpg'), with_circles_drawn(img, dots))

    save_to_json(dots, position)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--position", help="input image", required=True, choices=[*POSITIONS, 'all'])
    args = parser.parse_args()

    if args.position == "all":
        for position in POSITIONS:
            detect_dots(position)
    else:
        detect_dots(args.position)
