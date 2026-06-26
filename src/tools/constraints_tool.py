"""
constraints_tool.py
Tool for retrieving project constraints.
Exposed via MCP server for agent use.
"""
from src.utils.loader import load_constraints


def get_all_constraints() -> dict:
    """Return full project constraints."""
    return load_constraints()


def get_operational_constraints() -> dict:
    """Return only operational constraints (budget, time, density, temp)."""
    constraints = load_constraints()
    return constraints.get("operational_constraints", {})


def get_decision_rules() -> dict:
    """Return only decision rules (thresholds, targets, preferences)."""
    constraints = load_constraints()
    return constraints.get("decision_rules", {})


def get_allowed_actions() -> list[str]:
    """Return the list of actions this agent system is allowed to perform."""
    constraints = load_constraints()
    return constraints.get("allowed_actions", [])


def get_security_rules() -> dict:
    """Return security configuration rules."""
    constraints = load_constraints()
    return constraints.get("security_rules", {})
