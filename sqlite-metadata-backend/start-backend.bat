@echo off
echo ====================================
echo Starting SQLite Metadata Backend...
echo ====================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo Starting FastAPI server on http://localhost:5000
echo.
echo API Documentation: http://localhost:5000/docs
echo Health Check: http://localhost:5000/health
echo.
echo Press Ctrl+C to stop the server
echo.

python run.py
