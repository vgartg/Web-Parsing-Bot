@echo off
setlocal
cd /d "%~dp0\.."
python -m web_parsing_bot %*
