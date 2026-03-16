# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

Uses `uv` for package management and virtual environments.

```bash
uv venv && source .venv/bin/activate && uv pip install -e .
```

## Commands

```bash
uv run main.py        # Start the MCP server
uv run pytest         # Run all tests
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx  # Run a single test
```

## Architecture

This is a **FastMCP server** that exposes Python functions as MCP tools callable by Claude.

- `main.py` — Entry point. Creates a `FastMCP` instance, registers tools via `mcp.tool()`, and runs the server.
- `tools/` — Each file contains plain Python functions. Register a function as a tool by calling `mcp.tool()(fn)` in `main.py`.
- `tools/document.py` — Converts binary DOCX/PDF data to Markdown using `markitdown`.
- `tools/math.py` — Example addition tool.

## Tool Definition Pattern

Tools are plain functions with Pydantic `Field` descriptions on parameters and a structured docstring:

```python
from pydantic import Field

def my_tool(
    param: str = Field(description="What this parameter does"),
) -> str:
    """One-line summary.

    Longer description.

    When to use:
    - bullet points

    Examples:
    >>> my_tool("foo")
    'result'
    """
    ...
```

The docstring and `Field` descriptions are surfaced to Claude as tool documentation, so they should be precise and informative.
