"""
Configuration Management - Building Block: ConfigurationManager

Purpose:
    Loads and manages configuration from config.yaml and .env files.
    Provides centralized configuration access for all components.

Input Data:
    - config.yaml file
    - .env file (environment variables)

Output Data:
    - Configuration objects with settings

Setup/Configuration:
    - CONFIG_DIR environment variable (default: ./config)

References:
    - config.yaml: Full configuration specification
    - .env.example: Environment variable template
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """
    Configuration settings loaded from config.yaml and .env.

    Usage:
        >>> from my_project.config.settings import settings
        >>> print(settings.player_id)
        'P01'
        >>> print(settings.strategy_mode)
        'hybrid'
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize settings.

        Args:
            config_path: Path to config.yaml (default: ./config/config.yaml)
        """
        # Find config file
        if config_path is None:
            # Look in several locations
            possible_paths = [
                Path("config/config.yaml"),
                Path(__file__).parent.parent.parent / "config" / "config.yaml",
            ]
            for path in possible_paths:
                if path.exists():
                    config_path = str(path)
                    break

        # Load config.yaml if available
        self.config_data: Dict[str, Any] = {}
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                self.config_data = yaml.safe_load(f) or {}

    # Player Configuration
    @property
    def player_id(self) -> str:
        return os.getenv("PLAYER_ID", self.config_data.get("player", {}).get("id", "P01"))

    @property
    def display_name(self) -> str:
        return os.getenv("PLAYER_DISPLAY_NAME", self.config_data.get("player", {}).get("display_name", "Player"))

    # Strategy Configuration
    @property
    def strategy_mode(self) -> str:
        return os.getenv("STRATEGY_MODE", self.config_data.get("strategy", {}).get("mode", "hybrid"))

    @property
    def gemini_model_id(self) -> str:
        return os.getenv("GEMINI_MODEL_ID", self.config_data.get("strategy", {}).get("llm", {}).get("model_id", "gemini-2.0-flash-exp"))

    @property
    def gemini_temperature(self) -> float:
        return float(os.getenv("GEMINI_TEMPERATURE", self.config_data.get("strategy", {}).get("llm", {}).get("temperature", 0.7)))

    # League Configuration
    @property
    def league_manager_host(self) -> str:
        return os.getenv("LEAGUE_MANAGER_HOST", self.config_data.get("league", {}).get("manager", {}).get("host", "localhost"))

    @property
    def league_manager_port(self) -> int:
        return int(os.getenv("LEAGUE_MANAGER_PORT", self.config_data.get("league", {}).get("manager", {}).get("port", 8000)))

    @property
    def player_agent_port(self) -> int:
        return int(os.getenv("PLAYER_AGENT_PORT", self.config_data.get("league", {}).get("agent", {}).get("port", 8101)))

    # Logging Configuration
    @property
    def log_level(self) -> str:
        return os.getenv("LOG_LEVEL", self.config_data.get("logging", {}).get("level", "INFO"))

    @property
    def log_format(self) -> str:
        return os.getenv("LOG_FORMAT", self.config_data.get("logging", {}).get("format", "json"))


# Global settings instance
settings = Settings()
