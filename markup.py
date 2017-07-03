import cv2
from scipy.spatial import distance
import numpy as np
import scipy.io as sio
from Tkinter import Tk
from tkFileDialog import askopenfilename

class markup:

    def __init__(self):
        self.ix, self.iy = -1, -1
        self.distance_pixel_ratio = 1.0
        self.filename = ''
        self.size = 25
        self.mode = False
        self.save = True
        self.mvsa_temp = 0.0
        self.mvsa = 0.0
        self.mvsa_markup = True
        self.mvsa_diam_markup = False


    def mouse_callback(self, event, x, y, flags, param):
        global iy, ix, drawing

        if event == cv2.EVENT_LBUTTONDOWN:
            ix, iy = x, y
            if self.mode:
                y1, x1, y2, x2 = self.get_points(x, y)
                cv2.rectangle(param, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0))
            else:
                cv2.line(param, (ix, iy), (x, y), (255, 0, 0), 2)

        elif event == cv2.EVENT_LBUTTONUP:
            if ~self.mode:
                cv2.line(param, (ix, iy), (x, y), (255, 0, 255), 2)
                dist = self.calculate_distance((ix, iy), (x, y))
                cv2.putText(param, str(dist), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
                if self.mvsa_markup:
                    if self.mvsa_diam_markup:
                        self.mvsa = float(self.mvsa + float(self.mvsa_temp * (dist/2) * np.pi))
                        self.mvsa_temp = 0.0
                    else:
                        self.mvsa_temp = float(self.mvsa + dist)

        elif event == cv2.EVENT_RBUTTONDOWN:
            ix, iy = x, y
            cv2.line(param, (ix, iy), (x, y), (0, 255, 0), 2)

        elif event == cv2.EVENT_RBUTTONUP:
            self.set_pixel_distance_ratio((ix, iy), (x, y), 2.0)
            cv2.line(param, (ix, iy), (x, y), (0, 255, 0), 2)


    def get_points(self, x, y):
        dist = float(1/(self.distance_pixel_ratio * 1/self.size))
        return (y + dist/2, x - dist/2, y - dist/2, y + dist/2)

    def calculate_distance(self, p1, p2):
        pix_dist = distance.euclidean(p1, p2)
        return float(self.distance_pixel_ratio * pix_dist)

    def set_pixel_distance_ratio(self, p1, p2, dist):
        pix_dist = distance.euclidean(p1, p2)
        self.distance_pixel_ratio = float(dist/pix_dist)

    def run(self):
        src = cv2.imread(self.filename)
        img = cv2.resize(src, None, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        cv2.namedWindow('markup', cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback('markup', self.mouse_callback, param=img)

        while cv2.waitKey(33) != ord('q'):
            if cv2.waitKey(33) == ord('m'):
                if self.mode:
                    self.mode = False
                    print("Now in line mode.")
                else:
                    self.mode = True
                    print("Now in rectangle mode.")
            if cv2.waitKey(33) == ord('n'):
                if self.save:
                    self.save = False
                    print("No longer in saving mode.")
                else:
                    self.save = True
                    print("Now in saving mode.")
            if cv2.waitKey(33) == ord('s'):
                if self.mvsa_markup:
                    self.mvsa_markup = False
                    print("No longer in mvsa markup mode.")
                else:
                    self.mvsa_markup = True
                    print("Now in mvsa markup mode.")
            if cv2.waitKey(33) == ord('d'):
                if self.mvsa_markup:
                    self.mvsa_markup = False
                    print("No longer in mvsa diameter markup mode.")
                else:
                    self.mvsa_markup = True
                    print("Now in mvsa diameter markup mode.")
            cv2.imshow('markup', img)
            cv2.waitKey(33)

        if self.save:
            cv2.imwrite(self.filename[:-4] + '_markup.jpg', img)
            self.save_markup()
        cv2.destroyAllWindows()

    def file_IO(self):
        print('Select the image to markup.')
        Tk().withdraw()
        self.filename = askopenfilename()

    def save_markup(self):
        sio.savemat(self.filename[:-4] + '_markup.mat', {'pixel_ratio':self.distance_pixel_ratio, 'mvsa':self.mvsa})