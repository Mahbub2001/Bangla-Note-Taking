# main.py
from fastapi import FastAPI
from routers.notes import router as notes_router

app = FastAPI(title="Video Lecture Summarizer API")
app.include_router(notes_router, prefix="/api")
