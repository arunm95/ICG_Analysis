import cv2
from scipy.spatial import distance

drawing = False
ix, iy = -1, -1
distance_pixel_ratio = 1.0

def mouse_callback(event, x, y, flags, param):
    global iy, ix, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        cv2.line(img, (ix, iy), (x, y), (255, 0, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(img, (ix, iy), (x, y), (255, 0, 255), 2)
        dist = calculate_distance((ix, iy), (x, y))
        cv2.putText(img, str(dist), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

def calculate_distance(p1, p2):
    pix_dist = distance.euclidean(p1, p2)
    return float(distance_pixel_ratio * pix_dist)

def set_pixel_distance_ratio(p1, p2, dist):
    global distance_pixel_ratio
    pix_dist = distance.euclidean(p1, p2)
    distance_pixel_ratio = float(dist/pix_dist)


img = cv2.imread('example1_capture_thresh4.jpg')
cv2.namedWindow('markup', cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback('markup', mouse_callback)

while cv2.waitKey(33) != ord('q'):
    cv2.imshow('markup', img)
    cv2.waitKey(33)

# cv2.imwrite('example1_capture_thresh1_markup.jpg', img)