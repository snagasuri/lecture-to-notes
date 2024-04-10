// Any component or page file within app directory, e.g., app/pages/upload.jsx
'use client'
import { useState } from 'react';

export default function Upload() {
  const [message, setMessage] = useState('');
  const [description, setDescription] = useState(''); // State to hold the description

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) {
      setMessage('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:3001/convert', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();
    if (response.ok) {
      setMessage('File uploaded successfully.');
      setDescription(result.data.description); // Update the state with the description
    } else {
      setMessage(`Upload failed: ${result.error}`);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleUpload} accept="application/pdf" />
      <div>{message}</div>
      <div>Description: {description}</div> {/* Display the description */}
    </div>
  );
}
