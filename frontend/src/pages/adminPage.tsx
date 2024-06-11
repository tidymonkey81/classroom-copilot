import React, { useState } from 'react';
import { Button, TextField, Container, Box, Typography, Input } from '@mui/material';
import { createGlobalSchoolDB } from './services/adminDBService';
import { createSchoolNode, createSchoolNodes } from './services/schoolDBService';
import { uploadCurriculum, uploadSubjectCurriculum } from './services/curriculumDBService';

function Admin() {
  const [file, setFile] = useState(null);
  const [backendUrl, setBackendUrl] = useState(`http://${import.meta.env.VITE_BACKEND_URL}:${import.meta.env.VITE_BACKEND_PORT}`);

  const handleCreateGlobalSchoolDB = () => {
    createGlobalSchoolDB(backendUrl);
  };

  const handleCreateSchoolNode = () => {
    if (!file) {
      alert('Please select a file first!');
      return;
    }
    createSchoolNode(file, backendUrl);
  };

  const handleCreateSchoolNodesBatch = () => {
    if (!file) {
      alert('Please select a file first!');
      return;
    }
    createSchoolNodesBatch(file, backendUrl);
  };

  const handleUploadCurriculum = () => {
    if (!file) {
      alert('Please select a file first!');
      return;
    }
    uploadCurriculum(file, backendUrl);
  };

  const handleUploadSubjectCurriculum = () => {
    if (!file) {
      alert('Please select a file first!');
      return;
    }
    uploadSubjectCurriculum(file, backendUrl);
  };

  return (
    <Container maxWidth="md" style={{ marginTop: '20px' }}>
      <Typography variant="h4" gutterBottom>Admin Management</Typography>
      <Box display="flex" flexDirection="column" alignItems="center" gap={2}>
        <TextField
          label="Backend URL"
          variant="outlined"
          value={backendUrl}
          onChange={(e) => setBackendUrl(e.target.value)}
          fullWidth
        />
        <Button variant="contained" color="primary" onClick={handleCreateGlobalSchoolDB}>
          Create Global School DB
        </Button>
        <Input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          disableUnderline
          inputProps={{ 'aria-label': 'Upload file' }}
        />
        <Button variant="contained" color="secondary" onClick={handleCreateSchoolNode}>
          Create School Node
        </Button>
        <Button variant="contained" color="secondary" onClick={handleCreateSchoolNodesBatch}>
          Create School Nodes
        </Button>
        <Button variant="contained" color="secondary" onClick={handleUploadCurriculum}>
          Upload Curriculum
        </Button>
        <Button variant="contained" color="secondary" onClick={handleUploadSubjectCurriculum}>
          Upload Subject Curriculum
        </Button>
      </Box>
    </Container>
  );
}

export default Admin;