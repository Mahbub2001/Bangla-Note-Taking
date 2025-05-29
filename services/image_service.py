from PIL import Image
import base64
import os
from moviepy import VideoFileClip
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_frame(video_path: str, time: float, frame_path: str) -> None:
    with VideoFileClip(video_path) as clip:
        frame = clip.get_frame(time)
        image = Image.fromarray(frame)
        image.save(frame_path)

def analyze_image(frame_path: str) -> str:
    with open(frame_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    messages = [
        {
            "role": "system",
            "content": "You are an educational assistant analyzing lecture visuals. "
                       "Describe any diagrams, slides, or classroom visuals in detail in bengali language."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Describe this lecture image focusing on educational content:"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
    
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=0.9
        )
        return completion.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Image analysis failed: {str(e)}")
        return "Visual content description unavailable"

















# from PIL import Image
# import io
# import numpy as np
# from moviepy import VideoFileClip
# from openai import OpenAI
# import base64
# import os
# from dotenv import load_dotenv
# load_dotenv()  
# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=os.getenv("OPENROUTER_API_KEY"),  
# )

# def extract_frame(video_path: str, time: float, frame_path: str) -> None:
#     """
#     Extract a frame at given time (seconds) from the video.
#     """
#     clip = VideoFileClip(video_path)
#     frame = clip.get_frame(time)  
#     image = Image.fromarray(frame)
#     image.save(frame_path)
#     clip.close()

# def analyze_image(frame_path: str) -> str:
#     """
#     Send image to a vision-capable LLM via OpenRouter API to get descriptive context.
#     """
#     with open(frame_path, "rb") as image_file:
#         base64_image = base64.b64encode(image_file.read()).decode('utf-8')
#         messages = [
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "Describe the content of this image in the context of a classroom lecture."
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/jpeg;base64,{base64_image}"
#                     }
#                 }
#             ]
#         }
#     ]
    
#     completion = client.chat.completions.create(
#         extra_headers={
#             "HTTP-Referer": "<YOUR_SITE_URL>", 
#             "X-Title": "<YOUR_SITE_NAME>",     
#         },
#         model="google/gemma-3-27b-it:free", 
#         messages=messages,
#         temperature=0.7
#     )
    
#     description = completion.choices[0].message.content
#     return description.strip()