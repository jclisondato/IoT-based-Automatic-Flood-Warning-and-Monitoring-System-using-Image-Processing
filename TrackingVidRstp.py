#rtsp://admin:Thesis12!@192.168.137.100:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif

import cv2
import numpy as np


def nothing(x):
    pass


# Replace 'your_rtsp_url' with the actual RTSP URL of your camera
rtsp_url = 'rtsp://admin:Thesis12!@192.168.110.200:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif'

# Initialize the capture from the RTSP stream
cap = cv2.VideoCapture(rtsp_url)

cv2.namedWindow('Trackbars')
cv2.createTrackbar('Hue Lower', 'Trackbars', 0, 179, nothing)
cv2.createTrackbar('Hue Upper', 'Trackbars', 179, 179, nothing)
cv2.createTrackbar('Saturation Lower', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('Saturation Upper', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('Value Lower', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('Value Upper', 'Trackbars', 255, 255, nothing)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame to a smaller size (e.g., 640x480)
    resized_frame = cv2.resize(frame, (640, 480))

    hsv_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV)

    # Get trackbar positions
    h_lower = cv2.getTrackbarPos('Hue Lower', 'Trackbars')
    h_upper = cv2.getTrackbarPos('Hue Upper', 'Trackbars')
    s_lower = cv2.getTrackbarPos('Saturation Lower', 'Trackbars')
    s_upper = cv2.getTrackbarPos('Saturation Upper', 'Trackbars')
    v_lower = cv2.getTrackbarPos('Value Lower', 'Trackbars')
    v_upper = cv2.getTrackbarPos('Value Upper', 'Trackbars')

    lower_color = np.array([h_lower, s_lower, v_lower])
    upper_color = np.array([h_upper, s_upper, v_upper])

    mask = cv2.inRange(hsv_frame, lower_color, upper_color)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 100:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(resized_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Original', resized_frame)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
