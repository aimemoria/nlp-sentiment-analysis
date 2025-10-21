@echo off
echo ====================================
echo Starting Frontend (React)
echo ====================================
echo.

cd frontend

echo Installing Node.js dependencies...
echo This may take a few minutes on first run...
echo.
call npm install
echo.

echo Starting React development server...
echo Browser will open automatically at http://localhost:3000
echo.
call npm start

pause
