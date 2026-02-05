# Detector Version v1 (Pre-Review Snapshot)

This directory contains the exact detector implementation used to generate
all behavioral signal results reported in the initial submission of the paper:

"Epistemic Failure Modes of Large Language Models Under Decision Uncertainty".

## Source
- Copied verbatim from: analysis/qualitative.py
- Snapshot date: 2026-02-04

## Behavioral Signals Implemented
- Assumption Invention
- Risk Rationalization
- Unjustified Confidence

## Detector Characteristics
- Rule-based heuristics
- Fixed confidence threshold (0.75)
- No semantic validation of assumptions
- No human annotation or calibration

## Status
This version is frozen and must not be modified.
Any revised or alternative detectors must be placed in
separately versioned directories (e.g., detectors_v2).

## Known Limitations
- Prompt-dependent (assumptions field required)
- No sensitivity analysis performed in v1
- Potential false positives due to coarse heuristics

