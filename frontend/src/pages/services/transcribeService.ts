export async function transcribeMP3(file: File, backendUrl: string) {
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const response = await fetch(`${backendUrl}/transcribe/local/faster-whisper`, {
        method: 'POST',
        body: formData,
      });
  
      if (response.status === 200) {
        const result = await response.json();
        console.log(result);
        alert('MP3 Uploaded Successfully!');
      } else {
        alert('MP3 Upload failed!');
      }
    } catch (error) {
      console.error('Error uploading MP3:', error);
      alert('MP3 Upload failed!');
    }
  }
