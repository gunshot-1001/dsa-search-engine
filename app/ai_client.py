import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_learning_path(user_profile_text: str, length: int = 8) -> str:
    prompt = (
        f"Create a {length}-step structured DSA study path for a student with profile: {user_profile_text}.\n"
        f"Each step should include:\n"
        f"- Topic name\n"
        f"- 1-2 recommended practice problems (just typical titles, not links)\n"
        f"- Rationale (1-2 sentences)."
    )
    resp = model.generate_content(prompt)

    # safely extract text
    try:
        return resp.text
    except AttributeError:
        return resp.candidates[0].content.parts[0].text


def explain_code(user_code: str, language: str, problem_description: str) -> str:
    prompt = (
        f"Problem:\n{problem_description}\n\n"
        f"User's {language} code:\n```{language}\n{user_code}\n```\n\n"
        f"Please:\n"
        f"1. Identify logical/structural errors.\n"
        f"2. Explain why the code may fail or be suboptimal.\n"
        f"3. Provide a corrected solution with detailed explanation."
    )
    resp = model.generate_content(prompt)

    # safely extract text
    try:
        return resp.text
    except AttributeError:
        return resp.candidates[0].content.parts[0].text
