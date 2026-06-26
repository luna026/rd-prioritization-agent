"""
context_agent.py
Second agent in the pipeline.
Loads all project data and builds a rich context summary using google-genai.
"""
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from src.utils.loader import load_experiments, load_constraints, load_notes, summarize_experiments
from src.prompts.prompts import CONTEXT_PROMPT_TEMPLATE

load_dotenv()
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


def run_context_agent(goal_rephrased: str) -> dict:
    """
    Load all project data and return a structured context object
    with history summary, notes, constraints, and LLM-generated analysis.
    """
    df = load_experiments()
    constraints = load_constraints()
    notes = load_notes()

    history_summary = summarize_experiments(df)
    notes_text = "\n\n".join([f"[{n['filename']}]\n{n['content']}" for n in notes])
    ops = constraints["operational_constraints"]
    rules = constraints["decision_rules"]

    prompt = CONTEXT_PROMPT_TEMPLATE.format(
        objective=goal_rephrased,
        history_summary=history_summary,
        notes=notes_text,
        max_budget=ops["max_budget_eur_per_experiment"],
        max_time=ops["max_time_hours_per_experiment"],
        min_stability=rules["minimum_stability_score"],
        target_alignment=rules["target_alignment_score"],
    )

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="You are an expert R&D planning assistant. Analyze the provided project context carefully and thoroughly.",
        ),
    )

    return {
        "raw_data": df,
        "constraints": constraints,
        "notes": notes,
        "history_summary": history_summary,
        "llm_analysis": response.text,
    }
