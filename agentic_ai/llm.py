# pyright: ignore[reportMissingImports]
from typing import Any, Dict, List, Optional, cast
from openai import OpenAI  # pyright: ignore[reportMissingImports]
from openai._types import NOT_GIVEN  # pyright: ignore[reportMissingImports]


class LLMClient:
    def __init__(self, model: str):
        self.model = model
        self.client = OpenAI()

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None):
        """Wrapper around OpenAI Chat Completions with tool-calling.

        Notes on typing:
        - The OpenAI SDK expects specific typed unions for messages/tools.
        - We cast to Any at the call-site to satisfy Pylance while preserving
          the simple internal representation used by the agent.
        - We pass NOT_GIVEN when tools/tool_choice are not provided to fit
          the SDK's expected sentinel for omitted params.
        """
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=cast(Any, messages),
            tools=cast(Any, tools) if tools is not None else NOT_GIVEN,
            tool_choice="auto" if tools else NOT_GIVEN,
        )
        return resp.choices[0]
    

