from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os

import modules.logger_tool as logger
os.environ['LOG_NAME'] = 'app'
os.environ['LOG_DIR'] = 'logs'
os.environ['LOG_LEVEL'] = 'DEBUG'

logging = logger.get_logger(os.environ['LOG_NAME'], log_level=os.environ['LOG_LEVEL'], log_path=os.environ['LOG_DIR'], log_file=os.environ['LOG_NAME'])

from routers.database import admin, schools, calendar, timetable, curriculum, department, teacher, student
from routers.transcribe import whisper_live, utterance
from routers.llm import ollama, openai
from routers.connections.arbor_router import router as arbor_router

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, Request, BackgroundTasks, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9500", "http://localhost:9500", "http://192.168.0.20:9500", "ws://localhost:9500", "ws://192.168.0.20:9500", "http://localhost:9501", "http://192.168.0.20:9501", "ws://localhost:9501", "ws://192.168.0.20:9501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Get the absolute path to the fastapi_frontend directory
frontend_directory = os.path.join(os.path.dirname(__file__), 'frontend')

app.mount("/static", StaticFiles(directory=os.path.join(frontend_directory, 'static')), name="static")
templates = Jinja2Templates(directory=os.path.join(frontend_directory, 'templates'))

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
app.include_router(whisper_live.router, prefix="/transcribe/live", tags=["Transcription"])
app.include_router(utterance.router, prefix="/transcribe/utterance", tags=["Utterance"])

# LLM Routes
app.include_router(ollama.router, prefix="/llm", tags=["LLM"])
app.include_router(openai.router, prefix="/llm", tags=["LLM"])

# Arbor Data Routes
app.include_router(arbor_router, prefix="/arbor", tags=["Arbor Data"])

# Add WebSocket route
@app.websocket("/transcribe/live/ws/transcriptions")
async def websocket_endpoint(websocket: WebSocket):
    await whisper_live.websocket_endpoint(websocket)

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/transcription", response_class=HTMLResponse)
async def get_transcription(request: Request):
    backend_url = os.getenv("BACKEND_URL", "localhost")
    backend_port = os.getenv("BACKEND_PORT", "9500")
    return templates.TemplateResponse("transcription.html", {"request": request, "backend_url": backend_url, "backend_port": backend_port})
