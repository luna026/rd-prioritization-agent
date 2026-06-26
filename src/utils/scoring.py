import pandas as pd


def score_experiment(row: pd.Series, constraints: dict) -> float:
    """
    Score a past experiment as a candidate for replication or extension.

    Scoring criteria (weighted sum):
    - Alignment score (higher = better)
    - Stability score (must meet minimum threshold)
    - Novelty score (favor under-explored conditions)
    - Cost penalty (higher cost = lower score)
    - Failed experiments are penalized
    """
    rules = constraints.get("decision_rules", {})
    ops = constraints.get("operational_constraints", {})

    min_stability = rules.get("minimum_stability_score", 0.50)
    max_budget = ops.get("max_budget_eur_per_experiment", 200)

    # Penalize if stability is below threshold
    if row["stability_score"] < min_stability:
        return 0.0

    # Penalize failures
    if row["outcome_status"] == "failed" and rules.get("penalize_failed_conditions", True):
        return 0.0

    # Weighted score
    alignment_weight = 0.40
    stability_weight = 0.25
    novelty_weight = 0.20
    cost_weight = 0.15

    cost_score = max(0.0, 1.0 - (row["cost_estimate_eur"] / max_budget))

    score = (
        alignment_weight * row["alignment_score"]
        + stability_weight * row["stability_score"]
        + novelty_weight * row["novelty_score"]
        + cost_weight * cost_score
    )
    return round(score, 4)


def rank_experiments(df: pd.DataFrame, constraints: dict, top_k: int = 3) -> pd.DataFrame:
    """Return top-k experiments by composite score."""
    df = df.copy()
    df["composite_score"] = df.apply(lambda row: score_experiment(row, constraints), axis=1)
    ranked = df[df["composite_score"] > 0.0].sort_values("composite_score", ascending=False)
    return ranked.head(top_k).reset_index(drop=True)
