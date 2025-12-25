"""
Structured Logging - Building Block: StructuredLogger

Purpose:
    Provides JSON-formatted structured logging for the Player Agent.
    Ensures consistent, machine-readable logs for debugging and analysis.

Input Data:
    - logger_name (str): Name of the logger (typically module name)
    - log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - message (str): Log message
    - context (dict): Additional context data

Output Data:
    - JSON-formatted log entries with timestamp, level, agent_id, message, context
    - Log files with rotation (if file logging enabled)

Setup/Configuration:
    - log_level: Minimum log level (from .env or config.yaml)
    - log_format: "json" or "text" (from .env or config.yaml)
    - file_path: Log file path (from config.yaml)

References:
    - Assignment Chapter 9: League Data Protocol (logs/ directory structure)
    - Assignment Chapter 10: Python Toolkit (JsonLogger)
    - config.yaml: logging section
"""

import logging
import sys
import json
from typing import Any, Optional, Dict
from pathlib import Path
from datetime import datetime, timezone

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False


class StructuredLogger:
    """
    Structured logging with JSON output format.

    This building block provides:
    1. JSON-formatted logs with consistent structure
    2. Automatic timestamp injection (UTC)
    3. Agent ID tagging for multi-agent environments
    4. Context enrichment (add arbitrary key-value pairs)
    5. File rotation support

    Example:
        >>> logger = StructuredLogger.setup_logger(
        ...     name="player_agent",
        ...     level="INFO",
        ...     agent_id="P01"
        ... )
        >>> logger.info("Game started", match_id="R1M1", opponent="P02")

        Output (JSON):
        {
            "timestamp": "2025-01-15T10:30:00.123456Z",
            "level": "INFO",
            "agent_id": "P01",
            "logger": "player_agent",
            "message": "Game started",
            "match_id": "R1M1",
            "opponent": "P02"
        }
    """

    _initialized_loggers: Dict[str, logging.Logger] = {}

    @staticmethod
    def setup_logger(
        name: str,
        level: str = "INFO",
        agent_id: Optional[str] = None,
        log_format: str = "json",
        log_file: Optional[str] = None,
        max_file_size_mb: int = 10,
        backup_count: int = 5
    ) -> logging.Logger:
        """
        Set up a structured logger instance.

        Args:
            name: Logger name (typically __name__ of the module)
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            agent_id: Player agent ID (e.g., "P01") for tagging
            log_format: "json" or "text" (default: json)
            log_file: Optional file path for file logging
            max_file_size_mb: Max size of log file before rotation
            backup_count: Number of backup files to keep

        Returns:
            logging.Logger: Configured logger instance

        Example:
            >>> logger = StructuredLogger.setup_logger(
            ...     name=__name__,
            ...     level="DEBUG",
            ...     agent_id="P01",
            ...     log_file="./logs/player.log"
            ... )
        """
        # Return cached logger if already initialized
        cache_key = f"{name}_{agent_id}_{log_format}"
        if cache_key in StructuredLogger._initialized_loggers:
            return StructuredLogger._initialized_loggers[cache_key]

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        logger.propagate = False

        # Clear existing handlers
        logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))

        if log_format == "json":
            formatter = StructuredLogger._get_json_formatter(agent_id)
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%dT%H:%M:%SZ'
            )

        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (if specified)
        if log_file:
            from logging.handlers import RotatingFileHandler

            # Create log directory if it doesn't exist
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_file_size_mb * 1024 * 1024,  # Convert MB to bytes
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(getattr(logging, level.upper()))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # Cache logger
        StructuredLogger._initialized_loggers[cache_key] = logger

        return logger

    @staticmethod
    def _get_json_formatter(agent_id: Optional[str] = None) -> logging.Formatter:
        """
        Create a JSON formatter for structured logging.

        Args:
            agent_id: Optional agent ID to include in all log entries

        Returns:
            logging.Formatter: Formatter that outputs JSON

        """
        class JSONFormatter(logging.Formatter):
            def __init__(self, agent_id: Optional[str] = None):
                super().__init__()
                self.agent_id = agent_id

            def format(self, record: logging.LogRecord) -> str:
                log_data = {
                    "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                    "level": record.levelname,
                    "logger": record.name,
                    "message": record.getMessage(),
                }

                # Add agent_id if specified
                if self.agent_id:
                    log_data["agent_id"] = self.agent_id

                # Add exception info if present
                if record.exc_info:
                    log_data["exception"] = self.formatException(record.exc_info)

                # Add any extra fields from record.__dict__
                extras = {
                    k: v for k, v in record.__dict__.items()
                    if k not in [
                        'name', 'msg', 'args', 'created', 'filename', 'funcName',
                        'levelname', 'levelno', 'lineno', 'module', 'msecs',
                        'message', 'pathname', 'process', 'processName', 'relativeCreated',
                        'thread', 'threadName', 'exc_info', 'exc_text', 'stack_info',
                        'getMessage', 'taskName'
                    ]
                }

                if extras:
                    log_data.update(extras)

                return json.dumps(log_data, ensure_ascii=False)

        return JSONFormatter(agent_id)

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get an existing logger or create a basic one.

        Args:
            name: Logger name

        Returns:
            logging.Logger: Logger instance

        Note:
            This returns a logger even if not previously set up.
            For structured logging, use setup_logger() first.
        """
        return logging.getLogger(name)


def setup_logger(
    name: str,
    level: str = "INFO",
    agent_id: Optional[str] = None,
    **kwargs
) -> logging.Logger:
    """
    Convenience function to set up a structured logger.

    Args:
        name: Logger name (use __name__ for current module)
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        agent_id: Player agent ID (e.g., "P01")
        **kwargs: Additional arguments passed to StructuredLogger.setup_logger()

    Returns:
        logging.Logger: Configured logger

    Example:
        >>> from my_project.utils.logger import setup_logger
        >>> logger = setup_logger(__name__, level="DEBUG", agent_id="P01")
        >>> logger.info("Agent started", port=8101)
    """
    return StructuredLogger.setup_logger(name, level, agent_id, **kwargs)


def log_with_context(
    logger: logging.Logger,
    level: str,
    message: str,
    **context
) -> None:
    """
    Log a message with additional context fields.

    Args:
        logger: Logger instance
        level: Log level (debug, info, warning, error, critical)
        message: Log message
        **context: Additional key-value pairs to include in log

    Example:
        >>> logger = setup_logger(__name__)
        >>> log_with_context(
        ...     logger, "info", "Parity chosen",
        ...     match_id="R1M1", choice="even", strategy="llm"
        ... )
    """
    log_method = getattr(logger, level.lower())
    log_method(message, extra=context)


# Example usage demonstration
if __name__ == "__main__":
    # Example 1: Basic JSON logging
    logger = setup_logger(
        name="example",
        level="INFO",
        agent_id="P01",
        log_format="json"
    )

    logger.info("Player agent started", port=8101, strategy="hybrid")
    logger.warning("LLM timeout", timeout_seconds=30, elapsed=32)
    logger.error("Connection failed", host="localhost", port=8000)

    # Example 2: Logging with context
    log_with_context(
        logger, "info", "Match completed",
        match_id="R1M1",
        result="win",
        points=3,
        opponent="P02"
    )

    # Example 3: File logging
    file_logger = setup_logger(
        name="file_example",
        level="DEBUG",
        agent_id="P01",
        log_file="./logs/player.log",
        max_file_size_mb=5,
        backup_count=3
    )

    file_logger.debug("This goes to both console and file")
