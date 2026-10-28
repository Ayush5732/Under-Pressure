@echo off
cd /d "%~dp0"
py -3 server.py
if errorlevel 1 (
  echo If Python was not found, install Python 3 from python.org and try again.
  pause
)
