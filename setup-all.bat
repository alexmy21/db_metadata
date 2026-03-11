@echo off
echo ====================================
echo SQLite Metadata Viewer - Quick Setup
echo ====================================
echo.
echo This script will set up both backend and frontend
echo.
pause

echo.
echo ====================================
echo Setting up BACKEND...
echo ====================================
cd sqlite-metadata-backend
call setup.bat
cd ..

echo.
echo ====================================
echo Setting up FRONTEND...
echo ====================================
cd sqlite-metadata-frontend
call setup.bat
cd ..

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo To start the application:
echo   1. Open a terminal and run: cd sqlite-metadata-backend ^&^& start-backend.bat
echo   2. Open another terminal and run: cd sqlite-metadata-frontend ^&^& start-frontend.bat
echo   3. Open your browser to: http://localhost:5173
echo.
pause
