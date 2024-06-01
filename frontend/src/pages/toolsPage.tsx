import React, { useState } from 'react';
import { Button, TextField, Container, Box, Typography, Input } from '@mui/material';
import { transcribeMP3 } from './services/transcribeService';


function tools() {
  const [file, setFile] = useState(null);
  const [backendUrl, setBackendUrl] = useState(`http://localhost:${import.meta.env.VITE_BACKEND_PORT}`);

  const handleTranscribeMP3 = () => {
    if (!file) {
      alert('Please select a file first!');
      return;
    }
    transcribeMP3(file, backendUrl);
  };

  return (
    <Container maxWidth="md" style={{ marginTop: '20px' }}>
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
      </Box>
    </Container>
  );
}

export default tools;