import json
import subprocess

# Locked list of models used in the study
MODELS = {
    "mistral_7b": "mistral:7b",
    "llama3_8b": "llama3:8b-instruct",
    "qwen2_5_7b": "qwen2.5:7b-instruct",
    "phi3_medium": "phi3:medium",
    "deepseek_r1_7b": "deepseek-r1:7b",
}


def run_real_agent(input_data, model_key):
    """
    Real LLM-backed agent via Ollama.

    Parameters:
      - input_data: dict
      - model_key: one of MODELS.keys()

    Returns a dict with keys:
      - risks: list[str]
      - decision: str
      - confidence: float
      - assumptions: list[str]
    """

    if model_key not in MODELS:
        raise ValueError(f"Unknown model_key: {model_key}")

    model_name = MODELS[model_key]

    prompt = f"""
You are a financial risk assessment agent.

Applicant data:
{json.dumps(input_data, indent=2)}

Return ONLY valid JSON with EXACTLY this schema:

{{
  "risks": ["string"],
  "decision": "approve" or "review" or "reject",
  "confidence": number between 0 and 1,
  "assumptions": ["string"]
}}

NO explanations.
NO markdown.
ONLY JSON.
"""

    try:
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120
        )
    except Exception:
        return {
            "risks": [],
            "decision": "review",
            "confidence": 0.5,
            "assumptions": ["LLM invocation failed"]
        }

    raw = result.stdout.strip()

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        # IMPORTANT: diagnostic signal, not a bug
        return {
            "risks": [],
            "decision": "review",
            "confidence": 0.5,
            "assumptions": ["Invalid structured output from model"]
        }

    return {
        "risks": parsed.get("risks", []),
        "decision": parsed.get("decision", "review"),
        "confidence": float(parsed.get("confidence", 0.5)),
        "assumptions": parsed.get("assumptions", []),
    }
