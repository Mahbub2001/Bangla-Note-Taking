from moviepy import VideoFileClip
import os

def split_video(
    video_path: str,
    segment_length: int = 30,
    overlap: int = 5,          
    output_dir: str = "temp_segments"
) -> list[str]:
    os.makedirs(output_dir, exist_ok=True)
    
    clip = VideoFileClip(video_path)
    duration = clip.duration
    segments = []
    segment_count = 1

    start = 0
    while start < duration:
        end = min(start + segment_length, duration)
        segment_file = os.path.join(output_dir, f"segment_{segment_count}.mp4")

        clip.subclipped(start, end).write_videofile(
            segment_file,
            codec="libx264",
            audio_codec="aac",
            threads=4,
            preset="fast"
        )

        segments.append(segment_file)
        segment_count += 1

        start += segment_length - overlap

    clip.close()
    return segments
