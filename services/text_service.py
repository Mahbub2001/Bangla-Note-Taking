from openai import OpenAI
from typing import List
import os
import re
from openai import APIConnectionError
from dotenv import load_dotenv
load_dotenv()  
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),  
)
def extract_latex_code(text: str) -> str:
    match = re.search(r"```latex(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    latex_start = text.find(r"\documentclass")
    if latex_start != -1:
        return text[latex_start:].strip()
    return text.strip()

def clean_markdown(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  
    text = re.sub(r'__(.*?)__', r'\1', text)      
    text = re.sub(r'\*(.*?)\*', r'\1', text)      
    text = re.sub(r'_(.*?)_', r'\1', text)        
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\*\s*', '', text, flags=re.MULTILINE) 
    text = text.replace('*', '')  

    return text

def summarize_segment(transcript: str, image_desc: str, position: str = "middle") -> str:
    prompt = (
        f"Lecture transcript:\n{transcript}\n\n"
        f"Scene description:\n{image_desc}\n\n"
        "Language should be Bengali.\n"
        "Output in LaTeX format ONLY. Do not include markdown or any explanation.\n"
        "Complete sentence if the transcript is unfinished."
        "Generate a the of the lecture segment that captures key concepts, examples, and formulas, explanation. "
        "Use proper LaTeX structure such as \\section{{}}, \\subsection{{}}, \\begin{{itemize}}...\\end{{itemize}}, and so on.\n"
        "Make the content clean and directly usable in Overleaf."
    )

    if position == "start":
        prompt += (
            "This is the start of the document. Begin with \\documentclass, packages, \\title, \\author, \\date, \\begin{document}, and \\maketitle.\n"
            "Include initial \\section or \\subsection as appropriate.\n"
            "Do not write \\end{document} yet.\n"
        )
    elif position == "end":
        prompt += (
            "This is the end of the document. Don't write \\documentclass, packages, \\title, \\author, \\date, \\begin{document}, and \\maketitle.\n"
            "Include summary and transition and close with \\end{document}.\n"
        )
    else:
        prompt += (
             "This is the middle of the document. Dont write  \\documentclass, packages, \\title, \\author, \\date, \\begin{document}, and \\maketitle.\n"
             "Include any necessary \\section or \\subsection as appropriate.\n"
        )
    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        latex_text = completion.choices[0].message.content
        return  extract_latex_code(clean_markdown(latex_text))
    except APIConnectionError as e:
        print("❌ API Connection Error while summarizing:", str(e))
        return "\\section*{Error}\nCould not generate summary due to connection error."








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
# def groq_completion(messages: list, model: str = "llama3-70b-8192") -> str:
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
    
# def clean_markdown(text: str) -> str:
#     text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  
#     text = re.sub(r'__(.*?)__', r'\1', text)      
#     text = re.sub(r'\*(.*?)\*', r'\1', text)      
#     text = re.sub(r'_(.*?)_', r'\1', text)        
#     text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
#     text = re.sub(r'^\s*\*\s*', '', text, flags=re.MULTILINE) 
#     text = text.replace('*', '')  

#     return text


# def summarize_segment(transcript: str, image_desc: str) -> str:
#     """
#     Generate concise summary with focus on continuity
#     """
#     prompt = (
#         f"Lecture transcript:\n{transcript}\n\n"
#         f"Scene description:\n{image_desc}\n\n"
#         "Strictly, the language must be Bengali. Do not write anything else.Only give the note. Dont write other things\n"
#         "Only utilize the transcript and scene description to create the final note.\n\n"
#         "Output the note in **LaTeX format**. Do not use markdown (no **, ##, etc.).\n"
#         "Use proper LaTeX structure such as \\section{{}}, \\subsection{{}}, \\begin{{itemize}}...\\end{{itemize}}, and so on.\n"
#         "Make sure to complete any unfinished sentences from the transcript.\n"
#         "key concepts, examples, formulas,solution of anything and explanations from the lecture.\n"
#         "End with two well-structured transitional sentences (also in Bengali) that help connect to the next lecture segment.\n"
#         "Make the note readable and presentable in a LaTeX document."
#     )
#     response = groq_completion([
#         {"role": "user", "content": prompt}
#     ])    
#     return clean_markdown(response)