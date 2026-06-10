@echo off
chcp 65001 >nul
cd /d %~dp0
echo 正在强制释放 8081 端口...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8081 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
timeout /t 1 /nobreak >nul
echo 启动机器人...
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
)
python bot.py
pause
