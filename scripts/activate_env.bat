@echo off
cd /d %~dp0
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
) else (
    echo 未找到虚拟环境，请先执行 python -m venv venv
)
echo Virtual environment activated. You can now run pip or python.
cmd /k
