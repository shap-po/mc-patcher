@echo off

pushd %~dp0
setlocal

call .venv\Scripts\activate
.venv\Scripts\python.exe main.py %*
