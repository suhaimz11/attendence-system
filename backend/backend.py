from flask import Flask, jsonify, request, send_file
import os
import csv
from werkzeug.utils import secure_filename

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

# Endpoint: Upload face data (for registering faces)
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
        return jsonify({"message": f"File {filename} uploaded successfully"}), 200

# Endpoint: Start attendance (Mark attendance)
@app.route('/api/start-attendance', methods=['POST'])
def start_attendance():
    data = request.get_json()
    student_id = data.get('student_id')
    timestamp = data.get('timestamp')

    if not student_id or not timestamp:
        return jsonify({"message": "Invalid data"}), 400

    # Append attendance to CSV file
    with open(ATTENDANCE_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['student_id', 'timestamp'])
        writer.writerow({'student_id': student_id, 'timestamp': timestamp})

    return jsonify({"message": "Attendance marked successfully"}), 200

# Endpoint: Serve registered face images (optional for debugging)
@app.route('/api/registered-faces/<filename>', methods=['GET'])
def get_registered_face(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath)
    return jsonify({"message": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
