import cv2
import os

# Create a cascade classifier for face detection
face_cascade = cv2.CascadeClassifier( cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

# Create a VideoCapture object to capture frames from the webcam
cap = cv2.VideoCapture(0)

# Get the name of the person whose face is being registered
name = input("Enter the name of the person: ")

# Create a folder with the name of the person (if it doesn't exist already)
if not os.path.exists('fdata/'+name):
    os.makedirs('fdata/'+name)

# Initialize the counter for the number of faces registered
count = 0

# Keep capturing frames from the webcam and registering faces until the user presses 'q'
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    
    # Convert the frame to grayscale for faster processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Draw rectangles around the detected faces and save them to the folder
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        file_path = os.path.join('fdata/'+name, f"{name}_{count}.jpg")
        cv2.imwrite(file_path, roi_color)
        count += 1
        if count==100:
            break
    
    # Display the frame with rectangles around the detected faces
    cv2.imshow('frame', frame)
    
    # Break out of the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q')or count==100:
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
