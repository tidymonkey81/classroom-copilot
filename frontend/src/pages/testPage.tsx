import React from 'react';
import useAudioRecorder from './useAudioRecorder';

const TranscriptionClient = ({ host, port }: { host: string; port: number }) => {
    const { isRecording, startRecording, stopRecording, audioURL } = useAudioRecorder();
    const [socket, setSocket] = React.useState<WebSocket | null>(null);

    React.useEffect(() => {
        const socketUrl = `ws://${host}:${port}`;
        const ws = new WebSocket(socketUrl);

        ws.onopen = () => {
            console.log("WebSocket connection established.");
        };

        setSocket(ws);

        return () => {
            ws.close();
        };
    }, [host, port]);

    React.useEffect(() => {
        if (audioURL && socket) {
            socket.send(audioURL); // Send audio URL or blob data
        }
    }, [audioURL, socket]);

    return (
        <div>
            <h1>Transcription Service</h1>
            {isRecording ? (
                <button onClick={stopRecording}>Stop Recording</button>
            ) : (
                <button onClick={startRecording}>Start Recording</button>
            )}
            <audio src={audioURL} controls />
        </div>
    );
};

export default TranscriptionClient;
