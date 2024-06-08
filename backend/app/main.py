import os
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from .routers.database import calendar, curriculum, timetable, school, admin
from .routers.transcribe import faster_whisper
from .routers.llm import ollama, openai
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(find_dotenv())

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router, prefix="/database/admin", tags=["Admin"])
app.include_router(calendar.router, prefix="/database/calendar", tags=["Calendar"])
app.include_router(school.router, prefix="/database/school", tags=["School"])
app.include_router(timetable.router, prefix="/database/timetable", tags=["Timetable"])
app.include_router(curriculum.router, prefix="/database/curriculum", tags=["Curriculum"])
app.include_router(faster_whisper.router, prefix="/transcribe/local", tags=["Transcription"])
app.include_router(ollama.router, prefix="/llm", tags=["LLM"])
app.include_router(openai.router, prefix="/llm", tags=["LLM"])
