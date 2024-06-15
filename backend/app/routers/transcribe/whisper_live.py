from fastapi import APIRouter, BackgroundTasks, WebSocket
# from ...modules.WhisperLive.run_server import TranscriptionServer
# from ...modules.WhisperLive.whisper_live import client
import os
import time

router = APIRouter()

user_dir = "data_local/users"
user_id = "kcar"
user_transcript_dir = f"{user_dir}/{user_id}/transcripts"
if not os.path.exists(user_transcript_dir):
    os.makedirs(user_transcript_dir)

    
@router.websocket("/whisper-live-audio-stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    transcription_client = client.TranscriptionClient(
        websocket=websocket,  # Ensure this is a WebSocket instance
        host="localhost",
        port=9090,
        lang="en",
        translate=False,
        use_vad=True,
        save_output_recording=True,
        output_recording_filename=f"{user_transcript_dir}/output_recording.wav",
        output_transcription_path=f"{user_transcript_dir}/output.srt"
    )
    await transcription_client.handle_connection()  # Adjusted method to handle the connection
    await websocket.close()

