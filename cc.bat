@echo off
setlocal

:: Load environment variables from .env file
for /f "delims=" %%a in (.env) do set "%%a"

:menu
cls
echo ================== Select an option: ==================
echo 1: Docker-compose options
echo 2: Run on host machine
echo Q: Quit
echo.
set /p choice="Please make a selection: "

if "%choice%"=="1" goto docker_menu
if "%choice%"=="2" goto host_menu
if /i "%choice%"=="Q" exit

echo Invalid option, please select a number from the list or Q to quit.
pause
goto menu

:docker_menu
cls
echo ===== Docker-compose Options =====
echo 1a: Instantiate all containers
echo 1b: Instantiate backend, Whisper, and Neo4j
echo 1c: Instantiate only frontend
echo 1d: Instantiate only backend
echo 1e: Instantiate only Whisper
echo 1f: Instantiate only Neo4j
echo 1g: Rebuild and instantiate all containers
echo 1h: Rebuild and instantiate only frontend container
echo 1i: Rebuild and instantiate only backend container
echo 1j: Rebuild and instantiate only Whisper container
echo 1k: Rebuild and instantiate only Neo4j container
echo R: Return to main menu
echo.
set /p choice="Select a Docker option: "

if "%choice%"=="1a" (
    docker-compose up
    goto docker_menu
)
if "%choice%"=="1b" (
    docker-compose up cc_backend cc_whisper cc_neo4j
    goto docker_menu
)
if "%choice%"=="1c" (
    docker-compose up cc_frontend
    goto docker_menu
)
if "%choice%"=="1d" (
    docker-compose up cc_backend
    goto docker_menu
)
if "%choice%"=="1e" (
    docker-compose up cc_whisper
    goto docker_menu
)
if "%choice%"=="1f" (
    docker-compose up cc_neo4j
    goto docker_menu
)
if "%choice%"=="1g" (
    docker-compose up --build
    goto docker_menu
)
if "%choice%"=="1h" (
    docker-compose up --build cc_frontend
    goto docker_menu
)
if "%choice%"=="1i" (
    docker-compose up --build cc_backend
    goto docker_menu
)
if "%choice%"=="1j" (
    docker-compose up --build cc_whisper
    goto docker_menu
)
if "%choice%"=="1k" (
    docker-compose up --build cc_neo4j
    goto docker_menu
)
if /i "%choice%"=="R" goto menu

echo Invalid Docker option, please select a valid sub-option or R to return.
pause
goto docker_menu

:host_menu
cls
echo ===== Run on Host Machine =====
echo 2a: Run frontend, backend and Whisper
echo 2b: Run only frontend
echo 2c: Run only backend
echo 2d: Run only Whisper
echo R: Return to main menu
echo.
set /p choice="Select a host option: "

if "%choice%"=="2a" (
    start cmd /k "cd frontend && npm run dev"
    start cmd /k "cd backend && conda activate cc && uvicorn app.main:app --host 0.0.0.0 --port 9500"
    start cmd /k "cd backend\app\modules\WhisperLive && conda activate cc && python3 run_server.py --port 9090 --backend faster_whisper"
    goto host_menu
)
if "%choice%"=="2b" (
    start cmd /k "cd frontend && npm run dev"
    goto host_menu
)
if "%choice%"=="2c" (
    start cmd /k "cd backend && uvicorn app.main:app --host 0.0.0.0 --port 9500"
    goto host_menu
)
if "%choice%"=="2d" (
    start cmd /k "cd backend\app\modules\WhisperLive && conda activate cc && python3 run_server.py --port 9090 --backend faster_whisper"
    goto host_menu
)
if /i "%choice%"=="R" goto menu

echo Invalid host option, please select a valid sub-option or R to return.
pause
goto host_menu