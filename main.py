from os import getenv
from fastapi import FastAPI
from meeting_notes_ai.media_handler import MediaHandler

app = FastAPI(
    root_path=getenv("ROOT_PATH", "http://localhost:8000"),
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
