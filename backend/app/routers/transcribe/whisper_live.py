from fastapi import APIRouter, BackgroundTasks, WebSocket
from ...modules.whisperlive_client_new import client
import os
import time

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
    transcription_client = client.TranscriptionClient(
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


from fastapi import APIRouter, WebSocket
from modules.whisperlive_client_new import Client as TranscriptionClient

router = APIRouter()

@router.websocket("/whisper-live-audio-stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # Assuming the server details and other configurations are set as environment variables or similar
        client = TranscriptionClient(
            ws=websocket,
            host="localhost",  # Backend server host
            port=9090,         # Backend server port
            lang="en",
            translate=False,
            use_vad=True,
            model="small",
            srt_file_path="path_to_srt_file.srt"  # Update with actual path
        )
        await client.handle_connection()  # This method should be implemented to manage the connection lifecycle
    finally:
        await websocket.close()
