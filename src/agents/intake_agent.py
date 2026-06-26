import os
import json
from dotenv import load_dotenv
from src.utils.llm_client import generate
from src.security.guardrails import validate_user_input

load_dotenv()

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
    is_valid, reason = validate_user_input(user_goal)
    if not is_valid:
        return {
            "valid": False,
            "intent": "unsupported",
            "goal_rephrased": user_goal,
            "rejection_reason": reason,
        }

    raw = generate(INTAKE_SYSTEM_PROMPT, f'User goal: "{user_goal}"\n\nRespond with valid JSON only.')

    try:
        cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(cleaned)
    except Exception:
        return {
            "valid": True,
            "intent": "prioritize_experiments",
            "goal_rephrased": user_goal,
            "rejection_reason": None,
        }
