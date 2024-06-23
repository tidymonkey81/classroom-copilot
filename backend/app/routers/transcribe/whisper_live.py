from fastapi import APIRouter, WebSocket
from modules.whisper_live.client import Client
import os

router = APIRouter()

def setup_directories(user_dir, user_id):
    user_transcript_dir = f"{user_dir}/{user_id}/transcripts"
    if not os.path.exists(user_transcript_dir):
        os.makedirs(user_transcript_dir)
    return user_transcript_dir

    
@router.websocket("/whisper-live-audio-stream")
async def websocket_endpoint(websocket: WebSocket):
    user_dir = "../../data/users"
    user_id = "kcar"
    user_transcript_dir = setup_directories(user_dir, user_id)
    
    await websocket.accept()
    transcription_client = Client.TranscriptionClient(
        websocket=websocket,
        lang="en",
        translate=False,
        use_vad=True,
        save_output_recording=True,
        output_recording_filename=f"{user_transcript_dir}/output_recording.wav",
        output_transcription_path=f"{user_transcript_dir}/output.srt"
    )
    await transcription_client.handle_connection()  # Adjusted method to handle the connection
    await websocket.close()
