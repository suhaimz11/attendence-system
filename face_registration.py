import cv2
import os

# Set up the directory to save registered faces
SAVE_DIR = "registered_faces"
os.makedirs(SAVE_DIR, exist_ok=True)

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Could not access the webcam.")
    exit()

print("Face Registration Started. Press 'q' to quit.")
user_name = input("Enter the name of the person to register: ").strip()

if not user_name:
    print("Error: No name entered. Exiting.")
    exit()

# Create a folder for the user
user_folder = os.path.join(SAVE_DIR, user_name)
os.makedirs(user_folder, exist_ok=True)

image_count = 0
max_images = 20  # Number of images to capture

while image_count < max_images:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    if not ret:
        print("Error: Frame not captured correctly.")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Extract the face region
        face = frame[y:y+h, x:x+w]

        # Save the face as an image file
        image_path = os.path.join(user_folder, f"face_{image_count}.jpg")
        cv2.imwrite(image_path, face)
        image_count += 1
        print(f"Saved {image_path}")

        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Break if the max number of images is reached
        if image_count >= max_images:
            break

    # Display the frame
    cv2.imshow('Face Registration', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(f"Face registration completed. {image_count} images saved in {user_folder}.")

# Release the webcam and close OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
