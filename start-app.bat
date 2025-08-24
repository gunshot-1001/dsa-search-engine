@echo off

start cmd /k "cd frontend && npm run dev"

REM Replace this with your actual path to uvicorn.exe
start cmd /k "C:\Users\Durvank\dsa-search-engine\venv\Scripts\uvicorn.exe app.main:app --reload"
