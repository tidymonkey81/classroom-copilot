export async function transcribeMP3(file: File, backendUrl: string) {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${backendUrl}/transcribe/local/faster-whisper-mp3-file`, {
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

let audioContext, source, processor, ws;  // Define these in a scope accessible by start and stop functions

export function startStreaming(setTranscript: React.Dispatch<React.SetStateAction<string>>, backendUrl: string): void {
  // Initialize audio capture and WebSocket connection
  audioContext = new AudioContext();
  /// ws = new WebSocket(`ws://${backendUrl.replace(/^http[s]?:\/\//, '')}/transcribe/local/faster-whisper-audio-stream`);
  ws = new WebSocket(`ws://${backendUrl.replace(/^http[s]?:\/\//, '')}/transcribe/live/whisper-live-audio-stream`);

  // Handle incoming WebSocket messages (transcription updates)
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    setTranscript(prev => `${prev}\n${data.transcription}`);
  };

  // Stream audio to the WebSocket
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      source = audioContext.createMediaStreamSource(stream);
      processor = audioContext.createScriptProcessor(4096, 1, 1);
      processor.onaudioprocess = (e) => {
        if (ws.readyState === WebSocket.OPEN) {
          const input = e.inputBuffer.getChannelData(0);
          console.log("Sending audio data", input.buffer); // Added console log
          ws.send(input.buffer);
        }
      };
      source.connect(processor);
      processor.connect(audioContext.destination);
    });
}

export function stopStreaming() {
  if (processor) processor.disconnect();
  if (source) source.disconnect();
  if (audioContext) audioContext.close();
  if (ws) ws.close();
}


export function startWhisperLiveWebsocket(setTranscript: React.Dispatch<React.SetStateAction<string>>, backendUrl: string): void {
  ws = new WebSocket(`ws://${backendUrl.replace(/^http[s]?:\/\//, '')}/transcribe/live/whisper-live-audio-stream`);
}

export function stopWhisperLiveWebsocket() {
  if (ws) ws.close();
}