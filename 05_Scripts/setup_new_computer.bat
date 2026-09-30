@echo off
TITLE Jarvis Starter Pack - Automatic Setup & Launch (Windows)
chcp 65001 >nul

echo ===================================================
echo   Jarvis Starter Pack Automatic Setup & Launch
echo ===================================================
echo.

:: 1. Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

:: 2. Create virtual environment if not present
if not exist "venv" (
    echo [1/3] Creating Python Virtual Environment (venv)...
    python -m venv venv
) else (
    echo [1/3] Virtual environment (venv) already exists.
)

:: 3. Activate venv & Install requirements
echo [2/3] Activating Virtual Environment and Installing Dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ===================================================
echo   Setup Completed Successfully!
echo ===================================================
echo.
echo Select Execution Mode:
echo [1] Desktop GUI App (PyWebView Standalone)
echo [2] Visual HUD Web Server (Web Browser)
echo [3] Voice Runner (Voice Assistant)
echo [4] Vision Runner (Camera / Vision Assistant)
echo [5] Exit
echo.

set /p mode="Enter choice [1-5]: "

if "%mode%"=="1" (
    echo Launching Desktop GUI App...
    python 01_Modules\Jarvis_Desktop_App_Starter\jarvis_app.py
) else if "%mode%"=="2" (
    echo Launching Visual HUD Web Server...
    python 01_Modules\Jarvis_Visual_HUD_Starter\main.py
) else if "%mode%"=="3" (
    echo Launching Voice Runner...
    python 01_Modules\Jarvis_Voice_Starter\voice_runner.py
) else if "%mode%"=="4" (
    echo Launching Vision Runner...
    python 01_Modules\Jarvis_Vision_Starter\vision_runner.py
) else (
    echo Exiting...
)

pause
