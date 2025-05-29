from openai import OpenAI
from typing import List
import os
from dotenv import load_dotenv
load_dotenv()  
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),  
)
def summarize_segment(transcript: str, image_desc: str) -> str:
    prompt = (
        f"Lecture transcript:\n{transcript}\n\n"
        f"Scene description:\n{image_desc}\n\n"
        "language should be in bengali\n\n"
        "Complete sentence if the transcript is unfinished"
        "Generate a the of the lecture segment that captures key concepts, examples, and formulas, explanation. "
        "Ensure the content is structured with bullet points or headings, and ends with two transitional sentences to connect to the next segment. "
    )
    
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  
            "X-Title": "<YOUR_SITE_NAME>",     
        },
        model="deepseek/deepseek-chat-v3-0324:free",  
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    summary = completion.choices[0].message.content
    return summary.strip()

def merge_summaries(summaries: List[str]) -> str:
    combined = "\n\n".join(f"Segment {i+1}: {s}" for i, s in enumerate(summaries))
    for i in range(len(summaries)):
        with open(f"temp_summary_{i+1}.txt", "w", encoding="utf-8") as f:
            f.write(summaries[i])
    prompt = (
        f"The following are summaries of sequential class segments:\n{combined}\n\n"
        "language should be in bengali\n\n"
        "Combine these into a single, coherent set of class notes, structured with bullet points or headings."
    )
    
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  
            "X-Title": "<YOUR_SITE_NAME>",      
        },
        model="deepseek/deepseek-chat-v3-0324:free",    
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    
    final_notes = completion.choices[0].message.content
    return final_notes.strip()













# from groq import Groq
# from typing import List
# import os
# import time
# from tenacity import retry, stop_after_attempt, wait_exponential
# from dotenv import load_dotenv
# import re

# load_dotenv()
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
# def groq_completion(messages: list, model: str = "deepseek-r1-distill-llama-70b") -> str:
#     """Safe wrapper for Groq API calls with retry logic"""
#     try:
#         response = client.chat.completions.create(
#             model=model,
#             messages=messages,
#             temperature=0.5,
#             max_tokens=1024,
#             top_p=0.9
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         if "rate limit" in str(e).lower():
#             time.sleep(15)  
#         raise

# def summarize_segment(transcript: str, image_desc: str) -> str:
#     """
#     Generate concise summary with focus on continuity
#     """
#     prompt = (
#         "As a lecture note assistant, create a note that:\n"
#         "1. Captures key concepts,examples,formula all the important things\n"
#         "2. Ends with 2 transitional sentences\n"
#         "3. Maintains academic tone\n\n"
#         "4. Language should be in bengali\n\n"
#         "5. If the transcript unfinished, then filled with your own words\n\n"
#         "6. Write as book notes, not a script.Combines the transcript and visual context for better note taking. Dont use this type: '**' \n\n"
#         f"Transcript:\n{transcript}\n\n" 
#         f"Visual Context:\n{image_desc}\n\n"
#         "Summary with ending transitions:"
#     )
    
#     # return groq_completion([
#     #     {"role": "system", "content": "You are an academic note-taking assistant like a student"},
#     #     {"role": "user", "content": prompt}
#     # ])
#     response = groq_completion([
#         {"role": "system", "content": "You are an academic note-taking assistant like a student"},
#         {"role": "user", "content": prompt}
#     ])
#     # Remove any `<think>` blocks if present
#     cleaned_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
#     return cleaned_response


# def merge_summaries(summaries: List[str]) -> str:
#     """
#     Build notes incrementally using context-carrying technique
#     """
#     if not summaries:
#         return "No content available"
#     combined = summaries[0]
    
#     for i, segment in enumerate(summaries[1:], 1):
#         context = ". ".join(combined.split(". ")[-2:]) + "."
        
#         prompt = (
#             "Continue developing these lecture notes:\n"
#             f"Previous Context: {context}\n\n"
#             f"New Content:\n{segment}\n\n"
#             "Create cohesive notes that:\n"
#             "1. Flow naturally from the context\n"
#             "2. End with 2 transitional sentences\n"
#             "3. Use bullet points for key points\n"
#             "4. Maintain academic style"
#             "Write as book notes, not a script.\n\n"
#         )
        
#         combined = groq_completion([
#             {"role": "system", "content": "Expert at connecting lecture segments"},
#             {"role": "user", "content": prompt}
#         ])
        
#         with open(f"temp_summary_{i}.txt", "w", encoding="utf-8") as f:
#             f.write(combined)
        
#         time.sleep(1) 
    
#     return combined
