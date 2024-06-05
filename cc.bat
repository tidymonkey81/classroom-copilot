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
echo 1b: Instantiate backend and Neo4j
echo 1c: Instantiate only backend
echo 1d: Instantiate only Neo4j
echo 1e: Rebuild and instantiate all containers
echo 1f: Rebuild and instantiate backend and Neo4j containers
echo 1g: Rebuild and instantiate only backend container
echo R: Return to main menu
echo.
set /p choice="Select a Docker option: "

if "%choice%"=="1a" (
    docker-compose up
    goto docker_menu
)
if "%choice%"=="1b" (
    docker-compose up cc_backend cc_neo4j
    goto docker_menu
)
if "%choice%"=="1c" (
    docker-compose up cc_backend
    goto docker_menu
)
if "%choice%"=="1d" (
    docker-compose up cc_neo4j
    goto docker_menu
)
if "%choice%"=="1e" (
    docker-compose up --build
    goto docker_menu
)
if "%choice%"=="1f" (
    docker-compose up --build cc_backend cc_neo4j
    goto docker_menu
)
if "%choice%"=="1g" (
    docker-compose up --build cc_backend
    goto docker_menu
)
if /i "%choice%"=="R" goto menu

echo Invalid Docker option, please select a valid sub-option or R to return.
pause
goto docker_menu

:host_menu
cls
echo ===== Run on Host Machine =====
echo 2a: Run frontend and backend
echo 2b: Run only frontend
echo 2c: Run only backend
echo R: Return to main menu
echo.
set /p choice="Select a host option: "

if "%choice%"=="2a" (
    start cmd /k "cd frontend && npm run dev"
    start cmd /k "cd backend && conda activate cc && uvicorn app.main:app --host 0.0.0.0 --port 8000"
    goto host_menu
)
if "%choice%"=="2b" (
    start cmd /k "cd frontend && npm run dev"
    goto host_menu
)
if "%choice%"=="2c" (
    start cmd /k "cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000"
    goto host_menu
)
if /i "%choice%"=="R" goto menu

echo Invalid host option, please select a valid sub-option or R to return.
pause
goto host_menu