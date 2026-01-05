@echo off
REM Start CRE Parser Application
echo Starting Commercial Real Estate Document Parser...
echo.
echo Opening application at http://localhost:5000
timeout /t 2
start http://localhost:5000
echo.
python run.py
