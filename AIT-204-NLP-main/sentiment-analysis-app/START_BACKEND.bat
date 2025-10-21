@echo off
echo ====================================
echo Starting Backend Server (Flask)
echo ====================================
echo.

cd backend

echo Installing Python dependencies...
pip install -r requirements.txt
echo.

echo Starting Flask server on http://localhost:5000
echo.
python app.py

pause
