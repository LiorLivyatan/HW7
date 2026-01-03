"""
MCP Tool Handlers - Building Block: ToolHandlers

Purpose:
    Implements the 3 required MCP tools for the Player Agent:
    1. handle_game_invitation - Respond to game invitations (≤5s)
    2. choose_parity - Choose "even" or "odd" (≤30s)
    3. notify_match_result - Process match results (≤10s)

Input Data:
    - MCP tool call parameters (conversation_id, match_id, etc.)
    - Game context from messages

Output Data:
    - Protocol-compliant response messages
    - State updates (match history, statistics)

Setup/Configuration:
    - PlayerState instance
    - StrategyEngine instance
    - ProtocolMessageBuilder instance

CRITICAL:
    - All responses MUST include exact JSON structure from Chapter 4
    - Timeouts MUST be respected (5s, 30s, 10s)
    - All timestamps MUST be UTC with 'Z'
    - parity_choice MUST be lowercase

References:
    - CLAUDE.md: Lines 943-1089 (Assignment Requirements)
    - Assignment Chapter 3: Even/Odd Game Flow
    - Assignment Chapter 4: JSON Message Structures
    - Assignment Chapter 5: Implementation Guide (tool implementations)
"""

from typing import Dict, Any
import asyncio
import time

from .state import PlayerState
from .strategy import StrategyEngine
from ...core.protocol import ProtocolMessageBuilder
from ...utils.logger import setup_logger
from ...utils.timestamp import utc_now
from ...utils.console import (
    print_game_invitation,
    print_parity_thinking,
    print_parity_choice,
    print_match_result,
    print_stats_summary,
    print_error
)

logger = setup_logger(__name__)


class ToolHandlers:
    """
    MCP tool implementations for Player Agent.

    This building block provides the 3 required tools:
    1. handle_game_invitation - Accepts/rejects game invitations
    2. choose_parity - Makes parity choice using strategy engine
    3. notify_match_result - Updates state based on match results

    Each handler ensures:
    - Protocol compliance (exact JSON structure)
    - Timeout compliance (within required limits)
    - State management (updates PlayerState)
    - Logging (structured logs for all operations)

    Example:
        >>> state = PlayerState(player_id="P01")
        >>> strategy = StrategyEngine(mode="hybrid")
        >>> handlers = ToolHandlers(state, strategy)
        >>>
        >>> # Handle invitation
        >>> result = await handlers.handle_game_invitation({
        ...     "conversation_id": "conv-001",
        ...     "match_id": "R1M1",
        ...     "opponent_id": "P02"
        ... })
    """

    def __init__(
        self,
        state: PlayerState,
        strategy: StrategyEngine
    ):
        """
        Initialize tool handlers.

        Args:
            state: PlayerState instance for managing player data
            strategy: StrategyEngine instance for parity choices

        Raises:
            ValueError: If state or strategy is None
        """
        if not state:
            raise ValueError("state cannot be None")
        if not strategy:
            raise ValueError("strategy cannot be None")

        self.state = state
        self.strategy = strategy

        # Initialize protocol message builder
        self.protocol = ProtocolMessageBuilder(player_id=state.player_id)

        # Set auth token if already registered
        if state.auth_token:
            self.protocol.set_auth_token(state.auth_token)

        logger.info(f"ToolHandlers initialized - player_id={state.player_id}, strategy_mode={strategy.mode}")

    async def handle_game_invitation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle GAME_INVITATION message from Referee.

        MCP Tool: handle_game_invitation
        Timeout: ≤5 seconds
        Message Type: GAME_JOIN_ACK

        This is called when the Referee invites the player to a match.
        The player must respond within 5 seconds with acceptance/rejection.

        Args:
            params: GAME_INVITATION message parameters
                - conversation_id (str): Conversation ID
                - match_id (str): Match identifier
                - opponent_id (str): Opponent player ID
                - game_type (str): "even_odd"
                - deadline (str): ISO-8601 deadline timestamp

        Returns:
            dict: GAME_JOIN_ACK message

        Example params:
            {
                "conversation_id": "conv-game-001",
                "match_id": "R1M1",
                "opponent_id": "P02",
                "game_type": "even_odd",
                "deadline": "2025-01-15T10:30:05.000000Z"
            }

        Example response:
            {
                "protocol": "league.v2",
                "message_type": "GAME_JOIN_ACK",
                "sender": "player:P01",
                "timestamp": "2025-01-15T10:30:00.123456Z",
                "conversation_id": "conv-game-001",
                "auth_token": "token-12345",
                "match_id": "R1M1",
                "player_id": "P01",
                "arrival_timestamp": "2025-01-15T10:30:00.123456Z",
                "accept": true
            }

        CRITICAL:
            - MUST respond within 5 seconds
            - MUST include auth_token
            - arrival_timestamp MUST be UTC with 'Z'

        See Also:
            Assignment Chapter 4: GAME_JOIN_ACK structure
            config.yaml: timeouts.game_invitation_response = 5
        """
        start_time = time.time()
        conversation_id = params.get("conversation_id", "unknown")
        match_id = params.get("match_id", "unknown")
        opponent_id = params.get("opponent_id", "unknown")
        game_type = params.get("game_type", "even_odd")
        deadline = params.get("deadline", "")

        logger.info(f"Game invitation received - match_id={match_id}, opponent_id={opponent_id}, deadline={deadline}")

        try:
            # Update auth token in protocol builder if state was registered
            if self.state.auth_token and not self.protocol.auth_token:
                self.protocol.set_auth_token(self.state.auth_token)

            # Build GAME_JOIN_ACK response
            # Default: always accept invitations
            response = self.protocol.build_game_join_ack(
                conversation_id=conversation_id,
                match_id=match_id,
                accept=True
            )

            # Calculate response time
            response_time = time.time() - start_time

            # Display invitation with rich formatting
            print_game_invitation(
                match_id=match_id,
                opponent_id=opponent_id,
                game_type=game_type,
                deadline=deadline,
                accepted=True,
                response_time=response_time
            )

            logger.info(f"Game invitation accepted - match_id={match_id}, response_time={response_time:.2f}s, accepted=True")

            return response

        except Exception as e:
            logger.error(f"Error handling game invitation - match_id={match_id}, error={str(e)}")
            raise

    async def choose_parity(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle CHOOSE_PARITY_CALL message from Referee.

        MCP Tool: choose_parity
        Timeout: ≤30 seconds
        Message Type: CHOOSE_PARITY_RESPONSE

        This is called when the Referee asks the player to choose parity.
        The player must respond within 30 seconds with "even" or "odd" (lowercase).

        Args:
            params: CHOOSE_PARITY_CALL message parameters
                - conversation_id (str): Conversation ID
                - match_id (str): Match identifier
                - opponent_id (str): Opponent player ID (optional)
                - standings (dict): Current standings (optional)
                - deadline (str): ISO-8601 deadline timestamp

        Returns:
            dict: CHOOSE_PARITY_RESPONSE message

        Example params:
            {
                "conversation_id": "conv-choice-001",
                "match_id": "R1M1",
                "opponent_id": "P02",
                "standings": {"P01": 3, "P02": 6, "P03": 0, "P04": 3},
                "deadline": "2025-01-15T10:30:30.000000Z"
            }

        Example response:
            {
                "protocol": "league.v2",
                "message_type": "CHOOSE_PARITY_RESPONSE",
                "sender": "player:P01",
                "timestamp": "2025-01-15T10:30:05.123456Z",
                "conversation_id": "conv-choice-001",
                "auth_token": "token-12345",
                "match_id": "R1M1",
                "player_id": "P01",
                "parity_choice": "even"  # MUST be lowercase!
            }

        CRITICAL:
            - MUST respond within 30 seconds
            - parity_choice MUST be lowercase "even" or "odd"
            - MUST include auth_token
            - Strategy engine has 25s timeout (5s buffer)

        Raises:
            Exception: If choice generation fails (after timeout/retry)

        See Also:
            Assignment Chapter 4: CHOOSE_PARITY_RESPONSE structure
            CLAUDE.md line 1920: Pitfall #2 - Parity Choice Capitalized
            config.yaml: timeouts.parity_choice_response = 30
        """
        start_time = time.time()
        conversation_id = params.get("conversation_id", "unknown")
        match_id = params.get("match_id", "unknown")
        opponent_id = params.get("opponent_id", "unknown")
        standings = params.get("standings", {})
        deadline = params.get("deadline")

        logger.info(f"Parity choice requested - match_id={match_id}, opponent_id={opponent_id}, deadline={deadline}")

        # Display parity choice context with rich formatting
        print_parity_thinking(
            match_id=match_id,
            opponent_id=opponent_id,
            standings=standings,
            strategy_mode=self.strategy.mode
        )

        try:
            # Build context for strategy engine
            context = {
                "opponent": opponent_id,
                "standings": standings,
                "history": self.state.get_match_history(limit=10),
                "deadline": deadline
            }

            # Get parity choice from strategy engine
            # Strategy engine handles timeout internally (25s with fallback)
            parity_choice = await self.strategy.choose_parity(context)

            # Validate choice is lowercase
            if parity_choice not in ["even", "odd"]:
                logger.error(f"Invalid parity choice from strategy - choice={parity_choice}, match_id={match_id}")
                # Emergency fallback to "even"
                parity_choice = "even"

            # Build CHOOSE_PARITY_RESPONSE
            response = self.protocol.build_choose_parity_response(
                conversation_id=conversation_id,
                match_id=match_id,
                parity_choice=parity_choice
            )

            # Calculate response time and display choice
            response_time = time.time() - start_time
            used_llm = self.strategy.mode in ["llm", "hybrid"]

            print_parity_choice(
                choice=parity_choice,
                response_time=response_time,
                used_llm=used_llm
            )

            logger.info(f"Parity choice made - match_id={match_id}, choice={parity_choice}, response_time={response_time:.2f}s")

            return response

        except asyncio.TimeoutError:
            logger.error(f"Parity choice timeout - using emergency fallback - match_id={match_id}, timeout=30s")
            # Emergency fallback
            response = self.protocol.build_choose_parity_response(
                conversation_id=conversation_id,
                match_id=match_id,
                parity_choice="even"  # Default fallback
            )
            return response

        except Exception as e:
            logger.error(f"Error choosing parity - match_id={match_id}, error={str(e)}")
            raise

    async def notify_match_result(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle GAME_OVER message from Referee.

        MCP Tool: notify_match_result
        Timeout: ≤10 seconds
        Message Type: RESULT_ACKNOWLEDGMENT

        This is called when the Referee notifies the player of the match result.
        The player must acknowledge within 10 seconds and update internal state.

        Args:
            params: GAME_OVER message parameters
                - conversation_id (str): Conversation ID
                - match_id (str): Match identifier
                - winner (str | None): Winner player ID (None for draw)
                - drawn_number (int): Number drawn by referee (1-10)
                - choices (dict): All player choices
                - opponent_id (str): Opponent player ID

        Returns:
            dict: RESULT_ACKNOWLEDGMENT message

        Example params:
            {
                "conversation_id": "conv-result-001",
                "match_id": "R1M1",
                "winner": "P01",  # or None for draw
                "drawn_number": 4,
                "choices": {
                    "P01": "even",
                    "P02": "odd"
                },
                "opponent_id": "P02"
            }

        Example response:
            {
                "protocol": "league.v2",
                "message_type": "RESULT_ACKNOWLEDGMENT",
                "sender": "player:P01",
                "timestamp": "2025-01-15T10:30:10.123456Z",
                "conversation_id": "conv-result-001",
                "auth_token": "token-12345",
                "match_id": "R1M1",
                "status": "acknowledged"
            }

        CRITICAL:
            - MUST respond within 10 seconds
            - MUST update internal state (stats, history)
            - MUST include auth_token

        See Also:
            Assignment Chapter 4: GAME_OVER structure
            config.yaml: timeouts.match_result_ack = 10
        """
        start_time = time.time()
        conversation_id = params.get("conversation_id", "unknown")
        match_id = params.get("match_id", "unknown")
        winner = params.get("winner")
        drawn_number = params.get("drawn_number", 0)
        choices = params.get("choices", {})
        opponent_id = params.get("opponent_id", "unknown")

        logger.info(f"Match result received - match_id={match_id}, winner={winner}, drawn_number={drawn_number}, choices={choices}")

        try:
            # Update player state with result
            self.state.update_from_result(params)

            # Build acknowledgment response
            response = self.protocol.build_result_acknowledgment(
                conversation_id=conversation_id,
                match_id=match_id,
                status="acknowledged"
            )

            # Get stats and determine points earned
            stats = self.state.get_stats()
            my_player_id = self.state.player_id
            my_choice = choices.get(my_player_id, "unknown")
            opponent_choice = choices.get(opponent_id, "unknown")

            # Calculate points earned
            if winner == my_player_id:
                points_earned = 3
            elif winner is None:
                points_earned = 1
            else:
                points_earned = 0

            # Display match result with rich formatting
            print_match_result(
                match_id=match_id,
                drawn_number=drawn_number,
                my_choice=my_choice,
                opponent_choice=opponent_choice,
                my_player_id=my_player_id,
                opponent_id=opponent_id,
                winner=winner,
                points_earned=points_earned
            )

            # Display updated stats
            print_stats_summary(
                wins=stats["wins"],
                losses=stats["losses"],
                draws=stats["draws"],
                total_points=stats["total_points"],
                matches_played=stats["total_matches"]
            )

            result_str = "win" if winner == my_player_id else ("draw" if winner is None else "loss")
            logger.info(f"Match result processed - match_id={match_id}, result={result_str}, stats={stats}")

            return response

        except Exception as e:
            logger.error(f"Error processing match result - match_id={match_id}, error={str(e)}")
            raise

    def update_auth_token(self, auth_token: str) -> None:
        """
        Update auth token after registration.

        This should be called after successful registration with League Manager.

        Args:
            auth_token: Authentication token from LEAGUE_REGISTER_RESPONSE
        """
        self.state.set_auth_token(auth_token)
        self.protocol.set_auth_token(auth_token)
        logger.info(f"Auth token updated - player_id={self.state.player_id}")
