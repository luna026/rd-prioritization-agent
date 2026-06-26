"""
llm_client.py — Unified LLM wrapper. Switch provider via .env LLM_PROVIDER.
Supports: "groq" (free) or "gemini"
"""
import os
from dotenv import load_dotenv
load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "groq")


def generate(system_prompt: str, user_prompt: str) -> str:
    if PROVIDER == "groq":
        from groq import Groq
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content

    else:  # gemini
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            contents=user_prompt,
            config=types.GenerateContentConfig(system_instruction=system_prompt),
        )
        return response.text
