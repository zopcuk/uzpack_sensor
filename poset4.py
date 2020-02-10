import numpy as np
import cv2.cv2 as cv2
import time
import configparser
import gpiozero

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#y_median = 0

while(True):
    start_time = time.time()
    ret, img = cap.read()




    while (ret == False):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        ret, img = cap.read()
        print("kamera baglantısı kopuk..")
        '''if True:
            print("exit")
            break'''

    if ret:

        '''x_crop = img.shape[1]/2
        img = img[0:int(img.shape[0]), int(x_crop-50):int(x_crop+50)] #crop_img = img[y:y+h, x:x+w] y dikey, x yatay
        #print(img.shape)'''

        '''# define the screen resulation
        screen_res = 640, 480
        scale_width = screen_res[0] / img.shape[1]q
        scale_height = screen_res[1] / img.shape[0]
        scale = min(scale_width, scale_height)
    
        # resized window width and height
        window_width = int(img.shape[1] * scale)
        window_height = int(img.shape[0] * scale)
    
        # cv2.WINDOW_NORMAL makes the output window resizealbe
        cv2.namedWindow('Resized Window', cv2.WINDOW_NORMAL)
    
        # resize the window according to the screen resolution
        cv2.resizeWindow('Resized Window', window_width, window_height)'''


        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, ksize=(3, 3), sigmaX=0)
        #cv2.imshow('blur', blur)
        '''sharp = cv2.addWeighted(blur, 2, gray, -0.5, 0)
        cv2.imshow('sharp', sharp)'''
        edged = cv2.Canny(blur, 30, 150)  # Perform Edge detection/////////////////////////////////////////////////////
        cv2.imshow('edged', edged)


        blur2 = cv2.medianBlur(gray, 5)
        th3 = cv2.adaptiveThreshold(blur2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 8)
        th3 = (255-th3)
        cv2.imshow('th', th3)

        rho = 2  # distance resolution in pixels of the Hough grid//////////////////////////////////////////////////////
        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 30  # minimum number of votes (intersections in Hough grid cell)////////////////////////////////////
        min_line_length = 10  # minimum number of pixels making up a line///////////////////////////////////////////////
        max_line_gap = 30  # maximum gap in pixels between connectable line segments////////////////////////////////////
        line_image = np.copy(img) * 0  # creating a blank to draw lines on

        # Run Hough on edge detected image
        # Output "lines" is an array containing endpoints of detected line segments
        lines = cv2.HoughLinesP(edged, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

        i=0
        y_values=0
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(line_image, (x1, y1), (x2, y2),  (0, 0, 255), 3)
                    i=i+1
                    y_values=y_values+y1+y2
        i=i*2
        if i != 0:
            y_median=y_values/i
        else:
            y_median = img.shape[0]/2

        #print("ortalama y degeri = {}".format(int(y_median)))
        dis = 600 - y_median
        #print("merkezden uzaklık = {} piksel".format(int(dis)))

        lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)

        h_value = lines_edges.shape[0]
        w_value = lines_edges.shape[1]
        h_value = h_value/2
        lines_edges = cv2.line(lines_edges, (0, int(h_value)), (w_value, int(h_value)), (0, 255, 0), 3)
        print("--- %s seconds ---" % (time.time() - start_time))

        cv2.imshow('Resized Window', lines_edges)

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
    '''if True:
        print("exit2")
        break'''
