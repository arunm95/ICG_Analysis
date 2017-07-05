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
        self.mvsa_markup = False
        self.mvsa_diam_markup = False


    def mouse_callback(self, event, x, y, flags, param):
        global iy, ix, drawing

        if event == cv2.EVENT_LBUTTONDOWN:
            ix, iy = x, y
            if self.mode:
                cv2.rectangle(param, (ix, iy), (x, y), (255, 0, 0))
            else:
                cv2.line(param, (ix, iy), (x, y), (255, 0, 0))

        elif event == cv2.EVENT_LBUTTONUP:
            if not self.mode:
                cv2.line(param, (ix, iy), (x, y), (255, 0, 255))
                dist = self.calculate_distance((ix, iy), (x, y))
                if self.mvsa_markup:
                    if self.mvsa_diam_markup:
                        self.mvsa = float(self.mvsa + float(self.mvsa_temp * (dist) * np.pi))
                        self.mvsa_temp = 0.0
                    else:
                        self.mvsa_temp = float(self.mvsa + dist)
                else:
                    cv2.putText(param, str(dist), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
            else:
                cv2.rectangle(param, (ix, iy), (x, y), (255, 0, 0))
                dim = self.get_dim([ix, iy], [x, y])
                cv2.putText(param, str(dim[0]) + ', ' + str(dim[1]), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

        elif event == cv2.EVENT_RBUTTONDOWN:
            ix, iy = x, y
            cv2.line(param, (ix, iy), (x, y), (0, 255, 0), 2)

        elif event == cv2.EVENT_RBUTTONUP:
            self.set_pixel_distance_ratio((ix, iy), (x, y), 2.0)
            cv2.line(param, (ix, iy), (x, y), (0, 255, 0), 2)


    def get_dim(self, p1, p2):
        return [self.calculate_distance((p1[0], p1[1]),(p2[0], p1[1])),
                self.calculate_distance((p1[0], p1[1]), (p1[0], p2[1]))]

    def calculate_distance(self, p1, p2):
        pix_dist = distance.euclidean(p1, p2)
        return float(self.distance_pixel_ratio * pix_dist)

    def set_pixel_distance_ratio(self, p1, p2, dist):
        pix_dist = distance.euclidean(p1, p2)
        self.distance_pixel_ratio = float(dist/pix_dist)

    def run(self):
        count = 0
        src = cv2.imread(self.filename)
        img = cv2.resize(src, None, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        cv2.namedWindow('markup', cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback('markup', self.mouse_callback, param=img)
        print("Starting markup, click m to enter rectangle mode, press n to exit saving mode, press s to to mark up mvsa, r to clear the image and d to enter diameter mode.")
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
                if self.mvsa_diam_markup:
                    self.mvsa_diam_markup = False
                    print("No longer in mvsa diameter markup mode.")
                else:
                    self.mvsa_diam_markup = True
                    print("Now in mvsa diameter markup mode.")
            if cv2.waitKey(33) == ord('r'):
                if self.save:
                    cv2.imwrite(self.filename[:-4] + '_markup' + str(count) + '.jpg', img)
                    cv2.namedWindow('markup_' + str(count), cv2.WINDOW_AUTOSIZE)
                    cv2.imshow('markup_' + str(count), img)
                    count = count + 1
                src = cv2.imread(self.filename)
                img = cv2.resize(src, None, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                cv2.setMouseCallback('markup', self.mouse_callback, param=img)
            cv2.imshow('markup', img)
            cv2.waitKey(33)

        if self.save:
            cv2.imwrite(self.filename[:-4] + '_markup' + str(count) + '.jpg', img)
            self.save_markup()
        cv2.destroyAllWindows()

    def file_IO(self):
        print('Select the image to markup.')
        Tk().withdraw()
        self.filename = askopenfilename()

    def save_markup(self):
        sio.savemat(self.filename[:-4] + '_markup.mat', {'pixel_ratio':self.distance_pixel_ratio, 'mvsa':self.mvsa})