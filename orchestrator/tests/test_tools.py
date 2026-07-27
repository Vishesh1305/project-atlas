from atlas.tools.calculate import CalculateTool


def test_run_invalid_input_returns_error_not_raises() -> None:
    tool = CalculateTool()
    result = tool.run({})
    assert "Invalid input" in result
