from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from services.video_service import split_video
from services.audio_service import extract_audio, transcribe_audio
from services.image_service import extract_frame, analyze_image
from services.text_service import summarize_segment, merge_summaries
from services.pdf_service import text_to_pdf
import os
from moviepy import VideoFileClip
router = APIRouter()

@router.post("/notes/generate")
async def generate_notes(
    file: UploadFile = File(None), 
    path: str = None
):
    if file:
        video_filename = file.filename
        video_path = f"input_videos/{video_filename}"
        os.makedirs(os.path.dirname(video_path), exist_ok=True)
        with open(video_path, "wb") as f:
            f.write(await file.read())
    elif path:
        video_path = path
        if not os.path.exists(video_path):
            raise HTTPException(status_code=404, detail="File path not found")
    else:
        raise HTTPException(status_code=400, detail="No video provided")

    segments = split_video(video_path)
    segment_summaries = []
    for seg_path in segments:
        audio_path = seg_path.replace(".mp4", ".wav")
        extract_audio(seg_path, audio_path)
        transcript = transcribe_audio(audio_path)
        print(f"Transcription for {seg_path}: {transcript}")
        frame_time = VideoFileClip(seg_path).duration / 2
        frame_path = seg_path.replace(".mp4", ".jpg")
        extract_frame(seg_path, frame_time, frame_path)
        image_desc = analyze_image(frame_path)
        summary = summarize_segment(transcript, image_desc)
        segment_summaries.append(summary)
        os.remove(seg_path)
        os.remove(audio_path)
        os.remove(frame_path)

    final_notes = merge_summaries(segment_summaries)
    pdf_path = f"output_notes/notes_{os.path.basename(video_path)}.pdf"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    text_to_pdf(final_notes, pdf_path)

    return FileResponse(pdf_path, media_type="application/pdf", filename="class_notes.pdf")
