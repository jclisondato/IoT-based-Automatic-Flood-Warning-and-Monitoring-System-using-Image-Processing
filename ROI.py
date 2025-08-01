import time

import cv2
import configparser

# Function to update the ROI values in config.ini
def update_config(x, y, width, height):
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Update the values in the [ROI] section
    config.set('ROI', 'x', str(x))
    config.set('ROI', 'y', str(y))
    config.set('ROI', 'width', str(width))
    config.set('ROI', 'height', str(height))

    # Write the updated configuration to the file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Create a callback function for mouse events
def click_event(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        if len(points) == 2:
            x1, y1 = points[0]
            x2, y2 = points[1]
            x = min(x1, x2)
            y = min(y1, y2)
            width = abs(x1 - x2)
            height = abs(y1 - y2)
            print(f"x: {x}, y: {y}, width: {width}, height: {height}")
            points.clear()
            cv2.destroyAllWindows()  # Close the window after calculation
            update_config(x, y, width, height)  # Update the config.ini file

        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Image", img)

def snap():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (640, 480))
        cv2.imwrite('picture.jpg', frame)
    cap.release()

snap()
# Read an image
img = cv2.imread("picture.jpg")

# Create a window and bind the mouse callback function
cv2.imshow("Image", img)
points = []
cv2.setMouseCallback("Image", click_event)

# Wait for a key press
cv2.waitKey(0)
