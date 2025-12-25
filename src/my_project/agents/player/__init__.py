"""
Player Agent Package

This package contains the implementation of the Even/Odd League Player Agent.

Components:
    - main.py: Entry point and CLI
    - server.py: FastAPI HTTP server (MCPProtocolHandler)
    - handlers.py: MCP tool implementations (ToolHandlers)
    - strategy.py: Parity choice strategy (StrategyEngine)
    - state.py: Player state management (PlayerState)

Usage:
    python -m my_project.agents.player.main --port 8101 --strategy hybrid
"""

__all__ = ["PlayerState", "StrategyEngine", "ToolHandlers", "create_app"]
