import cv2
import threading
from telegramcommands import telegram
import time
import configparser
import requests
from collections import Counter
from telegram import Update, InputTextMessageContent, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters


watercolor = ["Green"]
#colorsendfrequency = ["Green"]
config = configparser.ConfigParser()
config.read('config.ini')
api_token = '6127325854:AAGsCeqD6SZApUMGU5yWHmMpwX0Y7TNLRpY'
chat_id = '-1001926809085'

colorcheck = []
x = config.getint('ROI', 'x')
y = config.getint('ROI', 'y')
width = config.getint('ROI', 'width')
height = config.getint('ROI', 'height')

stop_countdownRed = False
stop_countdownOrange = False
stop_countdownYellow = False
stop_countdownGreen = False

def imageprocessing():
    global stop_countdownthread
    rstp = 'rtsp://admin:Thesis12!@192.168.110.200:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif'
    cap = cv2.VideoCapture(rstp)

    # #fps check
    # fps_start_time = time.time()
    # fps_counter = 0

    while True:
        water_level_position = y + height
        #frame = cv2.imread("picture1.jpg")
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        cv2.imwrite('picture.jpg', frame)
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
        water_level = 10  # Adjust this value as needed
        for contour in contours:
            # Compute the area and bounding box of each contour
            area = cv2.contourArea(contour)
            x_contour, y_contour, w_contour, h_contour = cv2.boundingRect(contour)
            # If the area exceeds the water level threshold, update the water level position
            if area > water_level:
                water_level_position = y + y_contour + h_contour
                coloridentify = y_contour + h_contour
                #print(coloridentify)
                colorcheck.append(map_value_to_color(coloridentify, height))
                print(map_value_to_color(coloridentify, height))

                if len(colorcheck) == 31: #Odd number only
                    if frequentcolors() == watercolor[0]:
                        colorcheck.clear()
                    else:
                        #colorsendfrequency.clear()
                        #stop_countdown_thread(countdown_thread)
                        #colorsendfrequency.append(frequentcolors)
                        sendPhotoStatus(watercolor[0],frequentcolors())
                        watercolor.clear()
                        watercolor.append(frequentcolors())
                        colorcheck.clear()
                # print(f"watercolor[0]: {watercolor[0]}"
                #       f"frequentcolors(): {frequentcolors()}")
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


def sendPhotoStatus(prevColor,currentColor):
    # print(map_string_to_value(prevColor))
    # print(map_string_to_value(currentColor))
    if map_string_to_value(prevColor) > map_string_to_value(currentColor):
        #stop_countdown_thread(map_string_to_value(currentColor))
        caption = (f'Water Level is rising from {prevColor} to {currentColor}, image status interval change to {map_string_to_value(currentColor)}')
        image_path = 'picture.jpg'
        url = f'https://api.telegram.org/bot{api_token}/sendPhoto'
        files = {'photo': open(image_path, 'rb')}
        data = {'chat_id': chat_id, 'caption': caption}
        requests.post(url, files=files, data=data)
    elif map_string_to_value(prevColor) < map_string_to_value(currentColor):
        #start_countdown(map_string_to_value(currentColor))
        caption = (f'Water Level is droping from {prevColor} to {currentColor}, image status interval change to {map_string_to_value(currentColor)}')
        image_path = 'picture.jpg'
        url = f'https://api.telegram.org/bot{api_token}/sendPhoto'
        files = {'photo': open(image_path, 'rb')}
        data = {'chat_id': chat_id, 'caption': caption}
        requests.post(url, files=files, data=data)

def map_string_to_value(color): # in seconds
    color_mapping = {
        "Green": 12,
        "Yellow": 9,
        "Orange": 6,
        "Red": 4,
    }
    return color_mapping.get(color, -1)

def frequentcolors():
    word_counts = Counter(colorcheck)
    target_words = {"Green", "Yellow", "Orange", "Red"}
    most_frequent_word = max(target_words, key=lambda word: word_counts[word])
    return most_frequent_word
def map_value_to_color(color,height):
    #print(f'color: {color},'
          #f'height: {height * 0.25}')
    if color >= height * 0.75:
        return "Green"
    elif height * 0.75 > color >= height * 0.5:
        return "Yellow"
    elif height * 0.5 > color >= height * 0.25:
        return "Orange"
    elif height * 0.25 > color >= 0:
        return 'Red'
##############################################################################################################
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! This is your bot.')

def statusmapping(color):
    color_mapping = {
        "Green": 'Baseline(Normal Monitoring)',
        "Yellow": 'Normal(Alert or Ready)',
        "Orange": 'Warning(Pre-Emptive Evacuation',
        "Red": 'Evacuate(Assisted Evacuation)',
    }
    return color_mapping.get(color, -1)
# Define a function to handle commands other than /start
def handle_commands(update: Update, context: CallbackContext):
    # Get the text of the incoming message
    text = update.message.text

    # Check if the message starts with "/"
    if text.startswith('/'):
        # Split the message into command and arguments
        command, *args = text[1:].split()
        # Handle different commands here
        if 'image' in command:
            image_path = 'picture.jpg' # change to camera live image
            update.message.reply_photo(open(image_path, 'rb'))
        elif 'help' in command:
            update.message.reply_text('Use "/" commands. ')
        elif 'status' in command:
            update.message.reply_text(f'Warning Code:{watercolor[0]}\n'
                                      f'Status:{statusmapping(watercolor[0])}')
        elif 'contact' in command:
            update.message.reply_text('EMERGENCY CONTACTS: 09123456789')
        # Add more commands as needed
        else:
            update.message.reply_text('I can only understand commands starting with "/."')

# Define a function to handle all non-command messages
def handle_non_commands(update: Update, context: CallbackContext):
    text = update.message.text
    # Check if the message starts with "/"
    if not text.startswith('/'):
        # Delete the incoming message
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

def telegram():
    # Replace 'YOUR_BOT_TOKEN' with your Telegram Bot API token
    updater = Updater(token=api_token, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # Register command handlers
    dp.add_handler(CommandHandler('start', start))
    # Register a message handler for non-command messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_non_commands))
    # Register a message handler to handle commands
    dp.add_handler(MessageHandler(Filters.text & Filters.command, handle_commands))
    # Start the Bot
    updater.start_polling()
    # Run the bot until you send a signal to stop it (e.g., Ctrl+C)
    updater.idle()

###################################################################################################################
def countdown(seconds):
    global stop_countdown
    print(seconds)
    timer = seconds
    for i in range(seconds, 0, -1):
        if timer != map_string_to_value(frequentcolors()):
            print("Countdown changed.")
            break
        print(f"countdown: {i}")
        time.sleep(1)
        continue
    caption = (f'Water Level is {frequentcolors()}, \n'
               f'Image Status Time Interval: {map_string_to_value(frequentcolors())}')
    image_path = 'picture.jpg'
    url = f'https://api.telegram.org/bot{api_token}/sendPhoto'
    files = {'photo': open(image_path, 'rb')}
    data = {'chat_id': chat_id, 'caption': caption}
    requests.post(url, files=files, data=data)
    countdown(map_string_to_value(frequentcolors()))

# def start_countdown(duration):
#     global stop_countdown
#     stop_countdown = False
#     countdown_thread = threading.Thread(target=countdown, args=(duration,))
#     print(f'check time: {duration}')
#     countdown_thread.start()
# # Function to stop the countdown
# def stop_countdown_thread(duration):
#     global stop_countdown
#     stop_countdown = True
#     return start_countdown(duration)


###################################################################################################################
# Start threads

thread1 = threading.Thread(target=telegram)
thread2 = threading.Thread(target=imageprocessing)
thread3 = threading.Thread(target=countdown, args=(map_string_to_value(watercolor[0]),))
thread1.start()
thread2.start()
thread3.start()
#if stop_initial == True:
#start_countdown(3)
# start_countdown(map_string_to_value(watercolor[0]))
