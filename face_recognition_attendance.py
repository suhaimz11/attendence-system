import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime

# Directory containing registered faces
REGISTERED_FACES_DIR = "registered_faces"
ATTENDANCE_FILE = "attendance.csv"

# Load registered face encodings and names
known_face_encodings = []
known_face_names = []

for user_name in os.listdir(REGISTERED_FACES_DIR):
    user_folder = os.path.join(REGISTERED_FACES_DIR, user_name)
    for image_name in os.listdir(user_folder):
        image_path = os.path.join(user_folder, image_name)
        image = face_recognition.load_image_file(image_path)
        try:
            encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(user_name)
        except IndexError:
            print(f"Could not encode face in {image_path}. Skipping...")

# Initialize webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Could not access the webcam.")
    exit()

print("Press 'q' to quit.")

# Attendance log
attendance_log = set()

def mark_attendance(name):
    """Mark attendance for a recognized user."""
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    if name not in attendance_log:
        with open(ATTENDANCE_FILE, "a") as file:
            file.write(f"{name},{timestamp}\n")
        attendance_log.add(name)
        print(f"Marked attendance for {name} at {timestamp}")

while True:
    # Capture video frame-by-frame
    ret, frame = video_capture.read()
    if not ret:
        print("Error: Frame not captured correctly.")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces and compute face encodings
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        # Compare detected face with registered faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Mark attendance if the face is recognized
        if name != "Unknown":
            mark_attendance(name)

        # Draw a rectangle and name around the detected face
        top, right, bottom, left = [v * 4 for v in face_location]  # Scale back up
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the video feed
    cv2.imshow('Face Recognition Attendance', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
