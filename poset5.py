import numpy as np
import cv2
import time
import configparser
from time import sleep
from gpiozero import Motor

motor = Motor(20, 21)

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
config = configparser.ConfigParser()
#y_median = 0
while True:
    ret, img = cap.read()

    config.read('test.ini')
    status_val = config.get('section_a', 'status_val')
    exit_val = config.getboolean('section_a', 'exit_val')
    canny_min = config.getint('section_a', 'canny_min')
    canny_max = config.getint('section_a', 'canny_max')
    rho = config.getfloat('section_a', 'rho')
    l_threshold = config.getint('section_a', 'l_threshold')
    min_line_length = config.getint('section_a', 'min_line_length')
    max_line_gap = config.getint('section_a', 'max_line_gap')

    if status_val == "test":
        start_time = time.time()

    while (ret == False):
        config.read('test.ini')
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        ret, img = cap.read()
        if status_val == "test":
            print("kamera baglantısı kopuk..")
        motor.stop()
        if exit_val:
            if status_val == "test":
                print("exit")
            break

    if ret:
        x_crop = img.shape[1] / 2
        img = img[0:int(img.shape[0]),
              int(x_crop - 50):int(x_crop + 50)]  # crop_img = img[y:y+h, x:x+w] y dikey, x yatay


        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, ksize=(3, 3), sigmaX=0)
        # cv2.imshow('blur', blur)
        '''sharp = cv2.addWeighted(blur, 2, gray, -0.5, 0)
        cv2.imshow('sharp', sharp)'''
        edged = cv2.Canny(blur, 30, 150)  # Perform Edge detection//////////////////////////////////////////////////////
        # cv2.imshow('edged', edged)

        rho = 2  # distance resolution in pixels of the Hough grid//////////////////////////////////////////////////////
        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 30  # minimum number of votes (intersections in Hough grid cell)////////////////////////////////////
        min_line_length = 3  # minimum number of pixels making up a line////////////////////////////////////////////////
        max_line_gap = 30  # maximum gap in pixels between connectable line segments////////////////////////////////////
        line_image = np.copy(img) * 0  # creating a blank to draw lines on

        # Run Hough on edge detected image
        # Output "lines" is an array containing endpoints of detected line segments
        lines = cv2.HoughLinesP(edged, rho, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)

        i = 0
        y_values = 0
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    i = i + 1
                    y_values = y_values + y1 + y2
        i = i * 2
        if i != 0:
            y_median = y_values / i
        else:
            y_median = img.shape[0] / 2


        dis = 600 - y_median


        lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)


        h_value = lines_edges.shape[0]
        w_value = lines_edges.shape[1]
        h_value = h_value / 2

        if status_val == "test":
            lines_edges = cv2.line(lines_edges, (0, int(h_value)), (w_value, int(h_value)), (0, 255, 0), 3)
            print("--- %s seconds ---" % (time.time() - start_time))
            cv2.imshow('Resized Window', lines_edges)
        else:
            cv2.destroyAllWindows()
            print("çalışıyor")

        h_median_alt = h_value - 5
        h_median_ust = h_value + 5

        if y_median < h_median_alt:
            if status_val == "test":
                print("aşağı")
            else:
                motor.forward()
        elif y_median > h_median_ust:
            if status_val == "test":
                print("yukarı")
            else:
                motor.backward()
        else:
            if status_val == "test":
                print("oratalandı")
            else:
                motor.stop()


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if exit_val:
        if status_val == "test":
            print("exit2")
        break
