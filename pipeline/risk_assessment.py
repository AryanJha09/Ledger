from agents.mock_agent import run_mock_agent
from agents.real_agent import run_real_agent

# Import metadata (single source of truth)
from config.agent_config import AGENT_METADATA



def assess_risk(ingest_output):
    """
    Calls the selected agent to assess risk based on ingested data.
    Selection is driven entirely by AGENT_METADATA.
    """

    agent_type = AGENT_METADATA["agent_type"]

    if agent_type == "mock":
        agent_output = run_mock_agent(ingest_output["data"])
    elif agent_type == "real":
        agent_output = run_real_agent(ingest_output["data"])
    else:
        raise ValueError(f"Unknown agent_type: {agent_type}")

    return {
        "agent_output": agent_output,
        "risks": agent_output.get("risks", []),
        "confidence": agent_output.get("confidence"),
        "assumptions": agent_output.get("assumptions", [])
    }
