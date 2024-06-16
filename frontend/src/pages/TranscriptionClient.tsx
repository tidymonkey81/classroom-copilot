import React, { useState, useEffect } from 'react';
import { bytesToFloatArray, createSRTFile } from './audioUtils';

interface Segment {
  text: string;
  start: string;
  end: string;
}

const TranscriptionClient = ({ host, port }: { host: string; port: number }) => {
  const [transcript, setTranscript] = useState<Segment[]>([]);
  const [socket, setSocket] = useState<WebSocket | null>(null);

  useEffect(() => {
    const socketUrl = `ws://${host}:${port}`;
    const ws = new WebSocket(socketUrl);

    ws.onopen = () => {
      console.log("Connected to the server");
      // Initial configuration message to the server
      const message = {
        uid: "client-uid",  // Generate or reuse a unique id for the client
        language: "en",
        task: "transcribe",
        model: "small",
        useVad: true,
      };
      ws.send(JSON.stringify(message));
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.segments) {
        processSegments(message.segments);
      }
    };

    ws.onerror = (event) => {
      console.error("WebSocket error:", event);
    };

    ws.onclose = (event) => {
      console.log(`WebSocket is closed: ${event.reason}`);
    };

    setSocket(ws);

    // Clean up on component unmount
    return () => {
      ws.close();
    };
  }, [host, port]);

  const processSegments = (segments: Segment[]) => {
    setTranscript((prevTranscript) => [...prevTranscript, ...segments]);
  };

  const sendAudioPacket = (audioBuffer: ArrayBuffer) => {
    if (socket) {
      socket.send(audioBuffer);
    }
  };

  return (
    <div>
      <h1>Transcription Client</h1>
      <div>
        {transcript.map((seg, index) => (
          <p key={index}>{seg.text} ({seg.start} - {seg.end})</p>
        ))}
      </div>
    </div>
  );
};

export default TranscriptionClient;
