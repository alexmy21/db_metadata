@echo off
echo ====================================
echo SQLite Metadata Viewer - Frontend Setup
echo ====================================
echo.

echo [1/2] Installing dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Please ensure Node.js 16+ is installed
    pause
    exit /b 1
)

echo [2/2] Setup complete!
echo.
echo ====================================
echo Frontend setup completed successfully!
echo ====================================
echo.
echo To start the frontend server, run:
echo   start-frontend.bat
echo.
pause
