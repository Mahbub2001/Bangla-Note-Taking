import os
from moviepy import VideoFileClip
from services.video_service import split_video
from services.audio_service import extract_audio, transcribe_audio
from services.image_service import extract_frame, analyze_image
from services.text_service import summarize_segment
from services.pdf_service import text_to_pdf
import time
import subprocess

def process_video_locally(video_path):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found at {video_path}")

    segments = split_video(video_path)
    segment_summaries = []
    total_segments = len(segments[:3])
    for i,seg_path in enumerate(segments[:3]):
        try:
            audio_path = seg_path.replace(".mp4", ".wav")
            extract_audio(seg_path, audio_path)
            transcript = transcribe_audio(audio_path)
            
            with VideoFileClip(seg_path) as clip:
                frame_time = clip.duration / 2
                frame_path = seg_path.replace(".mp4", ".jpg")
                extract_frame(seg_path, frame_time, frame_path)
                image_desc = analyze_image(frame_path)
                
            position = (
                "start" if i == 0 else
                "end" if i == total_segments - 1 else
                "middle"
            )
            
            summary = summarize_segment(transcript, image_desc,position)
            print(f"Summary for segment {os.path.basename(seg_path)}:\n{summary}\n")
            segment_summaries.append(summary)
            
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
    
    if segment_summaries:
        output_pdf = video_path.replace(".mp4", "_summary.pdf")
        full_summary = "\n\n".join(segment_summaries)
        with open("output.txt", "w", encoding="utf-8") as text_file:
            text_file.write(full_summary)

        # text_to_pdf(full_summary, output_pdf)
        # print(f"PDF generated successfully at {output_pdf}")

if __name__ == "__main__":
    video_file = "physics.mp4"
    process_video_locally(video_file)