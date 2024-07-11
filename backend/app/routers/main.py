from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
import modules.logger_tool as logger
log_name = 'api_main_fastapi'
user_profile = os.environ.get("USERPROFILE", "")
app_dir = os.environ.get("APP_DIR", "")
log_dir = os.path.join(user_profile, app_dir, "logs")
log_level = 'DEBUG'
logging = logger.get_logger(
    name=log_name,
    log_level=log_level,
    log_path=log_dir,
    log_file=log_name,
    runtime=True,
    log_format='default'
)

from routers.dev.tests import timetable_test
from routers.database import admin, schools, department, teacher, student
from routers.database.init import get_data, calendar, timetable, curriculum
from routers.transcribe import whisper_live, utterance
from routers.llm.private.ollama import ollama
from routers.llm.public.openai import openai
from routers.connections.arbor_router import router as arbor_router
from routers.langchain.graph_qa import router as graph_qa_router

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, Request, WebSocket
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

# Frontend setup
frontend_directory = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app.mount("/static", StaticFiles(directory=os.path.join(frontend_directory, 'static')), name="static")
templates = Jinja2Templates(directory=os.path.join(frontend_directory, 'templates'))

## Database Routes
# Admin routes
app.include_router(admin.router, prefix="/database/admin", tags=["Admin"])

# Test routes
app.include_router(timetable_test.router, prefix="/tests", tags=["Tests"])

# Upload routes
app.include_router(get_data.router, prefix="/database/upload", tags=["Upload"])

# School routes
app.include_router(schools.router, prefix="/database/schools", tags=["School"])

# Schedule routes
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
app.include_router(ollama.router, prefix="/llm/private/ollama", tags=["LLM"])
app.include_router(openai.router, prefix="/llm/public/openai", tags=["LLM"])

# Langchain routes
app.include_router(graph_qa_router, prefix="/langchain/graph_qa", tags=["Langchain"])

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