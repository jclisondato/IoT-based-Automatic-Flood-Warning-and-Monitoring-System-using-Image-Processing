import cv2
import threading
from telegramcommands import telegram
import time
import configparser
import requests
from collections import Counter

watercolor = ["Green"]
colorsendfrequency = ["Green"]
config = configparser.ConfigParser()
config.read('config.ini')
api_token = '6127325854:AAGsCeqD6SZApUMGU5yWHmMpwX0Y7TNLRpY'
chat_id = '-1001926809085'


colorcheck = []
x = config.getint('ROI', 'x')
y = config.getint('ROI', 'y')
width = config.getint('ROI', 'width')
height = config.getint('ROI', 'height')

stop_countdown = False

def imageprocessing():
    global stop_countdownthread
    #cap = cv2.VideoCapture("morning_300s.avi")

    #fps check
    # fps_start_time = time.time()
    # fps_counter = 0

    while True:
        water_level_position = y + height
        rstp = 'rtsp://admin:Thesis12!@192.168.110.200:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif'
        cap = cv2.VideoCapture(rstp)
        #frame = cv2.imread("picture2.jpg")
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        cv2.imwrite('picture.jpg', frame)
        # Check if the frame was successfully read
        if not ret:
           break

        # Extract the ROI from the frame
        roi = frame[y:y + height, x:x + width]
        # Convert the ROI to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        # Apply a threshold to create a binary image that highlights the water level
        _, threshold = cv2.threshold(gray_roi, 127, 255, cv2.THRESH_BINARY)
        # Find contours in the binary image
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Iterate over the contours and check if the water level has risen above a certain threshold
        water_level = 150  # Adjust this value as needed
        for contour in contours:
            # Compute the area and bounding box of each contour
            area = cv2.contourArea(contour)
            x_contour, y_contour, w_contour, h_contour = cv2.boundingRect(contour)
            # If the area exceeds the water level threshold, update the water level position
            if area > water_level:
                water_level_position = y + y_contour + h_contour
                coloridentify = y_contour + h_contour
                colorcheck.append(map_value_to_color(coloridentify, height))
                if len(colorcheck) == 3: #Odd number only
                    if frequentcolors() == watercolor[0]:
                        colorcheck.clear()
                    else:
                        colorsendfrequency.clear()
                        stop_countdown_thread(countdown_thread)
                        colorsendfrequency.append(frequentcolors)
                        sendPhotoStatus(watercolor[0],frequentcolors())
                        watercolor[0] = frequentcolors()
                    print(frequentcolors())
        # Draw the ROI rectangle on the frame
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
        # Draw the water level line within the ROI
        cv2.line(frame, (x, water_level_position), (x + width, water_level_position), (0, 0, 255), 2)

        cv2.imshow("Water Level Detection", frame)
        cv2.imshow("Threshold", threshold)
        #cv2.imwrite('picture.jpg', frame)

        # fps_counter += 1
        # if time.time() - fps_start_time >= 1:  # Check FPS every 1 second
        #     fps = fps_counter / (time.time() - fps_start_time)
        #     print(f"FPS: {fps:.2f}")
        #     fps_start_time = time.time()
        #     fps_counter = 0

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera when done
    cap.release()
    cv2.destroyAllWindows()

def frequentcolors():
    word_counts = Counter(colorcheck)
    target_words = {"Green", "Yellow", "Orange", "Red"}
    most_frequent_word = max(target_words, key=lambda word: word_counts[word])
    return most_frequent_word
def map_value_to_color(color,height):
    if color >= height * 0.75:
        return "Green"
    elif height * 0.75 >= color >= height * 0.5:
        return "Yellow"
    elif height * 0.5 >= color >= height * 0.25:
        return "Orange"
    elif height * 0.25 >= color >= 0:
        return 'Red'



def countdown(seconds):
    global stop_countdown
    for i in range(seconds, 0, -1):
        if stop_countdown:
            #print("Countdown stopped.")
            return
        time.sleep(1)
        print(f"Countdown {i}.")
    else:
        caption = (f'Color Status{frequentcolors()}, \n'
                   f'Image Status Time Interval: {map_string_to_value(frequentcolors())}')
        #print(caption)
        image_path = 'picture.jpg'
        url = f'https://api.telegram.org/bot{api_token}/sendPhoto'
        files = {'photo': open(image_path, 'rb')}
        data = {'chat_id': chat_id, 'caption': caption}
        response = requests.post(url, files=files, data=data)
        stop_countdown_thread(countdown_thread)
        start_countdown(seconds)


def start_countdown(duration):
    global stop_countdown
    stop_countdown = False
    countdown_thread = threading.Thread(target=countdown, args=(duration,))
    countdown_thread.start()
    return countdown_thread
# Function to stop the countdown
def stop_countdown_thread(countdown_thread):
    global stop_countdown
    stop_countdown = True
    countdown_thread.join()

def sendPhotoStatus(prevColor,currentColor):
    #print(map_string_to_value(prevColor))
    #print(map_string_to_value(currentColor))
    if map_string_to_value(prevColor) > map_string_to_value(currentColor):
        start_countdown(map_string_to_value(currentColor))
        caption = (f'Water Level is rising to {currentColor}, image status interval change to {map_string_to_value(currentColor)}')
        image_path = 'picture.jpg'
        url = f'https://api.telegram.org/bot{api_token}/sendPhoto'
        files = {'photo': open(image_path, 'rb')}
        data = {'chat_id': chat_id, 'caption': caption}
    elif map_string_to_value(prevColor) < map_string_to_value(currentColor):
        start_countdown(map_string_to_value(currentColor))
        caption = (f'Water Level is droping to {currentColor}, image status interval change to {map_string_to_value(currentColor)}')
        image_path = 'picture.jpg'
        url = f'https://api.telegram.org/bot{api_token}/sendPhoto'
        files = {'photo': open(image_path, 'rb')}
        data = {'chat_id': chat_id, 'caption': caption}


def map_string_to_value(color): # in seconds
    color_mapping = {
        "Green": 20,
        "Yellow": 15,
        "Orange": 10,
        "Red": 5,
    }
    return color_mapping.get(color, -1)

def maintotelegramColorStatus():
    color = watercolor[0]
    print(color)
    return color

# Start threads
#thread1 = threading.Thread(target=telegram)
thread2 = threading.Thread(target=imageprocessing)
countdown_thread = start_countdown(20)
#thread1.start()
thread2.start()




#condition for the intervals of rising and droping