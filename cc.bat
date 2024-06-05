@echo off
setlocal

:: Load environment variables from .env file
for /f "delims=" %%a in (.env) do set "%%a"

:menu
cls
echo ================== Select an option: ==================
echo 1: Instantiate all containers using docker-compose
echo 2: Instantiate backend and Neo4j using docker-compose
echo 3: Instantiate only backend using docker-compose
echo 4: Run frontend and backend directly on host machine
echo 5: Run only frontend on host machine
echo 6: Run only backend on host machine
echo 7: Rebuild and instantiate all containers
echo 8: Rebuild and instantiate backend and Neo4j containers
echo 9: Rebuild and instantiate only backend container
echo Q: Quit
echo.
set /p choice="Please make a selection: "

if "%choice%"=="1" (
    docker-compose up
    goto menu
)
if "%choice%"=="2" (
    docker-compose up cc_backend cc_neo4j
    goto menu
)
if "%choice%"=="3" (
    docker-compose up cc_backend
    goto menu
)
if "%choice%"=="4" (
    start cmd /k "cd frontend && npm run dev"
    start cmd /k "cd backend && conda activate cc && uvicorn app.main:app --host 0.0.0.0 --port 8000"
    goto menu
)
if "%choice%"=="5" (
    start cmd /k "cd frontend && npm run dev"
    goto menu
)
if "%choice%"=="6" (
    start cmd /k "cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000"
    goto menu
)
if "%choice%"=="7" (
    docker-compose up --build
    goto menu
)
if "%choice%"=="8" (
    docker-compose up --build cc_backend cc_neo4j
    goto menu
)
if "%choice%"=="9" (
    docker-compose up --build cc_backend
    goto menu
)
if /i "%choice%"=="Q" (
    exit
)
echo Invalid option, please select a number from 1 to 9 or Q to quit.
pause
goto menu