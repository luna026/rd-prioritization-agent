"""
test_mcp.py — Quick smoke test for the MCP tools (no server needed).
Calls the underlying tool functions directly to verify they return data.
"""
from src.tools.experiment_lookup import (
    get_all_experiments,
    get_successful_experiments,
    get_top_alignment_experiments,
)
from src.tools.constraints_tool import (
    get_all_constraints,
    get_decision_rules,
    get_allowed_actions,
)

print("=== MCP Tool Smoke Test ===\n")

exps = get_all_experiments()
print(f"✓ get_all_experiments        → {len(exps)} records")

successful = get_successful_experiments()
print(f"✓ get_successful_experiments → {len(successful)} records")

top3 = get_top_alignment_experiments(top_k=3)
print(f"✓ get_top_alignment_experiments (top 3):")
for e in top3:
    print(f"    {e['experiment_id']} | alignment={e['alignment_score']} | control={e['control_parameter']}")

constraints = get_all_constraints()
print(f"\n✓ get_all_constraints        → keys: {list(constraints.keys())}")

rules = get_decision_rules()
print(f"✓ get_decision_rules         → min_stability={rules['minimum_stability_score']}, target_alignment={rules['target_alignment_score']}")

actions = get_allowed_actions()
print(f"✓ get_allowed_actions        → {actions}")

print("\n=== All MCP tools verified ✓ ===")
