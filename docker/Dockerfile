# Analysis + runner image. Model inference happens in the separate `ollama`
# service (see docker-compose.yml), so this image stays small and CPU-only.
FROM python:3.12.8-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MPLBACKEND=Agg

RUN apt-get update \
 && apt-get install -y --no-install-recommends git make \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /work
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
# Fail the build if the test suite does not pass.
RUN python -m pytest -q

CMD ["make", "help"]
