from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from faster_whisper import WhisperModel

router = APIRouter()

@router.post("/faster-whisper")
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
    