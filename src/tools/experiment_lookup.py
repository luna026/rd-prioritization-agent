"""
experiment_lookup.py
Tool for retrieving and filtering experiment history.
Exposed via MCP server for agent use.
"""
import pandas as pd
from src.utils.loader import load_experiments


def get_all_experiments() -> list[dict]:
    """Return full experiment history as a list of records."""
    df = load_experiments()
    return df.to_dict(orient="records")


def get_successful_experiments() -> list[dict]:
    """Return only experiments with 'success' or 'partial_success' status."""
    df = load_experiments()
    filtered = df[df["outcome_status"].isin(["success", "partial_success"])]
    return filtered.to_dict(orient="records")


def get_experiment_by_id(experiment_id: str) -> dict | None:
    """Return a single experiment record by ID."""
    df = load_experiments()
    result = df[df["experiment_id"] == experiment_id]
    if result.empty:
        return None
    return result.iloc[0].to_dict()


def get_top_alignment_experiments(top_k: int = 3) -> list[dict]:
    """Return the top-k experiments ranked by alignment score."""
    df = load_experiments()
    top = df.nlargest(top_k, "alignment_score")
    return top.to_dict(orient="records")


def get_experiments_by_control(control_parameter: str) -> list[dict]:
    """Return all experiments using a specific control parameter."""
    df = load_experiments()
    filtered = df[df["control_parameter"] == control_parameter]
    return filtered.to_dict(orient="records")
