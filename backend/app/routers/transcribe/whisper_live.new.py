from fastapi import APIRouter, BackgroundTasks, WebSocket, WebSocketDisconnect
from modules.whisper_live.client import TranscriptionClient
import os
import asyncio
import queue
from dotenv import load_dotenv
from typing import List

import logging

load_dotenv()

router = APIRouter()

host = os.environ["WHISPERLIVE_HOST"]
port = os.environ["WHISPERLIVE_PORT"]

active_websockets: List[WebSocket] = []

def setup_directories(user_dir, user_id):
    user_transcript_dir = f"{user_dir}/{user_id}/transcripts"
    if not os.path.exists(user_transcript_dir):
        os.makedirs(user_transcript_dir)
    return user_transcript_dir

async def eos_sensitive_callback(text, start, end, is_final):
    if is_final:
        message = {
            "utterance": text,
            "start": start,
            "end": end,
            "eos": is_final
        }
        logging.info(f"Sending message: {message}")  # Debug print
        for websocket in active_websockets:
            try:
                await websocket.send_json(message)
                logging.info("Message sent successfully")  # Debug print
            except WebSocketDisconnect:
                active_websockets.remove(websocket)
                logging.info("WebSocket disconnected")  # Debug print

def run_transcription_client(user_id: str):
    user_dir = "../../data/users"
    user_transcript_dir = setup_directories(user_dir, user_id)

    transcription_queue = queue.Queue()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def callback_wrapper(*args):
        await eos_sensitive_callback(*args)

    client = TranscriptionClient(
        host,
        port,
        lang="en",
        translate=False,
        use_vad=True,
        save_output_recording=True,
        output_recording_filename=f"{user_transcript_dir}/output_recording.wav",
        output_transcription_path=f"{user_transcript_dir}/output.srt",
        callback=callback_wrapper,  # Use the async wrapper
        loop=loop  # Pass the event loop
    )

    client()
    loop.run_forever()

@router.post("/start_transcription/{user_id}")
async def start_transcription(user_id: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_transcription_client, user_id)
    return {"message": "Transcription started", "user_id": user_id}

@router.websocket("/ws/transcriptions")
async def websocket_endpoint(websocket: WebSocket):
    logging.info("WebSocket accessed")  # Debug print
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            logging.info(f"Received message: {message}")  # Debug print
            for ws in active_websockets:
                await ws.send_text(message)
    except WebSocketDisconnect:
        active_websockets.remove(websocket)
        logging.info("WebSocket disconnected")  # Debug print
