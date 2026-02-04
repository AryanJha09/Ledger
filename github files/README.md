# Ledger

Ledger is a research-oriented framework for studying **systemic vulnerabilities in LLM-based agent pipelines** for financial decision-making tasks, with a focus on loan approval scenarios.

The project simulates a multi-agent decision pipeline where Large Language Models (LLMs) are intentionally *mocked* to enable controlled experimentation, reproducibility, and behavioral analysis.

## Motivation

As LLM-driven agents are increasingly used in high-stakes domains (e.g., finance), understanding **failure modes, bias propagation, and emergent inconsistencies** becomes critical. Ledger provides a sandbox to analyze these risks at the pipeline level rather than at the single-model level.

## Pipeline Overview

The agent workflow is implemented as a directed graph and includes:
- Data ingestion
- Risk assessment
- Decision proposal
- Portfolio-level consistency checks
- Self-critique and contradiction detection
- Final decision synthesis

Each node can be independently instrumented, replaced, or stressed to study downstream effects.

## Key Features

- Modular, graph-based agent architecture
- Mocked LLM behavior for deterministic experiments
- Quantitative and qualitative log analysis
- Synthetic data generation
- Designed for research, not production use

## Project Structure (High-Level)

- `data/` – synthetic dataset generation
- `experiments/` – experiment runners and configurations
- `analysis/` – quantitative and qualitative behavior analysis
- `logs/` – structured experiment outputs

## Status

Active research project. Core pipeline and experimental framework implemented; analysis and ablation studies ongoing.

## Intended Audience

- ML & agentic systems researchers  
- AI safety and governance researchers  
- FinTech AI practitioners (research context only)

## Disclaimer

This project is for research and educational purposes only and is **not** intended for real-world financial decision-making.
