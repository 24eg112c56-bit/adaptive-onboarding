@echo off
echo ========================================
echo     SkillPath AI - Starting...
echo ========================================

echo [1/2] Starting Ollama...
start "" "C:\Users\Purna chander\AppData\Local\Programs\Ollama\ollama.exe" serve

timeout /t 3 /nobreak >nul

echo [2/2] Starting SkillPath AI server...
cd backend
start "" /B python -m uvicorn main:app --port 8001

timeout /t 3 /nobreak >nul

echo ========================================
echo  SkillPath AI is running!
echo  Opening browser...
echo ========================================

start "" "http://127.0.0.1:8001"
