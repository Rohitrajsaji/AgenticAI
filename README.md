# AgenticAI 🚀

**AgenticAI** is a minimal, modular agent framework that leverages OpenAI’s function/tool-calling to answer user queries. It can optionally use external tools like web search, URL fetching, and safe calculations to provide enriched responses.

---

## 🔹 Features
- Modular tool system — easily add new tools.  
- ReAct-style reasoning: step-by-step thought process with tool use and citations.  
- Simple, readable, maintainable, and extensible codebase.  
- Supports safe execution: calculator input restricted to safe characters; web fetch uses content cleaning.  
- CLI interface for interactive use.  

---

## 🔹 Project Structure

AgenticAI/
├─ agentic_ai/
│ ├─ agent.py # Core agent loop
│ ├─ tools.py # Tool registry and implementations
│ ├─ llm.py # OpenAI wrapper with tool-calling
│ ├─ memory.py # Conversation memory buffer
│ └─ config.py # Agent configuration
├─ examples/
│ └─ demo_cli.py # CLI entry point
├─ .venv/ # Python virtual environment (ignored in Git)
└─ requirements.txt # Dependencies

**Tools included:**  
- `web_search` (via Tavily API)  
- `fetch_url` (scrapes and cleans webpage text)  
- `calculator` (safe arithmetic evaluation)  

---

## 🔹 Installation

1. Clone the repository:  
            git clone https://github.com/rohitrajsaji/AgenticAI.git
            cd AgenticAI
2.Create and activate a virtual environment:
            python -m venv .venv
            source .venv/bin/activate      # macOS/Linux
            # .venv\\Scripts\\activate     # Windows
3.Install dependencies:
            pip install -r requirements.txt
4.Set your API keys:
            export OPENAI_API_KEY="your_openai_api_key"
            export TAVILY_API_KEY="your_tavily_api_key"

---

## 🔹 Usage

Run the CLI demo:
            python -m examples.demo_cli "Your query here"
Example:
            python -m examples.demo_cli "What's new in Python 3.13?"
The agent will process your query, optionally call tools, and provide a step-by-step response with citations.
