import React, { useState } from 'react';

function CCAdmin() {
  const [backendUrl, setBackendUrl] = useState(`http://localhost:${import.meta.env.VITE_BACKEND_PORT}`);

  async function createGlobalSchoolDB() {
    try {
      const response = await fetch(`${backendUrl}/admin/create-global-school-db`, {
        method: 'POST',
      });
      if (response.status === 200) {
        const result = await response.json(); // Only parse JSON if the status is 200
        console.log(result);
        console.log(result.message);
        alert('Global school DB created!'); // The global db was created
      } else {        
        alert('Global school DB creation failed!');
      }
    } catch (error) {
      console.error('Error creating global school db:', error);
      alert('Global school DB creation failed!');
    }
  }

  function handleBackendUrlChange(event) {
    setBackendUrl(event.target.value);
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <div>
        <input type="text" value={backendUrl} onChange={handleBackendUrlChange} placeholder="Backend URL" />
        <button onClick={createGlobalSchoolDB}>Create Global School DB</button>
      </div>
    </div>
  );
}

export default CCAdmin;

