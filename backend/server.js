const express = require('express');
const multer = require('multer');
const fetch = require('node-fetch'); // Make sure to have 'node-fetch' installed for this
const FormData = require('form-data');
const cors = require('cors');

const app = express();
app.use(cors());
const upload = multer({ storage: multer.memoryStorage() });

app.post('/convert', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).send('No file uploaded.');
  }

  const formData = new FormData();
  formData.append('file', req.file.buffer, req.file.originalname);

  try {
    const flaskResponse = await fetch('http://127.0.0.1:5000/process', {
      method: 'POST',
      body: formData,
      headers: formData.getHeaders(),
    });

    if (!flaskResponse.ok) throw new Error('Failed to process file with Flask.');

    const result = await flaskResponse.json();
    console.log('File processed by Flask:', result);
    res.json({ message: 'File uploaded and processed successfully.', data: result });
  } catch (error) {
    console.error('Error communicating with Flask:', error);
    res.status(500).send('Internal server error.');
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
