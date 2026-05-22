@echo off
setlocal
cd /d "%~dp0\.."
python -m pytest %*
