from modules.WhisperLive.whisper_live.client import TranscriptionClient
import os
import time
import subprocess
from functools import partial

def sample_callback(client, text, is_final):
    global last_text

    if is_final and text != last_text:
        print("\r" + text[-1], end='', flush=True)
        last_text = text
        #client.paused = True
        # Define the command to be run
        #command = f'echo "{text[-1]}" | piper --model en_US-lessac-medium --output-raw | aplay -r 22050 -f S16_LE -t raw -'
        # Run the command
        #subprocess.run(command, shell=True, check=True)

        #client.paused = False
    else:
        os.system("cls" if os.name == "nt" else "clear")
        print(text[-1], end='', flush=True)

last_text = ""

def setup_directories(user_dir, user_id):
    user_transcript_dir = f"{user_dir}/{user_id}/transcripts"
    if not os.path.exists(user_transcript_dir):
        os.makedirs(user_transcript_dir)
    return user_transcript_dir

def main():
    user_dir = "../../data/users"
    user_id = "kcar"
    user_transcript_dir = setup_directories(user_dir, user_id)

    def create_client():
        client = TranscriptionClient(
            "localhost",
            9090,
            lang="en",
            translate=False,
            model="tiny.en",
            use_vad=True,
            save_output_recording=True,
            output_recording_filename=f"{user_transcript_dir}/output_recording.wav",
            output_transcription_path=f"{user_transcript_dir}/output.srt"
        )
        client.callback = partial(sample_callback, client)
        return client

    client = create_client()
    client()

if __name__ == "__main__":
    main()
