import subprocess
import os
from dotenv import load_dotenv
from transformers import pipeline
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class AudioService:
    def __init__(self):
        self.whisper_pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-large-v3",
            device="cuda" if os.getenv("USE_CUDA", "false").lower() == "true" else "cpu"
        )
        self._verify_ffmpeg()

    def _verify_ffmpeg(self):
        try:
            subprocess.run(["ffmpeg", "-version"], 
                         check=True, 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error("FFmpeg is not installed or not in PATH")
            raise RuntimeError("FFmpeg is required for audio extraction") from e

    def extract_audio(self, video_path: str, audio_path: str) -> bool:
        try:
            os.makedirs(os.path.dirname(audio_path) or ".", exist_ok=True)
            
            command = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-vn", 
                "-acodec", "pcm_s16le",
                "-ar", "16000", 
                "-ac", "1", 
                "-loglevel", "error", 
                audio_path
            ]
            
            result = subprocess.run(command, 
                                  check=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
            
            if not os.path.exists(audio_path):
                logger.error(f"Audio extraction failed - no output file at {audio_path}")
                return False
                
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Audio extraction failed: {e.stderr.decode()}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during audio extraction: {str(e)}")
            return False

    def transcribe_audio(self, audio_path: str) -> Optional[str]:
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return None
            
        try:
            file_size = os.path.getsize(audio_path) / (1024 * 1024)  
            if file_size > 50:  
                logger.warning(f"Large audio file ({file_size:.2f}MB) may cause memory issues")
            
            result = self.whisper_pipe(audio_path)
            
            if not result or "text" not in result:
                logger.error("Unexpected response format from Whisper")
                return None
                
            return result["text"].strip()
            
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            return None

audio_service = AudioService()

def extract_audio(video_path: str, audio_path: str) -> bool:
    return audio_service.extract_audio(video_path, audio_path)

def transcribe_audio(audio_path: str) -> Optional[str]:
    return audio_service.transcribe_audio(audio_path)