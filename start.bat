@echo off
title AI-Adaptive Onboarding Engine - Startup

echo.
echo  ==========================================
echo   AI-Adaptive Onboarding Engine
echo  ==========================================
echo.

:: Check if Ollama is running
echo [1/3] Checking Ollama...
curl -s http://localhost:11434 >nul 2>&1
if %errorlevel% neq 0 (
    echo  Starting Ollama...
    start "" ollama serve
    timeout /t 4 /nobreak >nul
) else (
    echo  Ollama already running.
)

:: Pull model if not present
echo [2/3] Ensuring llama3.2 model is available...
ollama pull llama3.2 >nul 2>&1

:: Start backend
echo [3/3] Starting backend...
cd backend
start "AI-Adaptive Onboarding Engine" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload"
cd ..

:: Wait for backend to be ready
echo.
echo  Waiting for backend to start...
timeout /t 3 /nobreak >nul

:: Open browser
echo  Opening AI-Adaptive Onboarding Engine in browser...
start http://localhost:8001

echo.
echo  ==========================================
echo   App is running!
echo   Local:   http://localhost:8001
echo  ==========================================
echo.
echo  To share with others, run: ngrok http 8001
echo  (Install ngrok free at https://ngrok.com)
echo.
pause
