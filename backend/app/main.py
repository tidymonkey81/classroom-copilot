import os
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from .routers.database import calendar, curriculum, timetable, school, admin
from .routers.transcribe import whisper
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(find_dotenv())

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:8001", "http://localhost:8000", "bolt://localhost:7687", "http://localhost:7688", "http://localhost:7474", "http://127.0.0.1:8001", "http://127.0.0.1:8000", "bolt://127.0.0.1:7687", "http://127.0.0.1:7688", "http://127.0.0.1:7474", "http://cc_frontend:8001", "http://cc_backend:8000", "bolt://cc_neo4j:7687", "http://cc_neo4j:7688", "http://cc_neo4j:7474"],  # Include frontend, backend and neo4j origins
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router, prefix="/database/admin", tags=["Admin"])
app.include_router(calendar.router, prefix="/database/calendar", tags=["Calendar"])
app.include_router(school.router, prefix="/database/school", tags=["School"])
app.include_router(timetable.router, prefix="/database/timetable", tags=["Timetable"])
app.include_router(curriculum.router, prefix="/database/curriculum", tags=["Curriculum"])

app.include_router(whisper.router, prefix="/transcribe/local/whisper", tags=["Whisper"])
