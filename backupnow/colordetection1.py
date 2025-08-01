import cv2
import numpy as np

#rtsp_url = "rtsp://admin:Safetycode12@192.168.110.200:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
cap=cv2.VideoCapture(0)
lower_rangeR=np.array([0,76,142])
upper_rangeR=np.array([2,255,196])
lower_rangeO=np.array([0,78,203])
upper_rangeO=np.array([7,255,255])
lower_rangeY=np.array([16,55,248])
upper_rangeY=np.array([255,255,255])
lower_rangeG=np.array([69,23,0])
upper_rangeG=np.array([85,255,140])

def red(img):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_rangeR, upper_rangeR)
    _, mask1 = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cnts:
        x = 2000
        if cv2.contourArea(c) > x:
            x, y, w, h = cv2.boundingRect(c)
            coordinates = [x, y, w, h, (0, 0, 255)]
            color.append(coordinates)
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(image, ("RED"), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

def orange(img):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_rangeO, upper_rangeO)
    _, mask1 = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cnts:
        x = 600
        if cv2.contourArea(c) > x:
            x, y, w, h = cv2.boundingRect(c)
            coordinates = [x, y, w, h,(0, 165, 255)]
            color.append(coordinates)
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 2)
            cv2.putText(image, ("ORANGE"), (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

def yellow(img):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_rangeY, upper_rangeY)
    _, mask1 = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cnts:
        x = 600
        if cv2.contourArea(c) > x:
            x, y, w, h = cv2.boundingRect(c)
            coordinates = [x, y, w, h,(0,255,255)]
            color.append(coordinates)
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,255), 2)
            cv2.putText(image, ("YELLOW"), (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

def green(img):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_rangeG, upper_rangeG)
    _, mask1 = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for c in cnts:
        x = 600
        if cv2.contourArea(c) > x:
            x, y, w, h = cv2.boundingRect(c)
            coordinates = [x, y, w, h,(0, 255, 0)]
            color.append(coordinates)
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, ("GREEN"), (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

coordinates = [(331, 89), (611, 136), (267, 454), (58, 367)]

color = []
while True:
    ret,image=cap.read()
    #image = cv2.imread('original.jpg')
    image = cv2.resize(image, (640, 480))
    mask = cv2.imread('mask.jpg', cv2.IMREAD_GRAYSCALE)
    frame = cv2.bitwise_and(image, image, mask=mask)

    red(frame)
    orange(frame)
    yellow(frame)
    green(frame)
    for x,y,w,h,rgb in color:
        cv2.rectangle(image, (x, y), (x + w, y + h), (rgb), 2)
    for i in range(len(coordinates)):
        cv2.line(image, coordinates[i-1], coordinates[i], (100, 100, 255), 2)
    color.clear()
    #cv2.imshow("mask", mask)
    cv2.imshow("FRAME",image)
    if cv2.waitKey(1)&0xFF==27:
        break
#cap.release()
cv2.destroyAllWindows()