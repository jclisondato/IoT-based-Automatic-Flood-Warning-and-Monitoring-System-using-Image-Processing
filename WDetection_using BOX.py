import cv2

# Set up the video capture object
cap = cv2.VideoCapture(0)  # Use 0 for the default camera, or specify the video file path

# Define the region of interest (ROI) coordinates
x, y, width, height = 341, 78, 100, 200

# Initialize the water level position
water_level_position = y + height

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))

    # Check if the frame was successfully read
    if not ret:
        break

    # Extract the ROI from the frame
    roi = frame[y:y+height, x:x+width]

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

    # Draw the ROI rectangle on the frame
    cv2.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 2)

    # Draw the water level line within the ROI
    cv2.line(frame, (x, water_level_position), (x+width, water_level_position), (0, 0, 255), 2)

    # Display the frame
    cv2.imshow("Water Level Detection", frame)
    cv2.imshow("Threshold", threshold)
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
