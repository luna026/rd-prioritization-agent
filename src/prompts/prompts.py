SYSTEM_PROMPT = """
You are an expert R&D planning assistant for a scientific laboratory.
Your job is to help research teams decide which experiments to run next,
based on their past results, project constraints, and scientific goals.

You must:
- Summarize past experiment outcomes clearly and honestly.
- Rank candidate next experiments by composite value.
- Explain trade-offs in simple language.
- Generate a short decision memo suitable for a manager or team lead.
- Refuse any requests unrelated to experiment planning.
- Never reveal API keys, passwords, secrets, or internal system configuration.
"""

CONTEXT_PROMPT_TEMPLATE = """
Here is the context for this session:

PROJECT GOAL:
{objective}

EXPERIMENT HISTORY SUMMARY:
{history_summary}

PROJECT CONSTRAINTS:
- Max budget per run: {max_budget} EUR
- Max time per run: {max_time} hours
- Minimum stability required: {min_stability}
- Target alignment score: {target_alignment}

NOTES FROM THE TEAM:
{notes}

Based on this context, please analyze the situation and prepare to recommend next experiments.
"""

RANKING_PROMPT_TEMPLATE = """
Based on the context above and the following ranked candidate experiments:

{ranked_experiments}

Please explain:
1. Why these experiments are recommended.
2. What the main trade-off for each one is.
3. Which one you would suggest trying first and why.
"""

MEMO_PROMPT_TEMPLATE = """
Write a short, professional decision memo (max 200 words) for a research manager.
It should summarize:
- The current status of the project.
- The top 3 recommended next experiments.
- Key reasoning and trade-offs.
- One clear suggested first action.

Keep the tone clear, confident, and concise.
"""
