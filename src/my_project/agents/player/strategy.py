"""
Strategy Engine - Building Block: StrategyEngine

Purpose:
    Implements parity choice strategies using Agno framework with Gemini LLM.
    Provides random baseline, LLM-based reasoning, and hybrid fallback approaches.

Input Data:
    - context (dict): Game context with opponent, standings, match history
    - mode (str): Strategy mode ("random", "llm", "hybrid")

Output Data:
    - parity_choice (str): lowercase "even" or "odd"
    - reasoning (str): Explanation of choice (LLM mode only)

Setup/Configuration:
    - gemini_model_id: Gemini model to use (from config.yaml)
    - temperature: LLM temperature (0.0-1.0)
    - timeout: Maximum time for LLM response
    - system_prompt: Instructions for Gemini

CRITICAL:
    - Output MUST be lowercase: "even" or "odd"
    - Timeout MUST be < 30 seconds (use 25s for 5s buffer)
    - Fallback to random if LLM fails or times out

References:
    - CLAUDE.md: Lines 943-1089 (Assignment Requirements - choose_parity timeout)
    - CLAUDE.md: Lines 1920-1940 (Pitfall #2 - Parity Choice Capitalized)
    - config.yaml: strategy section
"""

import random
import asyncio
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import os

try:
    from agno.agent import Agent
    from agno.models.google import Gemini
    AGNO_AVAILABLE = True
except ImportError:
    AGNO_AVAILABLE = False

from ...utils.logger import setup_logger

logger = setup_logger(__name__)


class ParityChoice(BaseModel):
    """
    Structured output schema for Gemini LLM.

    This ensures the LLM always returns lowercase parity choices.
    Pydantic validation prevents capitalization errors.
    """
    choice: str = Field(
        ...,
        description="Parity choice - MUST be lowercase 'even' or 'odd'",
        pattern="^(even|odd)$"  # Regex validation for lowercase only
    )
    reasoning: str = Field(
        ...,
        description="Brief explanation of why this choice was made"
    )


class StrategyEngine:
    """
    Parity choice strategy engine with Agno+Gemini integration.

    This building block provides three strategy modes:
    1. **Random**: Fast, reliable baseline - random.choice(["even", "odd"])
    2. **LLM**: Gemini-powered reasoning (interesting but won't improve win rate)
    3. **Hybrid**: LLM with timeout fallback to random (RECOMMENDED)

    The hybrid mode provides the best of both worlds:
    - Uses Gemini when possible for interesting reasoning
    - Falls back to random if LLM times out or fails
    - Ensures we always respond within 30-second timeout

    Example:
        >>> engine = StrategyEngine(mode="hybrid")
        >>> context = {
        ...     "opponent": "P02",
        ...     "standings": {...},
        ...     "history": [...]
        ... }
        >>> choice = await engine.choose_parity(context)
        >>> print(choice)  # Always lowercase
        'even'
    """

    def __init__(
        self,
        mode: str = "hybrid",
        gemini_model_id: str = "gemini-2.0-flash-exp",
        temperature: float = 0.7,
        max_output_tokens: int = 100,
        llm_timeout: int = 25,  # 5-second buffer from 30s protocol timeout
        system_prompt: Optional[str] = None
    ):
        """
        Initialize the strategy engine.

        Args:
            mode: Strategy mode - "random", "llm", or "hybrid"
            gemini_model_id: Gemini model ID (default: free tier flash model)
            temperature: LLM temperature 0.0 (deterministic) to 1.0 (creative)
            max_output_tokens: Maximum response length
            llm_timeout: Timeout for LLM response in seconds (MUST be < 30)
            system_prompt: Optional custom system prompt (uses default if None)

        Raises:
            ValueError: If mode is invalid or llm_timeout >= 30
            ImportError: If Agno is not installed and mode requires LLM
        """
        if mode not in ["random", "llm", "hybrid"]:
            raise ValueError(f"Invalid mode: {mode}. Must be 'random', 'llm', or 'hybrid'")

        if llm_timeout >= 30:
            raise ValueError(
                f"llm_timeout must be < 30 seconds (protocol limit), got {llm_timeout}. "
                "Recommended: 25s for 5-second buffer."
            )

        self.mode = mode
        self.llm_timeout = llm_timeout

        # Initialize Agno agent if LLM mode enabled
        self.agent: Optional[Agent] = None
        if mode in ["llm", "hybrid"]:
            if not AGNO_AVAILABLE:
                raise ImportError(
                    "Agno framework not installed. "
                    "Install with: pip install agno>=0.59.0"
                )

            # Get API key from environment
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key or api_key == "your_google_gemini_api_key_here":
                logger.warning(
                    "GOOGLE_API_KEY not set in .env file. "
                    "LLM strategy will fall back to random. "
                    "Get your free API key from: https://aistudio.google.com/apikey"
                )
                if mode == "llm":
                    # LLM-only mode requires API key
                    raise ValueError(
                        "GOOGLE_API_KEY required for 'llm' mode. "
                        "Set in .env file or use 'hybrid' mode for fallback."
                    )
            else:
                # Initialize Agno agent with Gemini
                self.agent = self._create_agent(
                    gemini_model_id,
                    temperature,
                    max_output_tokens,
                    system_prompt
                )

        logger.info(f"StrategyEngine initialized - mode={mode}, llm_enabled={self.agent is not None}")

    def _create_agent(
        self,
        model_id: str,
        temperature: float,
        max_output_tokens: int,
        system_prompt: Optional[str]
    ) -> Agent:
        """
        Create Agno agent with Gemini model.

        Args:
            model_id: Gemini model ID
            temperature: LLM temperature
            max_output_tokens: Max response tokens
            system_prompt: System instructions

        Returns:
            Agent: Configured Agno agent
        """
        if system_prompt is None:
            system_prompt = self._get_default_system_prompt()

        agent = Agent(
            model=Gemini(
                id=model_id,
                temperature=temperature,
                max_output_tokens=max_output_tokens
            ),
            output_schema=ParityChoice,  # Ensures structured output
            instructions=system_prompt,
            markdown=False  # We want structured JSON output
        )

        return agent

    def _get_default_system_prompt(self) -> str:
        """
        Get default system prompt for Gemini.

        Returns:
            str: System prompt with game rules and requirements
        """
        return """You are an AI agent playing the Even/Odd game.

**Game Rules:**
- Two players simultaneously choose "even" or "odd"
- Referee draws a random number from 1-10
- You win if the number's parity matches your choice
- Scoring: Win = 3 points, Draw = 1 point, Loss = 0 points

**Your Task:**
Choose "even" or "odd" for the current match.

**CRITICAL REQUIREMENTS:**
1. Your choice MUST be lowercase: "even" or "odd" (NEVER "Even", "ODD", etc.)
2. Provide brief reasoning for your choice (1-2 sentences)
3. Consider game context: opponent patterns, standings, match history

**Important Note:**
This is a pure luck game. Your strategy won't statistically improve win rate,
but interesting reasoning makes for better documentation and analysis!

**Output Format:**
{
    "choice": "even",  // MUST be lowercase
    "reasoning": "Your explanation here"
}
"""

    async def choose_parity(self, context: Dict[str, Any]) -> str:
        """
        Choose parity ("even" or "odd") based on game context.

        This is the main method called by handlers.py when handling
        CHOOSE_PARITY_CALL from Referee.

        Args:
            context: Game context dictionary with:
                - opponent (str): Opponent player ID
                - standings (dict): Current league standings
                - history (list): Match history
                - deadline (str): ISO-8601 timestamp deadline

        Returns:
            str: Parity choice - ALWAYS lowercase "even" or "odd"

        Example:
            >>> context = {
            ...     "opponent": "P02",
            ...     "standings": {"P01": 6, "P02": 3},
            ...     "history": [...]
            ... }
            >>> choice = await engine.choose_parity(context)
            >>> assert choice in ["even", "odd"]

        CRITICAL:
            - MUST return within 30 seconds (we use 25s timeout for buffer)
            - MUST return lowercase "even" or "odd"
            - Falls back to random if LLM fails or times out
        """
        logger.info(f"Choosing parity - mode={self.mode}, opponent={context.get('opponent')}")

        try:
            if self.mode == "random":
                return self._random_choice()

            if self.mode in ["llm", "hybrid"]:
                # Try LLM with timeout
                try:
                    choice = await asyncio.wait_for(
                        self._llm_choice(context),
                        timeout=self.llm_timeout
                    )
                    logger.info(
                        f"LLM choice made",
                        choice=choice,
                        elapsed=f"<{self.llm_timeout}s"
                    )
                    return choice
                except asyncio.TimeoutError:
                    logger.warning(
                        f"LLM timeout - falling back to random",
                        timeout_seconds=self.llm_timeout
                    )
                    return self._random_choice()
                except Exception as e:
                    logger.error(f"LLM error - falling back to random: {str(e)}")
                    if self.mode == "llm":
                        # LLM-only mode: re-raise error
                        raise
                    # Hybrid mode: fall back to random
                    return self._random_choice()

        except Exception as e:
            logger.error(f"Strategy error - using random fallback: {str(e)}")
            return self._random_choice()

    def _random_choice(self) -> str:
        """
        Make random parity choice.

        Returns:
            str: Randomly chosen "even" or "odd"

        Note:
            This is the baseline strategy. Fast, reliable, and optimal
            for a pure luck game (50% win rate expected).
        """
        choice = random.choice(["even", "odd"])
        logger.debug(f"Random choice: {choice}")
        return choice

    async def _llm_choice(self, context: Dict[str, Any]) -> str:
        """
        Make LLM-powered parity choice using Gemini.

        Args:
            context: Game context with opponent, standings, history

        Returns:
            str: LLM-chosen parity (lowercase "even" or "odd")

        Raises:
            Exception: If LLM call fails
            asyncio.TimeoutError: If LLM takes too long
        """
        if not self.agent:
            raise RuntimeError("Agent not initialized. Check GOOGLE_API_KEY in .env")

        # Format context for LLM
        prompt = self._format_context_prompt(context)

        # Call Gemini via Agno
        # The output_schema (ParityChoice) ensures we get structured output
        response = await self.agent.arun(prompt)

        # Extract choice from structured response
        # Pydantic validation ensures it's lowercase "even" or "odd"
        if hasattr(response, 'content'):
            # Agno returns response object
            result = response.content
            if isinstance(result, ParityChoice):
                choice = result.choice
                reasoning = result.reasoning
            elif isinstance(result, dict):
                choice = result.get("choice", "even")
                reasoning = result.get("reasoning", "No reasoning provided")
            else:
                # Fallback parsing
                choice = str(result).lower()
                if choice not in ["even", "odd"]:
                    raise ValueError(f"Invalid LLM output: {result}")
                reasoning = "Parsed from text response"
        else:
            # Direct response
            choice = response.choice if hasattr(response, 'choice') else "even"
            reasoning = response.reasoning if hasattr(response, 'reasoning') else "Unknown"

        # Log reasoning
        logger.info(f"LLM reasoning - choice={choice}, reasoning={reasoning}")

        # Final validation
        if choice not in ["even", "odd"]:
            logger.error(f"Invalid LLM choice: {choice}. Using random fallback.")
            return self._random_choice()

        return choice

    def _format_context_prompt(self, context: Dict[str, Any]) -> str:
        """
        Format game context into prompt for LLM.

        Args:
            context: Game context dictionary

        Returns:
            str: Formatted prompt with context
        """
        opponent = context.get("opponent", "unknown")
        standings = context.get("standings", {})
        history = context.get("history", [])

        prompt = f"Make your parity choice for the current match.\n\n"
        prompt += f"**Opponent:** {opponent}\n\n"

        if standings:
            prompt += "**Current Standings:**\n"
            for player, points in standings.items():
                prompt += f"- {player}: {points} points\n"
            prompt += "\n"

        if history:
            prompt += "**Recent Match History:**\n"
            for i, match in enumerate(history[-5:], 1):  # Last 5 matches
                prompt += f"{i}. vs {match.get('opponent_id')}: "
                prompt += f"You chose {match.get('player_choice')}, "
                prompt += f"result: {match.get('result')}\n"
            prompt += "\n"

        prompt += "Choose 'even' or 'odd' and explain your reasoning."

        return prompt


# Convenience functions
async def choose_parity_random() -> str:
    """
    Quick random parity choice.

    Returns:
        str: "even" or "odd"
    """
    return random.choice(["even", "odd"])
