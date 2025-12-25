"""
Player Agent Entry Point

Usage:
    python -m my_project.agents.player.main --port 8101 --strategy hybrid

    Or directly:
    python src/my_project/agents/player/main.py --port 8101

Arguments:
    --port: Server port (8101-8104, default: 8101)
    --display-name: Player display name (default: "Gemini Agent")
    --strategy: Strategy mode - random/llm/hybrid (default: hybrid)
    --player-id: Player ID (default: P01)
    --host: Server host (default: localhost)
    --debug: Enable debug logging

Example:
    # Run with hybrid strategy on port 8101
    python -m my_project.agents.player.main --port 8101 --strategy hybrid

    # Run with random strategy (fast and reliable)
    python -m my_project.agents.player.main --port 8102 --strategy random

    # Run with LLM-only strategy
    python -m my_project.agents.player.main --port 8103 --strategy llm --debug
"""

import argparse
import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import uvicorn
from dotenv import load_dotenv

from my_project.agents.player.state import PlayerState
from my_project.agents.player.strategy import StrategyEngine
from my_project.agents.player.handlers import ToolHandlers
from my_project.agents.player.server import create_app
from my_project.utils.logger import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Even/Odd League Player Agent with Agno+Gemini",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PLAYER_AGENT_PORT", 8101)),
        help="Server port (8101-8104)"
    )

    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Server host"
    )

    parser.add_argument(
        "--player-id",
        type=str,
        default=os.getenv("PLAYER_ID", "P01"),
        help="Player ID (P01-P99)"
    )

    parser.add_argument(
        "--display-name",
        type=str,
        default=os.getenv("PLAYER_DISPLAY_NAME", "Gemini Agent"),
        help="Player display name"
    )

    parser.add_argument(
        "--strategy",
        type=str,
        choices=["random", "llm", "hybrid"],
        default=os.getenv("STRATEGY_MODE", "hybrid"),
        help="Strategy mode: random (fast), llm (Gemini), hybrid (recommended)"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        default=os.getenv("DEBUG", "False").lower() == "true",
        help="Enable debug logging"
    )

    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload on code changes (development only)"
    )

    return parser.parse_args()


def validate_environment():
    """
    Validate required environment variables.

    Raises:
        SystemExit: If critical environment variables are missing
    """
    # Check for API key if using LLM strategy
    strategy_mode = os.getenv("STRATEGY_MODE", "hybrid")
    if strategy_mode in ["llm", "hybrid"]:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_google_gemini_api_key_here":
            logger.warning(
                "=" * 60 +
                "\nWARNING: GOOGLE_API_KEY not set in .env file!\n" +
                "=" * 60 +
                "\n\nThe LLM strategy will NOT work without an API key.\n" +
                "Get your FREE API key from: https://aistudio.google.com/apikey\n" +
                "Then add it to your .env file:\n" +
                "  GOOGLE_API_KEY=your_actual_key_here\n\n" +
                "For now, the agent will fall back to random strategy.\n" +
                "=" * 60
            )


def main():
    """Main entry point."""
    args = parse_args()

    # Validate environment
    validate_environment()

    # Set up logging
    log_level = "DEBUG" if args.debug else os.getenv("LOG_LEVEL", "INFO")
    global logger
    logger = setup_logger(
        __name__,
        level=log_level,
        agent_id=args.player_id,
        log_format=os.getenv("LOG_FORMAT", "json")
    )

    logger.info(
        "=" * 60 +
        "\n🎮 Starting Even/Odd League Player Agent\n" +
        "=" * 60,
        player_id=args.player_id,
        display_name=args.display_name,
        port=args.port,
        strategy=args.strategy,
        host=args.host
    )

    try:
        # Initialize components
        logger.info("Initializing PlayerState...")
        state = PlayerState(
            player_id=args.player_id,
            display_name=args.display_name,
            max_history_entries=100,
            persistence_enabled=False  # Can be configured via config.yaml later
        )

        logger.info(f"Initializing StrategyEngine (mode: {args.strategy})...")
        strategy = StrategyEngine(
            mode=args.strategy,
            gemini_model_id=os.getenv("GEMINI_MODEL_ID", "gemini-2.0-flash-exp"),
            temperature=float(os.getenv("GEMINI_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("GEMINI_MAX_TOKENS", "100")),
            llm_timeout=int(os.getenv("LLM_TIMEOUT", "25"))
        )

        logger.info("Initializing ToolHandlers...")
        handlers = ToolHandlers(state, strategy)

        logger.info("Creating FastAPI application...")
        app = create_app(handlers)

        logger.info(
            "\n" + "=" * 60 +
            f"\n✅ Player Agent ready!\n" +
            "=" * 60 +
            f"\n\nServer running at: http://{args.host}:{args.port}\n" +
            f"MCP Endpoint: http://{args.host}:{args.port}/mcp\n" +
            f"API Docs: http://{args.host}:{args.port}/docs\n" +
            f"Health Check: http://{args.host}:{args.port}/health\n" +
            f"Player Stats: http://{args.host}:{args.port}/stats\n\n" +
            f"Player ID: {args.player_id}\n" +
            f"Display Name: {args.display_name}\n" +
            f"Strategy: {args.strategy}\n\n" +
            "Press CTRL+C to stop\n" +
            "=" * 60
        )

        # Run server
        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            log_level=log_level.lower(),
            reload=args.reload,
            access_log=args.debug
        )

    except KeyboardInterrupt:
        logger.info("\n\nShutting down gracefully...")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Fatal error starting server", error=str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
