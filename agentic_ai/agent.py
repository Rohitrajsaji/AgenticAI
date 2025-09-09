import json
from typing import Optional
from openai.types.chat import ChatCompletionMessageFunctionToolCall
from .llm import LLMClient
from .memory import ShortTermMemory
from .tools import registry, openai_tool_specs, call_tool
from .config import AgentConfig


SYSTEM_PROMPT = """You are a helpful, cautious, and tool-using assistant.
- Think step-by-step.
- Use tools when needed.
- If you can answer directly, do so concisely with citations when possible.
- When using tools, explain why and what you found.
- Stop when the user’s request is satisfied.
"""


class Agent:
    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        self.llm = LLMClient(model=self.config.model)
        self.mem = ShortTermMemory(max_messages=60)
        self.tools = registry()
        self.mem.add({"role": "system", "content": SYSTEM_PROMPT})

    def run(self, goal: str) -> str:
        self.mem.add({"role": "user", "content": goal})
        tool_specs = openai_tool_specs(self.tools)

        for _ in range(self.config.max_steps):
            choice = self.llm.chat(self.mem.get(), tools=tool_specs)
            msg = choice.message

            # Tool calls path
            if msg.tool_calls is not None:
                self.mem.add({
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": msg.tool_calls,
                })

                # Execute each tool call sequentially
                for tc in msg.tool_calls:
                    if isinstance(tc, ChatCompletionMessageFunctionToolCall):
                        # Safe: function is guaranteed to exist here
                        name = tc.function.name
                        try:
                            args = json.loads(tc.function.arguments or "{}")
                        except json.JSONDecodeError:
                            args = {}

                        result = call_tool(self.tools, name, args)
                        self.mem.add({
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": (
                                json.dumps(result)
                                if not isinstance(result, str)
                                else result
                            ),
                        })
                    else:
                        # Handle or skip unknown/custom tool calls
                        self.mem.add({
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": "Unsupported tool call type",
                        })
                continue

            # No tool calls => final answer
            final_answer = msg.content or ""
            self.mem.add({"role": "assistant", "content": final_answer})
            return final_answer

        return "Reached max steps without a final answer."
