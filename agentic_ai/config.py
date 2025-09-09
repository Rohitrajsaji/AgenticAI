from dataclasses import dataclass


@dataclass
class AgentConfig:
    model: str = "gpt-4o-mini"
    max_steps: int = 8
    temperature: float = 0.2
    top_p: float = 1.0
