from typing import Any, Dict, List, Callable
from bs4 import BeautifulSoup
import httpx
import json
import os
from tavily import TavilyClient

ToolSpec = Dict[str, Any]

# Initialize Tavily client
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def make_tool(
    name: str,
    description: str,
    parameters: Dict[str, Any],
    handler: Callable[..., Any],
) -> ToolSpec:
    return {
        "name": name,
        "description": description,
        "parameters": parameters,
        "handler": handler,
    }


def registry() -> List[ToolSpec]:
    return [
        make_tool(
            name="web_search",
            description="Search the web for current information using Tavily. Returns a list of results.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
            handler=tool_web_search,
        ),
        make_tool(
            name="fetch_url",
            description="Fetch a URL and return cleaned text content (best-effort).",
            parameters={
                "type": "object",
                "properties": {"url": {"type": "string"}},
                "required": ["url"],
            },
            handler=tool_fetch_url,
        ),
        make_tool(
            name="calculator",
            description="Safely evaluate simple arithmetic expressions. No variables or functions allowed.",
            parameters={
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
            handler=tool_calculator,
        ),
    ]


def tool_web_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Search the web using Tavily API."""
    results = tavily.search(query=query, max_results=max_results)
    return [
        {
            "title": r.get("title"),
            "href": r.get("url"),
            "snippet": r.get("content"),
        }
        for r in results.get("results", [])
    ]


def tool_fetch_url(url: str) -> Dict[str, Any]:
    """Fetch a webpage and extract readable text."""
    with httpx.Client(timeout=15.0, follow_redirects=True) as client:
        r = client.get(url, headers={"User-Agent": "agentic-ai/0.1"})
        r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    for s in soup(["script", "style", "noscript"]):
        s.extract()
    text = " ".join(soup.get_text(separator=" ").split())
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    return {"title": title, "text": text[:20000], "url": url}


ALLOWED_CHARS = set("0123456789+-*/(). ")


def tool_calculator(expression: str) -> str:
    """Evaluate basic math expressions safely."""
    if not set(expression).issubset(ALLOWED_CHARS):
        return "Error: unsupported characters."
    try:
        value = eval(expression, {"__builtins__": {}}, {})
        return str(value)
    except Exception as e:
        return f"Error: {e}"


def openai_tool_specs(tools: List[ToolSpec]) -> List[Dict[str, Any]]:
    """Convert internal tool registry to OpenAI tool spec format."""
    specs = []
    for t in tools:
        specs.append(
            {
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t["description"],
                    "parameters": t["parameters"],
                },
            }
        )
    return specs


def call_tool(tools: List[ToolSpec], name: str, args: Dict[str, Any]) -> Any:
    """Execute a registered tool by name with provided arguments."""
    mapping = {t["name"]: t["handler"] for t in tools}
    if name not in mapping:
        return {"error": f"Unknown tool: {name}"}
    return mapping[name](**args)
