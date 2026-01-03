"""
Registration Client - Building Block: RegistrationClient

Purpose:
    Handles registration with the League Manager.
    Sends LEAGUE_REGISTER_REQUEST and receives auth_token.

Input Data:
    - player_id (str): Player identifier
    - display_name (str): Player display name
    - callback_url (str): Player agent's MCP endpoint URL

Output Data:
    - auth_token (str): Authentication token from League Manager
    - registration_status (bool): Whether registration succeeded

Setup/Configuration:
    - league_manager_host (str): League Manager hostname
    - league_manager_port (int): League Manager port

References:
    - Assignment Chapter 4: LEAGUE_REGISTER_REQUEST/RESPONSE
    - Assignment Chapter 8: Game Flow (registration step)
"""

import httpx
from typing import Dict, Any, Optional
import uuid

from ..core.protocol import ProtocolMessageBuilder
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class RegistrationClient:
    """
    Client for registering with the League Manager.

    This building block handles:
    1. Constructing LEAGUE_REGISTER_REQUEST
    2. Sending HTTP request to League Manager
    3. Processing LEAGUE_REGISTER_RESPONSE
    4. Extracting and returning auth_token

    Example:
        >>> client = RegistrationClient(
        ...     league_manager_url="http://localhost:8000/mcp"
        ... )
        >>> auth_token = await client.register(
        ...     player_id="P01",
        ...     display_name="Gemini Agent",
        ...     callback_url="http://localhost:8101/mcp"
        ... )
    """

    def __init__(
        self,
        league_manager_url: str = "http://localhost:8000/mcp",
        timeout: int = 10
    ):
        """
        Initialize registration client.

        Args:
            league_manager_url: Full URL to League Manager's MCP endpoint
            timeout: Request timeout in seconds
        """
        self.league_manager_url = league_manager_url
        self.timeout = timeout

    async def register(
        self,
        player_id: str,
        display_name: str,
        callback_url: str
    ) -> str:
        """
        Register player with League Manager.

        Args:
            player_id: Player identifier (e.g., "P01")
            display_name: Human-readable player name
            callback_url: Player agent's MCP endpoint URL

        Returns:
            str: auth_token received from League Manager

        Raises:
            httpx.HTTPError: If registration request fails
            ValueError: If response doesn't contain auth_token

        Example:
            >>> token = await client.register(
            ...     player_id="P01",
            ...     display_name="Gemini Agent",
            ...     callback_url="http://localhost:8101/mcp"
            ... )
            >>> print(f"Registered! Token: {token}")
        """
        logger.info(
            f"Registering with League Manager - player_id={player_id}, "
            f"display_name={display_name}, callback_url={callback_url}, "
            f"league_manager_url={self.league_manager_url}"
        )

        # Build registration message
        protocol = ProtocolMessageBuilder(player_id=player_id)
        conversation_id = f"registration-{uuid.uuid4().hex[:8]}"

        message = protocol.build_league_register_request(
            conversation_id=conversation_id,
            display_name=display_name,
            callback_url=callback_url
        )

        # Send JSON-RPC 2.0 request
        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "league_register",
            "params": message,
            "id": 1
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.league_manager_url,
                    json=json_rpc_request
                )
                response.raise_for_status()
                data = response.json()

            # Extract auth_token from response
            if "result" in data:
                auth_token = data["result"].get("auth_token")
                if auth_token:
                    logger.info(
                        f"Registration successful - player_id={player_id}, "
                        f"token_preview={auth_token[:8]}..."
                    )
                    return auth_token
                else:
                    raise ValueError("No auth_token in registration response")
            elif "error" in data:
                error_msg = data["error"].get("message", "Unknown error")
                raise ValueError(f"Registration failed: {error_msg}")
            else:
                raise ValueError("Invalid response format")

        except httpx.HTTPError as e:
            logger.error(
                f"Registration request failed - player_id={player_id}, error={str(e)}"
            )
            raise

        except Exception as e:
            logger.error(
                f"Registration error - player_id={player_id}, error={str(e)}"
            )
            raise
