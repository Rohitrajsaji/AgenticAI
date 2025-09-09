from agentic_ai.tools import tool_calculator


def test_calculator_basic():
    assert tool_calculator("2+2") == "4"
    assert tool_calculator("10/5") == "2.0"
    assert "Error" in tool_calculator("__import__('os').system('rm -rf /')")
