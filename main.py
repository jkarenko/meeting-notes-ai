from fastapi import FastAPI, UploadFile, File, Request
import shutil
from fastapi.templating import Jinja2Templates
from os import getenv
from meeting_notes_ai.media_handler import MediaHandler

templates = Jinja2Templates(directory="templates")

app = FastAPI(
    root_path=getenv("ROOT_PATH", "http://127.0.0.1:8000"),
)
media_handler = MediaHandler()


@app.post("/extract_audio")
def extract_audio(input: str, output: str):
    return media_handler.extract_audio(input, output)


@app.post("/compress_audio")
def compress_audio(input: str, output: str):
    return media_handler.compress_audio(input, output)


@app.post("/speech_to_text")
def speech_to_text(audio_path: str):
    return media_handler.speech_to_text(audio_path)


@app.post("/meeting_minutes")
def meeting_minutes(transcription: str):
    return media_handler.meeting_minutes(transcription)


@app.post("/audio_to_minutes")
async def audio_to_minutes(request: Request, file: UploadFile = File(...)):
    with open(f"{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    meeting_summary = media_handler.audio_to_minutes(file.filename)
    print(meeting_summary)
    import json
    with open('meeting_summary.json', 'w') as json_file:
        json.dump(meeting_summary, json_file)
    return templates.TemplateResponse("meeting_summary.html", {"request": request, "meeting_summary": meeting_summary})


@app.get("/")
def ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
