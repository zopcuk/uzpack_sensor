import cv2
import threading
import numpy as np

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

    while True:
        ret, img = cap.read()

        while ret == False:
            #cap.release()

            cv2.destroyWindow(previewName)
            cap = cv2.VideoCapture(camID)
            ret, img = cap.read()
            print("kamera baglantısı kopuk..")
            '''if True:
                print("exit")
                break'''

        if ret:

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, ksize=(3, 3), sigmaX=0)
            # cv2.imshow('blur', blur)
            edged = cv2.Canny(blur, 30, 150)  # Perform Edge detection//////////////////////////////////////////////////

            rho = 2  # distance resolution in pixels of the Hough grid//////////////////////////////////////////////////
            theta = np.pi / 180  # angular resolution in radians of the Hough grid
            threshold = 30  # minimum number of votes (intersections in Hough grid cell)////////////////////////////////
            min_line_length = 10  # minimum number of pixels making up a line///////////////////////////////////////////
            max_line_gap = 30  # maximum gap in pixels between connectable line segments////////////////////////////////
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


            lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)

            h_value = lines_edges.shape[0]
            w_value = lines_edges.shape[1]
            h_value = h_value / 2
            lines_edges = cv2.line(lines_edges, (0, int(h_value)), (w_value, int(h_value)), (0, 255, 0), 3)


            cv2.imshow(previewName, lines_edges)

            h_median_alt = h_value - 5
            h_median_ust = h_value + 5

            if y_median < h_median_alt:
                print("aşağı")
            elif y_median > h_median_ust:
                print("yukarı")
            else:
                print("oratalandı")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Create threads as follows
thread1 = camThread("Camera 1", 0)
thread2 = camThread("Camera 2", 1)

thread1.start()
thread2.start()
print()
print("Active threads", threading.activeCount())
