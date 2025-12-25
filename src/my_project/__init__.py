"""
Even/Odd League Player Agent Package
=====================================

A production-ready AI Player Agent for the Even/Odd League using:
- FastAPI for HTTP server and MCP protocol compliance
- Agno framework with Google Gemini for AI-powered strategy
- Comprehensive state management and logging

Main Components:
- agents.player: Player Agent implementation with MCP tools
- core: Protocol message builders and registration client
- utils: Timestamp utilities and structured logging
- config: Configuration management

Usage:
    # Run the player agent
    python -m my_project.agents.player.main --port 8101 --strategy hybrid

    # Or import and use programmatically
    from my_project import PlayerState, StrategyEngine, create_app
"""

__version__ = "0.1.0"
__author__ = "Lior Livyatan"

# Export main public interfaces
from .agents.player.state import PlayerState
from .agents.player.strategy import StrategyEngine
from .agents.player.handlers import ToolHandlers
from .agents.player.server import create_app
from .core.protocol import ProtocolMessageBuilder
from .core.registration import RegistrationClient
from .utils.timestamp import TimestampUtil, utc_now
from .utils.logger import setup_logger
from .config.settings import settings

__all__ = [
    "PlayerState",
    "StrategyEngine",
    "ToolHandlers",
    "create_app",
    "ProtocolMessageBuilder",
    "RegistrationClient",
    "TimestampUtil",
    "utc_now",
    "setup_logger",
    "settings",
]
