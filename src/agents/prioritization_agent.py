"""
prioritization_agent.py
Third agent in the pipeline.
Ranks and explains next experiment candidates using scoring + Gemini reasoning.
"""
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from src.utils.scoring import rank_experiments
from src.prompts.prompts import RANKING_PROMPT_TEMPLATE

load_dotenv()
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


def run_prioritization_agent(context: dict) -> dict:
    """
    Score and rank candidate experiments.
    Returns ranked dataframe + LLM explanation of the ranking.
    """
    df = context["raw_data"]
    constraints = context["constraints"]
    top_k = constraints["output_requirements"]["top_k_recommendations"]

    ranked = rank_experiments(df, constraints, top_k=top_k)

    ranked_text = ""
    for i, row in ranked.iterrows():
        ranked_text += (
            f"\n{i+1}. {row['experiment_id']} | control={row['control_parameter']} | "
            f"alignment={row['alignment_score']} | stability={row['stability_score']} | "
            f"cost={row['cost_estimate_eur']} EUR | score={row['composite_score']}\n"
            f"   Notes: {row['notes_summary']}\n"
        )

    full_prompt = (
        f"Context analysis from previous step:\n{context['llm_analysis']}\n\n"
        + RANKING_PROMPT_TEMPLATE.format(ranked_experiments=ranked_text)
    )

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        contents=full_prompt,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are an expert R&D experiment planner. "
                "Given scored experiments, explain the recommendations clearly and highlight trade-offs. "
                "Be concise and specific. Do not invent data not provided."
            ),
        ),
    )

    return {
        "ranked": ranked,
        "ranking_explanation": response.text,
    }
