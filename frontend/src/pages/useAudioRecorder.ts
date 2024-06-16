import { useState, useEffect } from 'react';

const useAudioRecorder = () => {
    const [audioURL, setAudioURL] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);

    useEffect(() => {
        // Ask for user permissions to access the microphone
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(stream => {
                    const newMediaRecorder = new MediaRecorder(stream);
                    setMediaRecorder(newMediaRecorder);

                    newMediaRecorder.ondataavailable = event => {
                        if (event.data.size > 0) {
                            setAudioURL(URL.createObjectURL(event.data));
                        }
                    };
                })
                .catch(console.error);
        }

        return () => {
            mediaRecorder?.stream.getTracks().forEach(track => track.stop());
        };
    }, []);

    const startRecording = () => {
        if (mediaRecorder && mediaRecorder.state === 'inactive') {
            mediaRecorder.start();
            setIsRecording(true);
        }
    };

    const stopRecording = () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            setIsRecording(false);
        }
    };

    return {
        audioURL,
        isRecording,
        startRecording,
        stopRecording
    };
};

export default useAudioRecorder;
