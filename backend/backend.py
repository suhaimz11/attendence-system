from flask import Flask, jsonify, request, send_file
import os
import csv
from werkzeug.utils import secure_filename
import subprocess  # To run Python scripts
import json

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'registered_faces'
ATTENDANCE_FILE = 'attendance.csv'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Endpoint: Get attendance data
@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    attendance_data = []
    try:
        with open(ATTENDANCE_FILE, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                attendance_data.append(row)
    except FileNotFoundError:
        return jsonify({"message": "Attendance file not found"}), 404
    return jsonify(attendance_data)

# Endpoint: Upload face data (for registration)
@app.route('/api/upload-face', methods=['POST'])
def upload_face():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Run the face registration script
        try:
            subprocess.run(["python", "face_registration.py", filename], check=True)
            return jsonify({"message": f"File {filename} uploaded and face registered successfully"}), 200
        except subprocess.CalledProcessError:
            return jsonify({"message": "Error registering face"}), 500

# Endpoint: Start attendance (using face recognition)
@app.route('/api/start-attendance', methods=['POST'])
def start_attendance():
    student_id = request.json.get('student_id')
    if not student_id:
        return jsonify({"message": "Student ID is required"}), 400
    
    try:
        # Run the face recognition attendance script
        result = subprocess.run(
            ["python", "face_recognition_attendance.py", student_id],
            capture_output=True, text=True, check=True
        )
        # Assuming the script outputs a success message, we return it.
        return jsonify({"message": result.stdout.strip()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"message": f"Error processing attendance: {e.stderr}"}), 500

# Endpoint: Serve registered face images (optional for debugging)
@app.route('/api/registered-faces/<filename>', methods=['GET'])
def get_registered_face(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath)
    return jsonify({"message": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
