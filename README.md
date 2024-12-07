# Face Recognition Attendance System

This project is a Face Recognition Attendance System built using Python for the backend and HTML, CSS, and JavaScript for the frontend. The system allows for registering faces, detecting faces in real-time, and marking attendance when a recognized face is detected.

## Features

- **Face Registration:** Allows users to register their faces for the attendance system.
- **Face Detection:** Detects faces in real-time using the webcam.
- **Attendance Logging:** Marks attendance when a recognized face is detected and saves the records in a CSV file.

## Prerequisites

Before running the system, make sure to install the necessary dependencies.

### Backend (Python)

1. **Python 3.x**: Ensure Python 3.x is installed on your machine.
2. **Required Libraries**: Install the required libraries using `pip`:
    ```bash
    pip install opencv-python face_recognition werkzeug numpy
    ```

### Frontend

- **HTML/CSS/JavaScript**: Standard web technologies for the frontend. The frontend interacts with the backend via REST API calls.

## Project Setup

### 1. Clone the Repository

Clone this project to your local machine:
```bash
git clone <repository-url>
cd <project-directory>
