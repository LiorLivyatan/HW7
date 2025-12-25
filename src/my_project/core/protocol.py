"""
Protocol Message Builder - Building Block: ProtocolMessageBuilder

Purpose:
    Constructs league.v2 protocol messages with exact JSON structure compliance.
    Ensures all messages include required fields and follow protocol specifications.

Input Data:
    - Message-specific parameters (conversation_id, match_id, player_id, etc.)
    - auth_token (required for all messages after registration)
    - Choice/result data depending on message type

Output Data:
    - Properly formatted league.v2 protocol messages as dictionaries
    - Ready for JSON serialization and HTTP transmission

Setup/Configuration:
    - player_id: Player identifier (from state or config)
    - auth_token: Authentication token (from registration response)

CRITICAL:
    - All timestamps MUST be UTC with 'Z' suffix
    - parity_choice MUST be lowercase: "even" or "odd"
    - auth_token MUST be included in all messages after registration
    - Message envelope must include: protocol, message_type, sender, timestamp, conversation_id

References:
    - CLAUDE.md: Lines 943-1089 (Assignment-Specific Requirements)
    - CLAUDE.md: Lines 1891-2013 (MCP Protocol Pitfalls)
    - Assignment Chapter 4: JSON Message Structures
    - Assignment Chapter 2: General League Protocol (message envelope)
"""

from typing import Optional, Dict, Any
from ..utils.timestamp import utc_now


class ProtocolMessageBuilder:
    """
    Builder class for constructing league.v2 protocol messages.

    This building block ensures:
    1. Exact JSON structure matching Chapter 4 specifications
    2. UTC timestamps with 'Z' suffix
    3. Lowercase parity choices
    4. Complete message envelope (protocol, message_type, sender, timestamp, conversation_id)
    5. Auth token inclusion in all messages

    Message Types Built:
    - LEAGUE_REGISTER_REQUEST
    - GAME_JOIN_ACK
    - CHOOSE_PARITY_RESPONSE

    Example:
        >>> builder = ProtocolMessageBuilder(player_id="P01")
        >>> builder.set_auth_token("auth-token-12345")
        >>> message = builder.build_game_join_ack(
        ...     conversation_id="conv-001",
        ...     match_id="R1M1",
        ...     accept=True
        ... )
    """

    PROTOCOL_VERSION = "league.v2"

    def __init__(self, player_id: str):
        """
        Initialize the protocol message builder.

        Args:
            player_id: Player identifier (e.g., "P01")

        Raises:
            ValueError: If player_id is None or empty
        """
        if not player_id:
            raise ValueError("player_id cannot be None or empty")

        self.player_id = player_id
        self.auth_token: Optional[str] = None

    def set_auth_token(self, auth_token: str) -> None:
        """
        Set the authentication token (received from registration).

        Args:
            auth_token: Authentication token from LEAGUE_REGISTER_RESPONSE

        IMPORTANT:
            Call this immediately after successful registration!
            All subsequent messages MUST include this token.
        """
        self.auth_token = auth_token

    def _build_envelope(
        self,
        message_type: str,
        conversation_id: str,
        include_auth: bool = True
    ) -> Dict[str, Any]:
        """
        Build the standard message envelope required by league.v2.

        Args:
            message_type: Type of message (e.g., "GAME_JOIN_ACK")
            conversation_id: Conversation ID (from incoming message)
            include_auth: Whether to include auth_token (default: True)

        Returns:
            dict: Message envelope with protocol, message_type, sender, timestamp, conversation_id

        Raises:
            ValueError: If auth_token is required but not set
        """
        envelope = {
            "protocol": self.PROTOCOL_VERSION,
            "message_type": message_type,
            "sender": f"player:{self.player_id}",
            "timestamp": utc_now(),  # CRITICAL: UTC with 'Z'
            "conversation_id": conversation_id,
        }

        # Add auth_token if required
        if include_auth:
            if not self.auth_token:
                raise ValueError(
                    f"auth_token is required for {message_type} but not set. "
                    "Call set_auth_token() after registration."
                )
            envelope["auth_token"] = self.auth_token

        return envelope

    def build_league_register_request(
        self,
        conversation_id: str,
        display_name: str,
        callback_url: str
    ) -> Dict[str, Any]:
        """
        Build LEAGUE_REGISTER_REQUEST message.

        This is sent to League Manager to register the player agent.

        Args:
            conversation_id: Unique conversation ID for this registration
            display_name: Human-readable player name
            callback_url: URL where player agent listens (e.g., "http://localhost:8101/mcp")

        Returns:
            dict: LEAGUE_REGISTER_REQUEST message

        Example:
            >>> builder = ProtocolMessageBuilder(player_id="P01")
            >>> msg = builder.build_league_register_request(
            ...     conversation_id="reg-001",
            ...     display_name="Gemini Agent",
            ...     callback_url="http://localhost:8101/mcp"
            ... )

        See Also:
            Assignment Chapter 4: LEAGUE_REGISTER_REQUEST structure
        """
        envelope = self._build_envelope(
            message_type="LEAGUE_REGISTER_REQUEST",
            conversation_id=conversation_id,
            include_auth=False  # No auth needed for registration
        )

        envelope.update({
            "player_id": self.player_id,
            "display_name": display_name,
            "callback_url": callback_url,
        })

        return envelope

    def build_game_join_ack(
        self,
        conversation_id: str,
        match_id: str,
        accept: bool = True
    ) -> Dict[str, Any]:
        """
        Build GAME_JOIN_ACK message.

        Response to GAME_INVITATION from Referee.
        MUST be sent within 5 seconds (see config.yaml timeouts).

        Args:
            conversation_id: From GAME_INVITATION message
            match_id: From GAME_INVITATION message
            accept: Whether to accept invitation (default: True)

        Returns:
            dict: GAME_JOIN_ACK message

        Example:
            >>> msg = builder.build_game_join_ack(
            ...     conversation_id="conv-game-001",
            ...     match_id="R1M1",
            ...     accept=True
            ... )

        CRITICAL:
            - Response time: ≤5 seconds
            - arrival_timestamp: UTC with 'Z'
            - auth_token: MUST be included

        See Also:
            Assignment Chapter 4: GAME_JOIN_ACK structure
            config.yaml: timeouts.game_invitation_response = 5
        """
        envelope = self._build_envelope(
            message_type="GAME_JOIN_ACK",
            conversation_id=conversation_id,
            include_auth=True
        )

        envelope.update({
            "match_id": match_id,
            "player_id": self.player_id,
            "arrival_timestamp": utc_now(),  # When player "arrives"
            "accept": accept,
        })

        return envelope

    def build_choose_parity_response(
        self,
        conversation_id: str,
        match_id: str,
        parity_choice: str
    ) -> Dict[str, Any]:
        """
        Build CHOOSE_PARITY_RESPONSE message.

        Response to CHOOSE_PARITY_CALL from Referee.
        MUST be sent within 30 seconds (see config.yaml timeouts).

        Args:
            conversation_id: From CHOOSE_PARITY_CALL message
            match_id: From CHOOSE_PARITY_CALL message
            parity_choice: Player's choice - MUST be lowercase "even" or "odd"

        Returns:
            dict: CHOOSE_PARITY_RESPONSE message

        Example:
            >>> msg = builder.build_choose_parity_response(
            ...     conversation_id="conv-choice-001",
            ...     match_id="R1M1",
            ...     parity_choice="even"  # MUST be lowercase!
            ... )

        CRITICAL:
            - Response time: ≤30 seconds
            - parity_choice: MUST be lowercase "even" or "odd"
            - auth_token: MUST be included
            - Will raise ValueError if parity_choice is not lowercase

        Raises:
            ValueError: If parity_choice is not "even" or "odd" (lowercase)

        See Also:
            Assignment Chapter 4: CHOOSE_PARITY_RESPONSE structure
            CLAUDE.md line 1920: Pitfall #2 - Parity Choice Capitalized
            config.yaml: timeouts.parity_choice_response = 30
        """
        # CRITICAL: Validate parity_choice is lowercase
        if parity_choice not in ["even", "odd"]:
            raise ValueError(
                f"parity_choice must be lowercase 'even' or 'odd', got: '{parity_choice}'. "
                f"This is a CRITICAL protocol requirement. See CLAUDE.md line 1920."
            )

        envelope = self._build_envelope(
            message_type="CHOOSE_PARITY_RESPONSE",
            conversation_id=conversation_id,
            include_auth=True
        )

        envelope.update({
            "match_id": match_id,
            "player_id": self.player_id,
            "parity_choice": parity_choice,  # MUST be lowercase
        })

        return envelope

    def build_result_acknowledgment(
        self,
        conversation_id: str,
        match_id: str,
        status: str = "acknowledged"
    ) -> Dict[str, Any]:
        """
        Build acknowledgment for GAME_OVER message.

        Response to notify_match_result call from Referee.
        MUST be sent within 10 seconds (see config.yaml timeouts).

        Args:
            conversation_id: From GAME_OVER message
            match_id: From GAME_OVER message
            status: Acknowledgment status (default: "acknowledged")

        Returns:
            dict: Result acknowledgment message

        Example:
            >>> msg = builder.build_result_acknowledgment(
            ...     conversation_id="conv-result-001",
            ...     match_id="R1M1",
            ...     status="acknowledged"
            ... )

        CRITICAL:
            - Response time: ≤10 seconds
            - auth_token: MUST be included

        See Also:
            config.yaml: timeouts.match_result_ack = 10
        """
        envelope = self._build_envelope(
            message_type="RESULT_ACKNOWLEDGMENT",
            conversation_id=conversation_id,
            include_auth=True
        )

        envelope.update({
            "match_id": match_id,
            "status": status,
        })

        return envelope


# Validation utilities
def validate_parity_choice(choice: str) -> bool:
    """
    Validate that parity choice is lowercase "even" or "odd".

    Args:
        choice: Parity choice to validate

    Returns:
        bool: True if valid, False otherwise

    Example:
        >>> validate_parity_choice("even")
        True
        >>> validate_parity_choice("Even")
        False
        >>> validate_parity_choice("EVEN")
        False
    """
    return choice in ["even", "odd"]


def normalize_parity_choice(choice: str) -> str:
    """
    Normalize parity choice to lowercase (with validation).

    Args:
        choice: Parity choice (any case)

    Returns:
        str: Lowercase parity choice

    Raises:
        ValueError: If choice is not "even" or "odd" (case-insensitive)

    Example:
        >>> normalize_parity_choice("Even")
        'even'
        >>> normalize_parity_choice("ODD")
        'odd'
        >>> normalize_parity_choice("invalid")
        ValueError: Invalid parity choice: invalid

    Warning:
        While this function can fix capitalization errors from LLM,
        it's better to prevent them using Pydantic output_schema.
        See agents/player/strategy.py for the correct approach.
    """
    choice_lower = choice.lower()
    if choice_lower not in ["even", "odd"]:
        raise ValueError(f"Invalid parity choice: {choice}")
    return choice_lower
