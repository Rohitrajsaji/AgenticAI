# AgenticAI (Minimal Agent)

A small, understandable agent with ReAct-style tool use built on OpenAI function-calling.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai==1.* pydantic==2.* httpx==0.27.* tenacity==8.* rich==13.* click==8.* \
            duckduckgo-search==6.* beautifulsoup4==4.* lxml==5.*
export OPENAI_API_KEY="sk-..."
python -m examples.demo_cli "What's new in Python 3.13? Summarize with 2 sources."
```

## Structure

- `agentic_ai/agent.py` — main agent loop (tool-calling)
- `agentic_ai/tools.py` — tool registry and implementations (web_search, fetch_url, calculator)
- `agentic_ai/llm.py` — OpenAI client wrapper
- `agentic_ai/memory.py` — short-term memory buffer
- `agentic_ai/config.py` — configuration defaults
- `examples/demo_cli.py` — CLI entry point

## Tests

```bash
pytest -q
```
