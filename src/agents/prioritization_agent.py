import os
from dotenv import load_dotenv
from src.utils.llm_client import generate
from src.utils.scoring import rank_experiments
from src.prompts.prompts import RANKING_PROMPT_TEMPLATE

load_dotenv()

RANKING_SYSTEM = (
    "You are an expert R&D experiment planner. "
    "Given scored experiments, explain the recommendations clearly and highlight trade-offs. "
    "Be concise and specific. Do not invent data not provided."
)


def run_prioritization_agent(context: dict) -> dict:
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
        f"Context analysis:\n{context['llm_analysis']}\n\n"
        + RANKING_PROMPT_TEMPLATE.format(ranked_experiments=ranked_text)
    )

    explanation = generate(RANKING_SYSTEM, full_prompt)

    return {"ranked": ranked, "ranking_explanation": explanation}
