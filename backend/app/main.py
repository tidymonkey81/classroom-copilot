import os
import logging
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.database import admin, calendar, curriculum, timetable, schools, department, teacher, student
from .routers.transcribe import faster_whisper
from .routers.llm import ollama, openai

logging.basicConfig(level=logging.DEBUG)

load_dotenv(find_dotenv())

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9501", "http://192.168.0.20:9501", "ws://localhost:9501", "ws://192.168.0.20:9501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Database Routes
app.include_router(admin.router, prefix="/database/admin", tags=["Admin"])
app.include_router(schools.router, prefix="/database/schools", tags=["School"])
app.include_router(calendar.router, prefix="/database/calendar", tags=["Calendar"])
app.include_router(timetable.router, prefix="/database/timetable", tags=["Timetable"])
app.include_router(curriculum.router, prefix="/database/curriculum", tags=["Curriculum"])
app.include_router(department.router, prefix="/database/department", tags=["Department"])
app.include_router(teacher.router, prefix="/database/teacher", tags=["Teacher"])
app.include_router(student.router, prefix="/database/student", tags=["Student"])

# Transcription Routes
app.include_router(faster_whisper.router, prefix="/transcribe/local", tags=["Transcription"])

# LLM Routes
app.include_router(ollama.router, prefix="/llm", tags=["LLM"])
app.include_router(openai.router, prefix="/llm", tags=["LLM"])