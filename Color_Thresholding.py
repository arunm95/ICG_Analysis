import cv2
import os
from os import mkdir
import numpy as np
from Tkinter import Tk
from tkFileDialog import askopenfilename
# Experience has determined adaptive mean thresholding to provide the best contrast, edge detection doesn't work either

class ImgCapture:

    def __init__(self):
        self.filename = ''

    def run(self):
        cap = cv2.VideoCapture(self.filename)

        # Get first frame of video
        ret, frame = cap.read()
        cv2.namedWindow('Video', cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow('capture', cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow('TVideo_AM', cv2.WINDOW_AUTOSIZE)

        cv2.imshow('Video', frame)
        f_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Adaptive Mean
        th2 = cv2.adaptiveThreshold(f_grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        cv2.imshow('TVideo_AM', th2)

        count = 0

        print('Tap I to capture an image, and q to quit.')

        while cv2.waitKey(33) != ord('q'):
            ret, frame = cap.read()
            cv2.imshow('Video', frame)
            f_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Adaptive Mean
            th2 = cv2.adaptiveThreshold(f_grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
            cv2.imshow('TVideo_AM', th2)

            if cv2.waitKey(33) == ord('i'):
                if not os.path.exists(self.filename[:-4]):
                    os.mkdir(self.filename[:-4])
                cv2.imwrite(self.filename[:-4] + '/capture_orig' + str(count) + '.jpg', frame)
                cv2.imshow('capture', frame)
                cv2.imwrite(self.filename[:-4] + '/capture_thresh' + str(count) + '.jpg', th2)
                count = count + 1
        cv2.destroyAllWindows()

    def file_IO(self):
        print('Select the video file.')
        Tk().withdraw()
        self.filename = askopenfilename()

