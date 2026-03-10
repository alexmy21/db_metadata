@echo off
echo ====================================
echo SQLite Metadata Viewer - Backend Setup
echo ====================================
echo.

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Please ensure Python 3.8+ is installed
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Creating sample database...
python app\utils\create_sample_db.py
if errorlevel 1 (
    echo ERROR: Failed to create sample database
    pause
    exit /b 1
)

echo [5/5] Setup complete!
echo.
echo ====================================
echo Backend setup completed successfully!
echo ====================================
echo.
echo To start the backend server, run:
echo   start-backend.bat
echo.
pause
