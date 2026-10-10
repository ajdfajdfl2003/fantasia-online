@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PY=
where py >nul 2>nul && set PY=py -3
if not defined PY if exist "%LOCALAPPDATA%\Programs\Python\Python38\python.exe" set PY="%LOCALAPPDATA%\Programs\Python\Python38\python.exe"
if not defined PY set PY=python
start "" cmd /c "timeout /t 2 >nul & start http://localhost:8000"
%PY% server.py
pause
