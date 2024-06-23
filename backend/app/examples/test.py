from modules.whisper_live.client import TranscriptionClient
import os
import time

import queue

from dotenv import load_dotenv
load_dotenv()

host = os.environ["WHISPERLIVE_HOST"]
port = os.environ["WHISPERLIVE_PORT"]

def setup_directories(user_dir, user_id):
    user_transcript_dir = f"{user_dir}/{user_id}/transcripts"
    if not os.path.exists(user_transcript_dir):
        os.makedirs(user_transcript_dir)
    return user_transcript_dir

def eos_sensitive_callback(text, start, end, is_final):
    if is_final:
        print(f"Utterance: {text} (start: {start}, end: {end})")

def main():
    user_dir = "../../data/users"
    user_id = "kcar"
    user_transcript_dir = setup_directories(user_dir, user_id)

    transcription_queue = queue.Queue()
    client = TranscriptionClient(
        host,
        port,
        lang="en",
        translate=False,
        use_vad=True,
        save_output_recording=True,
        output_recording_filename=f"{user_transcript_dir}/output_recording.wav",
        output_transcription_path=f"{user_transcript_dir}/output.srt",
        callback=eos_sensitive_callback  # Set the callback here
    )

    client()

if __name__ == "__main__":
    main()
