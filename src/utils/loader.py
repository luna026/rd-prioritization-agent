import pandas as pd
import json
from pathlib import Path


def load_experiments(csv_path: str = "data/experiments.csv") -> pd.DataFrame:
    """Load experiment history from CSV."""
    df = pd.read_csv(csv_path)
    return df


def load_constraints(json_path: str = "data/constraints.json") -> dict:
    """Load project constraints from JSON."""
    with open(json_path, "r") as f:
        return json.load(f)


def load_notes(notes_dir: str = "data/sample_notes") -> list[dict]:
    """Load all .txt notes from the sample_notes directory."""
    notes = []
    for path in sorted(Path(notes_dir).glob("*.txt")):
        notes.append({"filename": path.name, "content": path.read_text()})
    return notes


def summarize_experiments(df: pd.DataFrame) -> str:
    """Create a brief text summary of past experiment outcomes."""
    total = len(df)
    successes = len(df[df["outcome_status"] == "success"])
    partial = len(df[df["outcome_status"] == "partial_success"])
    failed = len(df[df["outcome_status"] == "failed"])

    best_alignment = df.loc[df["alignment_score"].idxmax()]
    best_stability = df.loc[df["stability_score"].idxmax()]
    best_balance = df.loc[(df["alignment_score"] + df["stability_score"]).idxmax()]

    summary = f"""
Past Experiment Summary ({total} total runs):
- Successes: {successes} | Partial: {partial} | Failed: {failed}
- Best alignment: {best_alignment['experiment_id']} (score={best_alignment['alignment_score']}, control={best_alignment['control_parameter']})
- Best stability: {best_stability['experiment_id']} (score={best_stability['stability_score']}, control={best_stability['control_parameter']})
- Best overall trade-off: {best_balance['experiment_id']} (alignment={best_balance['alignment_score']}, stability={best_balance['stability_score']}, cost={best_balance['cost_estimate_eur']} EUR)
"""
    return summary.strip()
