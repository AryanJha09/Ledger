# Reproducing the resubmission results (Ledger v2)

The original submission's pipeline is kept unchanged in `agents/`, `diagnostics/`,
`analysis/` and `experiments/` so that it can be audited. All new work is in
`ledger2/`. Every table and figure in the paper is produced by a `make` target.

## What changed from v1, and why

| v1 problem | v2 fix | Where |
| --- | --- | --- |
| Unparseable output replaced by `review / 0.5 / []` and counted as behaviour (LLaMA3 100/100, DeepSeek-R1 100/100, Phi-3 93/100 runs) | Raw text always saved; robust parser strips `<think>` blocks, fences and prose; failures get a status and are excluded; compliance reported per model | `ledger2/parsing.py`, `make audit-v1` |
| `is_tooling_failure` checked the wrong key | Fixed | `analysis/utils.py` |
| Unseeded data; one fixed no-uncertainty case | Seeded generator with per-condition streams and SHA-256 dataset hash; 50 varied control cases | `ledger2/dataset.py`, `ledger2/domains/` |
| `ollama run` defaults; metadata said `mistral-7b-instruct, T=0.7` for every model | HTTP API with explicit temperature, top_p, seed, context and length; model digest, Ollama version, hardware and git revision logged per run | `ledger2/ollama_client.py`, `ledger2/runner.py` |
| Hedge-word "escalation" detector | Input-grounded tags (fills missing field, forward-looking, extra-schema fact, contradicts input, ...) | `ledger2/detectors/v2.py` |
| Signal definitions in code differed from the paper | One definition per signal, quoted in the paper | `ledger2/detectors/v2.py` |
| No human validation | Blinded stratified sample, guidelines, Cohen/Fleiss kappa, Krippendorff alpha, detector P/R/F1 | `annotation/`, `ledger2/agreement.py` |
| Percentages without uncertainty | Wilson CIs, Fisher/chi-square with Holm, Cohen's h, Cramer's V, logistic regression with length covariate, bootstrap | `ledger2/stats.py`, `ledger2/report.py` |
| "Review" rate read as restraint | Normative policy per case; appropriate restraint, masked overreach, risky commitment rates | `ledger2/domains/*.py` (`policy`) |
| Single domain | Loan, clinical triage referral, hiring screen with the same five conditions | `ledger2/domains/` |

## Steps

```bash
# 0. Tests (also run during the Docker build)
docker compose build ledger

# 1. Model server. NVIDIA GPU: as is. CPU-only: delete the `deploy:` block.
#    macOS: install Ollama natively, then export OLLAMA_HOST=http://host.docker.internal:11434
docker compose up -d ollama
docker compose run --rm ledger make pull
docker compose run --rm ledger make models     # paste digests into configs/main.yaml

# 2. Check the stack (a few minutes)
docker compose run --rm ledger make smoke

# 3. Experiments (resumable; re-run the same command after an interruption)
docker compose run --rm ledger make run-main       # 5,250 generations
docker compose run --rm ledger make run-ablation   # 2,500 generations

# 4. Tables and figures
docker compose run --rm ledger make report         # results/main/report/report.md

# 5. Human validation
docker compose run --rm ledger make annotation     # annotation/sheet_template.csv
#    annotators follow annotation/GUIDELINES.md and save annotation/labels/<initials>.csv
docker compose run --rm ledger make agreement      # results/validation/agreement.json
```

Without Docker: `pip install -r requirements.txt` (Python 3.11+), run Ollama, then the same `make` targets.

## Audit of the original logs

`make audit-v1` reads `data/v1_logs/` (the logs behind the IC3AI submission)
and writes `results/audit_v1/audit.md`.
