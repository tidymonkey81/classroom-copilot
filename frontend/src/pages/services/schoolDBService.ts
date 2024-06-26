export async function createSchoolNode(file: File, backendUrl: string) {
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const response = await fetch(`${backendUrl}/database/school/create-school`, {
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

  export async function createSchoolNodesBatch(file: File, backendUrl: string) {
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const response = await fetch(`${backendUrl}/database/schools/batch-create-schools`, {
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
      console.error('Error creating school nodes:', error);
      alert('Creation failed!');
    }
  }