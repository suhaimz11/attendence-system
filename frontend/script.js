document.getElementById("start-attendance").addEventListener("click", startAttendance);
document.getElementById("upload-face").addEventListener("click", uploadFace);
document.getElementById("view-attendance").addEventListener("click", viewAttendance);

// Start attendance by providing the student ID
async function startAttendance() {
    const studentId = document.getElementById("student-id").value;

    if (!studentId) {
        alert("Please enter a student ID.");
        return;
    }

    const response = await fetch('http://127.0.0.1:5000/api/start-attendance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ student_id: studentId })
    });

    const data = await response.json();
    alert(data.message);
}

// Upload a face image for registration
async function uploadFace() {
    const fileInput = document.getElementById("file-input");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file to upload.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch('http://127.0.0.1:5000/api/upload-face', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    alert(data.message);
}

// View the attendance records
async function viewAttendance() {
    const response = await fetch('http://127.0.0.1:5000/api/attendance', {
        method: 'GET'
    });

    const data = await response.json();

    if (data.length === 0) {
        alert("No attendance records found.");
        return;
    }

    const attendanceList = document.getElementById("attendance-list");
    attendanceList.innerHTML = "";  // Clear the existing list

    data.forEach(record => {
        const li = document.createElement("li");
        li.textContent = `${record.student_id}: ${record.timestamp}`;
        attendanceList.appendChild(li);
    });
}
