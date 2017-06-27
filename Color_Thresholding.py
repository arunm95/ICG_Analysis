import cv2
import numpy as np

# Experience has determined adaptive mean thresholding to provide the best contrast, edge detection doesn't work either



def nothing(excess):
    pass








# MAIN METHODS

cap = cv2.VideoCapture('example1.avi')

# Get first frame of video
ret, frame = cap.read()
cv2.namedWindow('Video', cv2.WINDOW_AUTOSIZE)
cv2.namedWindow('Control', cv2.WINDOW_AUTOSIZE)
cv2.namedWindow('TVideo_AM', cv2.WINDOW_AUTOSIZE)

cv2.imshow('Video', frame)
f_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Adaptive Mean
th2 = cv2.adaptiveThreshold(f_grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
cv2.imshow('TVideo_AM', th2)

count = 0

while cv2.waitKey(33) != ord('q'):
    ret, frame = cap.read()
    cv2.imshow('Video', frame)
    f_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Adaptive Mean
    th2 = cv2.adaptiveThreshold(f_grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imshow('TVideo_AM', th2)

    if cv2.waitKey(30) == ord('i'):
        cv2.imwrite('example1_capture_video' + str(count) + '.jpg', frame)
        cv2.imwrite('example1_capture_thresh' + str(count) + '.jpg', frame)
        count = count + 1



