import cv2
import os
import numpy as np

import datetime
import smtplib
import subprocess

# Email login credentials
email = "weapondetector@gmail.com"
password = "ehycnaltfqdgqkdo"

# Email details
to_email = "sg7744@srmist.edu.in"
subject = "ALERT"
body = "Unauthorized Access has been detected!"

# Create an SMTP object
smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
smtp_server.starttls()

# Login to the email account
smtp_server.login(email, password)

# Create the email message
message = f"Subject: {subject}\n\n{body}"

# Create a cascade classifier for face detection
face_cascade = cv2.CascadeClassifier( cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

# Create a recognizer for face recognition
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Get the paths of the folders containing the training data
data_path = 'fdata/'
folders = os.listdir(data_path)

# Initialize dictionaries for mapping between person names and labels
name_to_label = {}
label_to_name = {}

# Initialize lists for storing the training data and labels
X_train = []
y_train = []

# Assign unique integer labels to each person in the dataset
label = 0
for folder in folders:
    name_to_label[folder] = label
    label_to_name[label] = folder
    files = os.listdir(data_path + folder)
    for file in files:
        img = cv2.imread(data_path + folder + '/' + file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            X_train.append(roi_gray)
            y_train.append(label)
    label += 1

# Train the recognizer on the training data and labels
recognizer.train(X_train, np.array(y_train))

# Create a VideoCapture object to capture frames from the webcam
cap = cv2.VideoCapture(0)

# Keep detecting faces and recognizing them until the user presses 'q'
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    
    # Convert the frame to grayscale for faster processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    name ="no face"
    # Recognize the detected faces and display their names
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        label, confidence = recognizer.predict(roi_gray)
        print(confidence)
        if confidence<65:
            name = label_to_name[label]
        else:
            name="Unauthorized"
            


        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Display the frame with names and rectangles around the detected faces
    cv2.imshow('frame', frame)
    
    # Break out of the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q')or name=="Unauthorized":
       
 
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
subprocess.run("python detect2.py --weights model.pt --conf 0.5 --img-size 640 --source 0 --view-img --no-trace")

smtp_server.sendmail(email, to_email, message)
smtp_server.quit()