# R&D Experiment Prioritization Agent

An AI agent system for R&D teams that analyzes previous experiment outcomes, current constraints, and project goals to recommend the next best experiments and generate a short decision-ready memo.

## Problem

In many research and development settings, experiment planning is slow and inconsistent because prior experiment notes, results, and constraints are scattered across spreadsheets, text files, and team memory.

This leads to:
- repeated failed experiments,
- slow decision-making,
- poor knowledge reuse,
- wasted time and budget.

This project addresses that problem by building an agent-based workflow that helps prioritize the next experiments in a structured and explainable way.

## Why agents

This problem is a good fit for AI agents because it requires more than a single answer:
- one component must read and organize past experiment records,
- another must reason over constraints and goals,
- another must rank possible next actions,
- and another must generate a clear report for a human decision-maker.

Instead of a simple chatbot, this project uses an agent workflow to turn messy R&D context into actionable recommendations.

## Track

This project is submitted to the **Agents for Business** track because it focuses on improving decision-making and productivity in R&D workflows, where time and cost matter.

## What the system does

Given:
- past experiment records,
- project constraints,
- short experiment notes,
- and a user goal,

the system:
1. summarizes past work,
2. identifies promising next directions,
3. ranks candidate experiments,
4. explains trade-offs,
5. generates a short decision memo.

## Example use case

A materials R&D team is trying to improve particle alignment in an active matter system under limited time and budget. The team has already tried several combinations of control parameters, but results are mixed and notes are incomplete. The agent reviews prior outcomes and recommends the next best experiments to run.

## Architecture

This project uses a small multi-agent design:

- **Intake Agent**  
  Accepts the user goal and request.

- **Context Agent**  
  Reads experiment history, notes, and constraints, then creates a structured context summary.

- **Prioritization Agent**  
  Scores and ranks possible next experiments based on goals, past outcomes, novelty, and feasibility.

- **Report Agent**  
  Produces a human-readable recommendation memo.

## Course concepts demonstrated

This project is designed to demonstrate at least three course concepts required by the capstone:

- **Agent / Multi-agent system (ADK)** — in code
- **MCP Server** — in code
- **Security features** — in code
- **Antigravity / deployability / agent skills** — may be discussed in the video depending on final implementation

## Repository structure

```text
rd-prioritization-agent/
├── README.md
├── requirements.txt
├── .env.example
├── app.py
├── demo.py
├── data/
│   ├── experiments.csv
│   ├── constraints.json
│   └── sample_notes/
├── src/
│   ├── agents/
│   ├── tools/
│   ├── prompts/
│   ├── security/
│   └── utils/
├── output/
├── assets/
└── docs/
```

## Data files

The starter version uses synthetic sample data:
- `data/experiments.csv` for prior experiment history,
- `data/constraints.json` for project and operational constraints,
- `data/sample_notes/` for short unstructured notes.

This makes the project easy to run locally without private or sensitive data.

## Setup

1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Add environment variables to `.env` if needed.
5. Run the demo:
   ```bash
   python demo.py
   ```

## Example output

The expected output is:
- a ranked list of recommended next experiments,
- a short explanation of why they were selected,
- a decision memo for a scientist or R&D manager.

## Security notes

This project is designed to avoid unsafe or irrelevant behavior by:
- restricting the scope of supported tasks,
- validating inputs,
- limiting tool access,
- preventing accidental exposure of secrets,
- and rejecting unsupported requests.

## Limitations

This is an early prototype intended for demonstration and learning. It uses synthetic data and simplified scoring logic. It does not replace human scientific judgment and should be treated as a decision-support tool, not an autonomous lab planner.

## Future work

Possible extensions:
- connect to real lab notebooks or experiment databases,
- integrate literature retrieval,
- support interactive web UI,
- improve ranking with learned scoring models,
- add deployment and monitoring.

## Kaggle submission assets

This repository supports the required capstone submission materials:
- public code repository,
- README documentation,
- architecture explanation,
- video demo,
- Kaggle writeup.

## Author

Built as a capstone project for Kaggle’s **AI Agents: Intensive Vibe Coding Capstone Project**.
