import time
import csv
import numpy as np
import cv2
from Tkinter import Tk
from tkFileDialog import askopenfilename


class Transit_Time:

    def __init__(self):
        self.filename = ''
        self.list = list()

    def run(self):
        MVTT = float(input("Input MVTT"))
        AMVTT = float(input("Input AMVTT"))
        VMVTT = float(input("Input VMVTT"))
        name = self.filename[-22:-4]
        self.list.append([name, MVTT, AMVTT, VMVTT])
        print(self.list[-1])

    def save_csv(self):
        with open("transit_time_output_2.csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerows(self.list)

    def file_IO(self):
        print('Select the video file.')
        Tk().withdraw()
        self.filename = askopenfilename()

tt = Transit_Time()
while (raw_input("continue? (y/n)") == 'y'):
    tt.file_IO()
    tt.run()
tt.save_csv()