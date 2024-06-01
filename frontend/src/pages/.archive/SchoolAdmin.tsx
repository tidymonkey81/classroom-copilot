import React, { useState } from 'react';

function SchoolAdmin() {
  const [file, setFile] = useState(null);
  const [backendUrl, setBackendUrl] = useState(`http://localhost:${import.meta.env.VITE_BACKEND_PORT}`)

  async function createSchoolNode() {
    if (!file) {
        alert('Please select a file first!');
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${backendUrl}/school/create-school`, {
            method: 'POST',
            body: formData,
        });

        if (response.status === 200) {
            const result = await response.json();
            console.log(result);
            alert('Upload Successful!');
            } else {        
                alert('Upload failed!');
            }
            } catch (error) {
            console.error('Error creating school node:', error);
            alert('Creation failed!');
        }
    }

  async function uploadCurriculum() {
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${backendUrl}/curriculum/upload-subject-curriculum`, {
        method: 'POST',
        body: formData,
        // headers: {
          // 'Authorization': `Bearer ${yourAuthToken}` // Temporarily commented out
        // }
      });

      if (response.status === 200) {
        const result = await response.json(); // Only parse JSON if the status is not 200
        console.log(result);
        alert('Upload Successful!'); // The upload was successful
      } else {        
        alert('Upload failed!');
      }
    } catch (error) {
      console.error('Error uploading curriculum:', error);
      alert('Upload failed!');
    }
  }

  function handleFileChange(event) {
    setFile(event.target.files[0]);
  }

  function handleBackendUrlChange(event) {
    setBackendUrl(event.target.value);
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <div>
            <input type="file" id="schoolFile" name="schoolFile" onChange={handleFileChange} />
            <input type="text" value={backendUrl} onChange={handleBackendUrlChange} placeholder="Backend URL" />
            <button onClick={createSchoolNode}>Create School Node</button>
        </div>
        <div>
            <input type="file" id="curriculumFile" name="curriculumFile" onChange={handleFileChange} />
            <input type="text" value={backendUrl} onChange={handleBackendUrlChange} placeholder="Backend URL" />
            <button onClick={uploadCurriculum}>Upload Curriculum</button>
        </div>
    </div>
  );
}

export default SchoolAdmin;