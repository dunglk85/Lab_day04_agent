"""Backward-compatible exports for tests and existing imports.

Main orchestration now lives in `src.agent.graph_builder`.
"""

from src.agent.graph_builder import (  # noqa: F401
    AgentState,
    SYSTEM_PROMPT,
    agent_node,
    build_graph,
    llm,
    llm_with_tools,
    tools_list,
)

# Keep the old module-level `graph` symbol for existing test code.
graph = build_graph()


if __name__ == "__main__":
    from src.agent.cli import run_cli

    run_cli()
