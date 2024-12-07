import React, { useState } from 'react';
import './App.css';

function App() {
  const [status, setStatus] = useState('Ready to start attendance.');

  const startAttendance = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/start_attendance', {
        method: 'GET',
      });

      if (response.ok) {
        setStatus('Attendance started! Scan your face.');
      } else {
        setStatus('Error starting attendance.');
      }
    } catch (error) {
      setStatus('Error starting attendance: ' + error.message);
    }
  };

  return (
    <div className="App">
      <h1>Face ID Attendance System</h1>
      <p>{status}</p>
      <button onClick={startAttendance}>Start Attendance</button>
    </div>
  );
}

export default App;
