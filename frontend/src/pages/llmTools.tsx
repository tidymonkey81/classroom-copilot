import React, { useState } from 'react';
import { Button, TextField, Container, Box, Typography, Select, MenuItem } from '@mui/material';
import { sendPrompt, sendVisionPrompt } from './services/llmService';

function LLMTools() {
  const backendBaseUrl = import.meta.env.VITE_BACKEND_URL;
  console.log(backendBaseUrl);
  const backendBasePort = import.meta.env.VITE_BACKEND_PORT;
  const backendUrl = `${backendBaseUrl}:${backendBasePort}`;
  const [backendUrlState, setBackendUrlState] = useState(backendUrl);
  const [prompt, setPrompt] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  const [model, setModel] = useState('llama3');
  const [temperature, setTemperature] = useState(0.7);
  const [imagePath, setImagePath] = useState('');
  const [visionResponse, setVisionResponse] = useState('');

  const handleSendPrompt = async () => {
    if (!prompt) {
      alert('Please enter a prompt!');
      return;
    }
    const responseData = await sendPrompt({ model, prompt, temperature }, backendUrlState);
    setResponseMessage(responseData.response);
  };

  const handleVisionPrompt = async () => {
    if (!imagePath || !prompt) {
      alert('Please enter an image path and a prompt!');
      return;
    }
    const responseData = await sendVisionPrompt({ model, imagePath, prompt }, backendUrlState);
    setVisionResponse(responseData.response);
  };

  return (
    <Container maxWidth="md" style={{ marginTop: '20px', height: '100vh', overflowY: 'auto' }}>
      <Typography variant="h4" gutterBottom>Ollama Tools</Typography>
      <Box display="flex" flexDirection="column" alignItems="center" gap={2}>
        <TextField
          label="Backend URL"
          variant="outlined"
          value={backendUrlState}
          onChange={(e) => setBackendUrlState(e.target.value)}
          fullWidth
        />
      </Box>
      
      {/* Text Tools Section */}
      <Box display="flex" flexDirection="column" alignItems="center" gap={2} marginTop="20px">
        <Typography variant="h5" gutterBottom>Text Tools</Typography>
        <Select
          value={model}
          onChange={(e) => setModel(e.target.value as string)}
          displayEmpty
          inputProps={{ 'aria-label': 'Select model' }}
        >
          <MenuItem value="llama3">llama3</MenuItem>
          <MenuItem value="llama2">llama2</MenuItem>
          <MenuItem value="mistral">mistral</MenuItem>
          <MenuItem value="llava">llava</MenuItem>
        </Select>
        <TextField
          label="Temperature"
          type="number"
          variant="outlined"
          value={temperature}
          onChange={(e) => setTemperature(parseFloat(e.target.value))}
          fullWidth
        />
        <TextField
          label="Enter Prompt"
          variant="outlined"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          fullWidth
        />
        <Button variant="contained" color="primary" onClick={handleSendPrompt}>
          Send Text Prompt
        </Button>
        <TextField
          label="Text Response"
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

      {/* Image Tools Section */}
      <Box display="flex" flexDirection="column" alignItems="center" gap={2} marginTop="20px">
        <Typography variant="h5" gutterBottom>Image Tools</Typography>
        <TextField
          label="Image Path"
          variant="outlined"
          value={imagePath}
          onChange={(e) => setImagePath(e.target.value)}
          fullWidth
        />
        <TextField
          label="Image Prompt"
          variant="outlined"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          fullWidth
        />
        <Button variant="contained" color="primary" onClick={handleVisionPrompt}>
          Send Vision Prompt
        </Button>
        <TextField
          label="Vision Response"
          variant="outlined"
          value={visionResponse}
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

export default LLMTools;
