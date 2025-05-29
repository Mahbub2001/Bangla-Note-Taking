import os
from moviepy import VideoFileClip
from services.video_service import split_video
from services.audio_service import extract_audio, transcribe_audio
from services.image_service import extract_frame, analyze_image
from services.text_service import summarize_segment, merge_summaries
from services.pdf_service import text_to_pdf
import time
import subprocess

def process_video_locally(video_path):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found at {video_path}")

    segments = split_video(video_path)
    segment_summaries = []
    
    for seg_path in segments[:4]:
    # for seg_path in segments:
        try:
            audio_path = seg_path.replace(".mp4", ".wav")
            extract_audio(seg_path, audio_path)
            transcript = transcribe_audio(audio_path)
            
            with VideoFileClip(seg_path) as clip:
                frame_time = clip.duration / 2
                frame_path = seg_path.replace(".mp4", ".jpg")
                extract_frame(seg_path, frame_time, frame_path)
                image_desc = analyze_image(frame_path)
            
            summary = summarize_segment(transcript, image_desc)
            print(f"Summary for segment {os.path.basename(seg_path)}:\n{summary}\n")
            segment_summaries.append(summary)
            with open(f"temp_summary_{os.path.basename(seg_path)}.txt", "w", encoding="utf-8") as f:
                f.write(summary)
            
        finally:
            if os.path.exists(seg_path):
                for _ in range(3):  
                    try:
                        os.remove(seg_path)
                        break
                    except PermissionError:
                        time.sleep(0.1)
            if os.path.exists(audio_path):
                os.remove(audio_path)
            if os.path.exists(frame_path):
                os.remove(frame_path)

    # final_notes = merge_summaries(segment_summaries)
    # pdf_path = f"output_notes/notes_{os.path.basename(video_path)}.pdf"
    # os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    # text_to_pdf(final_notes, pdf_path)
    
    # print(f"Processing complete! PDF saved to: {pdf_path}")

if __name__ == "__main__":
    video_file = "physics.mp4"
    process_video_locally(video_file)