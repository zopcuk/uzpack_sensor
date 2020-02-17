import cv2
import threading
import numpy as np
import configparser
from gpiozero import Motor
import time
import math

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

def camPreview(previewName, camID):
    cap = cv2.VideoCapture(camID)
    config = configparser.ConfigParser()
    config.read('test.ini')
    motor1 = Motor(20, 21)
    motor2 = Motor(19, 26)
    print("running")

    while True:
        time.sleep(0.005)
        ret, img = cap.read()
        status_val = config.get('section_a', 'status_val')
        canny_min = config.getint('section_a', 'canny_min')
        canny_max = config.getint('section_a', 'canny_max')
        rho = config.getfloat('section_a', 'rho')
        l_threshold = config.getint('section_a', 'l_threshold')
        min_line_length = config.getint('section_a', 'min_line_length')
        max_line_gap = config.getint('section_a', 'max_line_gap')

        if status_val == "test":
            start_time = time.time()

        while ret == False:
            time.sleep(1)

            if status_val == "test":
                print("kamera baglantisi kopuk..")
                cv2.destroyWindow(previewName)

            if camID == cam0:
                motor1.stop()
            elif camID == cam1:
                motor2.stop()

            cap = cv2.VideoCapture(camID)
            ret, img = cap.read()


        if ret:
            x_crop = img.shape[1] / 2
            img = img[0:int(img.shape[0]),
                  int(x_crop - 50):int(x_crop + 50)]  # crop_img = img[y:y+h, x:x+w] y->dikey, x->yatay

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, ksize=(3, 3), sigmaX=0)
            edged = cv2.Canny(blur, canny_min,canny_max)  # Perform Edge detection

            rho = rho  # distance resolution in pixels of the Hough grid
            theta = np.pi / 180  # angular resolution in radians of the Hough grid
            threshold = l_threshold  # minimum number of votes (intersections in Hough grid cell)
            min_line_length = min_line_length  # minimum number of pixels making up a line
            max_line_gap = max_line_gap  # maximum gap in pixels between connectable line segments
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
                        slope = (y2 - y1) / (x2 - x1)  # <-- Calculating the slope.
                        if math.fabs(slope) < 0.2:
                            cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 3)
                            i = i + 1
                            y_values = y_values + y1 + y2
            i = i * 2
            if i != 0:
                y_median = y_values / i
            else:
                y_median = img.shape[0] / 2


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

            h_median_alt = h_value - 5
            h_median_ust = h_value + 5

            if y_median < h_median_alt:
                if status_val == "test":
                    print("{} down".format(camID))
                else:
                    if camID == cam0:
                        motor1.forward()
                    elif camID == cam1:
                        motor2.forward()
            elif y_median > h_median_ust:
                if status_val == "test":
                    print("{} up".format(camID))
                else:
                    if camID == cam0:
                        motor1.backward()
                    elif camID == cam1:
                        motor2.backward()
            else:
                if status_val == "test":
                    print("{} middle".format(camID))
                else:
                    if camID == cam0:
                        motor1.stop()
                    elif camID == cam1:
                        motor2.stop()

            if status_val == "test":
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

# Create threads as follows


cam0 = 0
cam1 = 1
thread1 = camThread("Camera 1", cam0)
thread2 = camThread("Camera 2", cam1)

thread1.start()
thread2.start()
print()
print("Active threads", threading.activeCount())
