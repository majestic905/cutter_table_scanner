import cv2
import numpy as np
import argparse
from operator import itemgetter

N_ROWS, N_COLS, PX_BETWEEN = 29, 33, 100


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
        center_x, center_y = round(dot[0]), round(dot[1])
        cv2.circle(image, (center_x, center_y), circle_radius, circle_color, circle_thickness)

        text = str(i)
        text_bottom_left = (center_x - 20, center_y - 20)
        cv2.putText(image, text, text_bottom_left, cv2.FONT_HERSHEY_SIMPLEX, text_font_scale, text_color, text_thickness)

    return image


def sort_dots(dots: list):
    dots = sorted(dots, key=itemgetter(1))
    dots = [dots[i:i + N_COLS] for i in range(0, len(dots), N_COLS)]
    return [dot for row in dots for dot in sorted(row)]


def write_dots_json(filename: str, dots: list):
    def get_line(dot, row, col):
        dot_x, dot_y = dot[1], dot[0]
        dst_x, dst_y = max(0, row * PX_BETWEEN - 1), max(0, col * PX_BETWEEN - 1)
        return f'{{"src": [{dot_x}, {dot_y}], "dst": [{dst_x}, {dst_y}]}}'

    dots = [dots[i:i + N_COLS] for i in range(0, len(dots), N_COLS)]
    lines = [get_line(dot, i, j) for i, row in enumerate(dots) for j, dot in enumerate(row)]

    with open(filename, 'w') as output:
        output.writelines(",\n".join(lines))


def find_contour_centers(contours: list):
    moments = [cv2.moments(contour) for contour in contours]
    return [(M["m10"] / M["m00"], M["m01"] / M["m00"]) for M in moments]


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


def detect_dots(filename: str):
    name, ext = filename.split('.')

    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imwrite(f'{name}_01_blurred.{ext}', blurred)

    _, threshed = cv2.threshold(blurred, 100, 255, cv2.THRESH_TOZERO)
    cv2.imwrite(f'{name}_02_threshed.{ext}', threshed)

    contours = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
    print('All contours count:', len(contours))
    cv2.imwrite(f'{name}_03_contours_all.{ext}', with_contours_drawn(img, contours))

    contours = [contour for contour in contours if 20 < cv2.contourArea(contour) < 170]
    print('Threshed contours count:', len(contours))
    cv2.imwrite(f'{name}_04_contours_filtered.{ext}', with_contours_drawn(img, contours))

    dots = find_contour_centers(contours)
    dots = sort_dots(dots)
    cv2.imwrite(f'{name}_05_dots.{ext}', with_circles_drawn(img, dots))

    write_dots_json(f'{name}.json', dots)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="input image")
    args = parser.parse_args()

    filename = args.file
    detect_dots(filename)
