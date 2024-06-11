from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, WebSocket, WebSocketDisconnect
from faster_whisper import WhisperModel
import numpy as np
import logging
from datetime import datetime
from threading import Lock

router = APIRouter()

audio_buffer_lock = Lock()

logging.basicConfig(level=logging.DEBUG)

@router.websocket("/faster-whisper-audio-stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    model = WhisperModel('tiny', device='cpu')
    audio_buffer = bytearray()
    last_sound_time = datetime.now()  # Initialize when the connection starts
    recording = False
    silence_threshold = 10000  # Adjust this threshold based on your needs
    min_silence_duration = 5  # seconds
    min_chunk_size = 1024 * 16  # Minimum size of audio data to process

    try:
        while True:
            data = await websocket.receive_bytes()
            with audio_buffer_lock:
                # Create a temporary copy for processing to avoid resizing issues
                temp_buffer = bytearray(audio_buffer)
                temp_buffer.extend(data)
                audio_data = np.frombuffer(temp_buffer, dtype=np.int16)
                # Calculate peak amplitude instead of RMS
                current_volume = np.max(np.abs(audio_data))
                logging.debug(f"Current volume: {current_volume}")

                # Log if the volume is consistently at maximum
                if current_volume >= 32767:
                    logging.debug("Potential clipping detected. Check microphone settings.")

                if current_volume > silence_threshold:
                    if not recording:
                        recording = True
                        logging.debug("Started recording due to volume threshold.")
                    last_sound_time = datetime.now()

                if recording and (datetime.now() - last_sound_time).total_seconds() > min_silence_duration:
                    if len(temp_buffer) >= min_chunk_size:
                        logging.debug(f"Processing buffered audio data: {len(temp_buffer)} bytes")
                        audio_data = np.frombuffer(temp_buffer, dtype=np.float32)
                        segments = model.transcribe(audio_data)
                        for segment in segments:
                            if hasattr(segment, 'text'):
                                await websocket.send_json({"transcription": segment.text})
                        # Clear the original buffer safely after processing
                        audio_buffer = bytearray()
                    recording = False
                    logging.debug("Stopped recording and cleared buffer")

    except WebSocketDisconnect:
        logging.debug("WebSocket disconnected")

@router.post("/faster-whisper-mp3-file")
async def transcribe_audio(file: UploadFile = File(...)):
    if file.content_type != "audio/mpeg":
        raise HTTPException(status_code=400, detail="Invalid file type. Only MP3 files are supported.")

    #model_size = "large-v3"
    #model_size = "medium"
    model_size = "small"
    #model_size = "tiny"
    
    # model = WhisperModel(model_size, device="cuda", compute_type="float16")

    # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    with open("temp_audio.mp3", "wb") as temp_file:
        temp_file.write(await file.read())

    segments, info = model.transcribe("temp_audio.mp3", beam_size=5)
    transcription = [{"start": segment.start, "end": segment.end, "text": segment.text} for segment in segments]

    return {
        "language": info.language,
        "language_probability": info.language_probability,
        "transcription": transcription
    }
