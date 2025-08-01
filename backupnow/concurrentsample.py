import cv2
import configparser

# Function to update the ROI values and xcopy, ycopy values in config.ini
def update_config(x, y, width, height, xcopy, ycopy):
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Update the values in the [ROI] section
    config.set('ROI', 'x', str(x))
    config.set('ROI', 'y', str(y))
    config.set('ROI', 'width', str(width))
    config.set('ROI', 'height', str(height))

    # Update the xcopy and ycopy values
    config.set('ROI', 'xcopy', str(xcopy))
    config.set('ROI', 'ycopy', str(ycopy))

    # Write the updated configuration to the file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Create a callback function for mouse events
def click_event(event, x, y, flags, param):
    global points, exit_program, height, width, xcopy, ycopy
    if event == cv2.EVENT_LBUTTONDOWN:
        print(len(points))
        points.append((x, y))
        if len(points) == 2:
            x1, y1 = points[0]
            x2, y2 = points[1]
            x = min(x1, x2)
            y = min(y1, y2)
            width = abs(x1 - x2)
            height = abs(y1 - y2)
            print(f"x: {x}, y: {y}, width: {width}, height: {height}")
        if len(points) == 3:
            x, y = points[0]
            xcopy, ycopy = points[2]
            print(f"xcopy: {xcopy}, ycopy: {ycopy}")
            update_config(x, y, width, height, xcopy, ycopy)  # Update the config.ini file
            exit_program = True
            cv2.destroyAllWindows()

        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Image", img)

# Read an image
img = cv2.imread("roipicture.jpg")

# Create a window and bind the mouse callback function
cv2.imshow("Image", img)
points = []
xcopy, ycopy, height, width = 0, 0, 0, 0
exit_program = False
cv2.setMouseCallback("Image", click_event)

# Wait for a key press
cv2.waitKey(0)
