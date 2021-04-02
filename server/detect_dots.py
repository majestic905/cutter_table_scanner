import cv2
import numpy as np
import argparse
from operator import itemgetter

N_ROWS, N_COLS = 29, 33


def with_circles_drawn(image: np.ndarray, dots: list):
    image = image.copy()

    circle_radius = 2
    circle_color = (0, 0, 255)
    circle_thickness = -1  # -1 fills the circle with circle_color

    text_font_scale = 0.5
    text_color = (255, 0, 0)
    text_thickness = 2

    for i, dot in enumerate(dots):
        circle_center = (dot[0], dot[1])
        cv2.circle(image, circle_center, circle_radius, circle_color, circle_thickness)

        text = str(i)
        text_bottom_left = (dot[0] - 20, dot[1] - 20)
        cv2.putText(image, text, text_bottom_left, cv2.FONT_HERSHEY_SIMPLEX, text_font_scale, text_color, text_thickness)


def get_dots_matrix(dots: list):
    dots = sorted(dots, key=itemgetter(1))
    dots = [dots[i:i + N_COLS] for i in range(0, len(dots), N_COLS)]
    return [sorted(row) for row in dots]


def write_dots_json(filename: str, dots: list):
    with open(filename, 'w') as output:
        for row in dots:
            for dot in row:
                output.write(
                    '{"src": [%d, %d], "dst": [%d, %d]},' % (dot[1], dot[0], max(0, r * 100 - 1), max(0, c * 100 - 1)))


def detect_dots(filename: str):
    name, ext = filename.split('.')

    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshed = cv2.threshold(blurred, 100, 255, cv2.THRESH_TOZERO)
    cv2.imwrite(f'{name}_threshed.{ext}', threshed)

    contours = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
    print('All found contours count:', len(contours))

    contours = [contour for contour in contours if 20 < cv2.contourArea(contour) < 170]
    print('Threshed contours count:', len(contours))

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

    dots = []

    # cv2.drawContours(img, contours, -1, (255, 0, 0), 6)
    for i in range(len(contours)):
        M = cv2.moments(contours[i])
        cX = round(M["m10"] / M["m00"])
        cY = round(M["m01"] / M["m00"])
        dots.append([cX, cY])

    dots = get_dots_matrix(dots)
    cv2.imwrite(f'{name}_circles.{ext}', with_circles_drawn(img, dots))

    write_dots_json(f'{name}.json', dots)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="input image")
    args = parser.parse_args()

    filename = args.file
    detect_dots(filename)
