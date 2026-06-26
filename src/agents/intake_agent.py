"""
intake_agent.py
First agent in the pipeline.
Validates and extracts structured intent from the user's goal using ADK + Gemini.
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai
from src.security.guardrails import validate_user_input

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

INTAKE_SYSTEM_PROMPT = """
You are the intake agent for an R&D experiment planning system.
Your only job is to validate and extract the user's planning intent.

Given a user goal, respond with a JSON object containing:
- "valid": true or false
- "intent": one of ["prioritize_experiments", "summarize_history", "generate_memo", "unsupported"]
- "goal_rephrased": a clean one-sentence restatement of the goal
- "rejection_reason": null if valid, or a brief reason if not

Only respond with valid JSON. No extra text.
"""


def run_intake_agent(user_goal: str) -> dict:
    """
    Validate user input and extract structured intent.
    Returns a dict with intent, rephrased goal, and validation result.
    """
    # Security check before calling LLM
    is_valid, reason = validate_user_input(user_goal)
    if not is_valid:
        return {
            "valid": False,
            "intent": "unsupported",
            "goal_rephrased": user_goal,
            "rejection_reason": reason,
        }

    model = genai.GenerativeModel(
        model_name=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        system_instruction=INTAKE_SYSTEM_PROMPT,
    )

    response = model.generate_content(
        f'User goal: "{user_goal}"\n\nRespond with valid JSON only.'
    )

    import json
    try:
        # Strip markdown code fences if present
        raw = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        result = json.loads(raw)
    except Exception:
        result = {
            "valid": True,
            "intent": "prioritize_experiments",
            "goal_rephrased": user_goal,
            "rejection_reason": None,
        }

    return result
