@echo off
chcp 65001 >nul
title 花碎机器人 - 一键启动

:: 检查是否以管理员身份运行
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在请求管理员权限...
    powershell start -verb runas '%0' && exit
)

echo ========================================
echo  正在启动签名服务器、NapCat 和 NoneBot
echo ========================================

:: 请根据你的实际安装路径修改以下变量
set SIGN_DIR=D:\qqbot\Qsign
set NAPCAT_DIR=D:\qqbot\NapCat.Shell.Windows.OneKey\NapCat.44498.Shell
set BOT_DIR=%~dp0

:: 1. 启动签名服务器
if exist "%SIGN_DIR%\一键startAPI.bat" (
    echo [1/3] 启动签名服务器...
    start "Qsign" cmd /c "cd /d "%SIGN_DIR%" && 一键startAPI.bat"
) else (
    echo [警告] 签名服务器启动脚本不存在: %SIGN_DIR%\一键startAPI.bat
)

timeout /t 5 /nobreak >nul

:: 2. 启动 NapCat
if exist "%NAPCAT_DIR%\napcat.bat" (
    echo [2/3] 启动 NapCat...
    start "NapCat" cmd /c "cd /d "%NAPCAT_DIR%" && napcat.bat"
) else (
    echo [错误] 找不到 NapCat 启动脚本，请检查路径。
    pause
    exit /b 1
)

:: 等待二维码文件生成并自动打开文件夹
echo 等待二维码生成（约10秒）...
set QRCODE_DIR=%NAPCAT_DIR%\versions\9.9.26-44498\resources\app\napcat\cache
set QRCODE_PATH=%QRCODE_DIR%\qrcode.png

set /a TIMEOUT=20
:wait_qr
if not exist "%QRCODE_PATH%" (
    timeout /t 1 /nobreak >nul
    set /a TIMEOUT-=1
    if %TIMEOUT% gtr 0 goto wait_qr
)

if exist "%QRCODE_PATH%" (
    echo 二维码已生成，正在打开文件夹并选中图片...
    start explorer /select,"%QRCODE_PATH%"
) else (
    echo 未检测到二维码文件，请手动查看 NapCat 窗口或目录。
)

timeout /t 8 /nobreak >nul

:: 3. 启动 NoneBot2
if exist "%BOT_DIR%\start_bot.bat" (
    echo [3/3] 启动 NoneBot2...
    start "NoneBot" cmd /c "cd /d "%BOT_DIR%" && start_bot.bat"
) else (
    echo [错误] 找不到 NoneBot 启动脚本。
    pause
    exit /b 1
)

echo ========================================
echo  所有服务已启动，请检查各窗口是否正常。
echo  请勿关闭这些窗口！
echo ========================================
pause
