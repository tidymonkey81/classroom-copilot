import React, { useState } from 'react';
import { Button, TextField, Container, Box, Typography, Input } from '@mui/material';
import { transcribeMP3 } from './services/transcribeService';
import { sendPrompt } from './services/llmService';


function tools() {
  const [file, setFile] = useState(null);
  const [backendUrl, setBackendUrl] = useState(`http://localhost:${import.meta.env.VITE_BACKEND_PORT}`);
  const [prompt, setPrompt] = useState('');
  const [responseMessage, setResponseMessage] = useState('');

  const handleTranscribeMP3 = () => {
    if (!file) {
      alert('Please select a file first!');
      return;
    }
    transcribeMP3(file, backendUrl);
  };

  const handleSendPrompt = async () => { // Make sure to declare this function as async
    if (!prompt) {
      alert('Please enter a prompt!');
      return;
    }
    const responseData = await sendPrompt(prompt, backendUrl); // Update to handle response
    setResponseMessage(responseData); // Set the response data to state
  };

  return (
    <Container maxWidth="md" style={{ marginTop: '20px' }} className="container">
      <Typography variant="h4" gutterBottom>Transcription Tools</Typography>
      <Box display="flex" flexDirection="column" alignItems="center" gap={2}>
        <TextField
          label="Backend URL"
          variant="outlined"
          value={backendUrl}
          onChange={(e) => setBackendUrl(e.target.value)}
          fullWidth
        />
        <Input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          disableUnderline
          inputProps={{ 'aria-label': 'Upload file' }}
        />
        <Button variant="contained" color="primary" onClick={handleTranscribeMP3}>
          Transcribe MP3
        </Button>
        <TextField
          label="Enter Prompt"
          variant="outlined"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          fullWidth
        />
        <Button variant="contained" color="primary" onClick={handleSendPrompt}>
          Send Prompt
        </Button>
        <TextField
          label="Response"
          variant="outlined"
          value={responseMessage}
          fullWidth
          multiline
          minRows={5}
          InputProps={{
            readOnly: true,
          }}
        />
      </Box>
    </Container>
  );
}

export default tools;