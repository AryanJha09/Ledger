# Ledger

Ledger is a research-oriented framework for studying systemic vulnerabilities in LLM-based agent pipelines for financial decision-making, with a focus on loan approval scenarios.

The project simulates a multi-agent decision pipeline where Large Language Models (LLMs) are intentionally mocked to enable controlled experimentation, reproducibility, and behavioral analysis.

## Motivation

As LLM-driven agents are increasingly used in high-stakes domains such as finance, understanding failure modes, bias propagation, and emergent inconsistencies becomes critical. Ledger provides a sandbox to analyze these risks at the pipeline level rather than at the single-model level.

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
- Quantitative and qualitative analysis of agent behavior
- Synthetic data generation
- Research-focused, not production-oriented

## Status

Active research project. Core pipeline implemented; analysis and ablation studies ongoing.

