# Every number in the paper is produced by one of these targets.
PY ?= python
CONFIG ?= configs/main.yaml

.PHONY: help test pull models smoke run-main run-ablation report audit-v1 annotation agreement reproduce

help:
	@echo "make test          unit tests"
	@echo "make pull          download the five models into Ollama"
	@echo "make models        print local model digests (copy into configs/*.yaml)"
	@echo "make smoke         2 cases/condition, 1 model: checks the stack"
	@echo "make run-main      main experiment (configs/main.yaml), resumable"
	@echo "make run-ablation  prompt-sensitivity ablation"
	@echo "make report        all tables and figures from results/main"
	@echo "make audit-v1      audit of the original submission's logs"
	@echo "make annotation    blinded 300-item annotation sheet"
	@echo "make agreement     inter-rater agreement + detector validation"
	@echo "make reproduce     report + audit from saved logs (no models needed)"

test:
	$(PY) -m pytest -q

pull:
	$(PY) -c "import yaml; from ledger2.ollama_client import OllamaClient as C; c=C(timeout=7200); [print(m['tag'], c.pull(m['tag']).get('status')) for m in yaml.safe_load(open('$(CONFIG)'))['models']]"

models:
	$(PY) -c "import yaml, json; from ledger2.ollama_client import OllamaClient as C; c=C(); print('ollama', c.version()); [print(json.dumps(c.model_info(m['tag']))) for m in yaml.safe_load(open('$(CONFIG)'))['models']]"

smoke:
	$(PY) -m ledger2.runner --config configs/smoke.yaml
	$(PY) -m ledger2.report --runs results/smoke/runs --out results/smoke/report

run-main:
	$(PY) -m ledger2.runner --config configs/main.yaml

run-ablation:
	$(PY) -m ledger2.runner --config configs/ablation_prompts.yaml

report:
	$(PY) -m ledger2.report --runs results/main/runs --out results/main/report
	@if [ -d results/ablation/runs ]; then $(PY) -m ledger2.report --runs results/ablation/runs --out results/ablation/report; fi

audit-v1:
	$(PY) -m ledger2.audit_v1 --logs data/v1_logs --out results/audit_v1

annotation:
	$(PY) -m ledger2.annotation --runs results/main/runs --n 300 --out annotation

agreement:
	$(PY) -m ledger2.agreement --labels annotation/labels/*.csv --key annotation/sample_key.csv --out results/validation

reproduce: audit-v1 report
