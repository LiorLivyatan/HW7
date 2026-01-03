"""
Tests for RegistrationClient - Building Block: RegistrationClient

Coverage:
- Initialization
- Successful registration
- Error handling (HTTP errors, invalid responses)
- Edge cases
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from my_project.core.registration import RegistrationClient


class TestRegistrationClient:
    """Test RegistrationClient initialization and basic functionality."""

    def test_initialization_default_values(self):
        """Test initialization with default values."""
        client = RegistrationClient()
        assert client.league_manager_url == "http://localhost:8000/mcp"
        assert client.timeout == 10

    def test_initialization_custom_values(self):
        """Test initialization with custom values."""
        client = RegistrationClient(
            league_manager_url="http://example.com:9000/mcp",
            timeout=30
        )
        assert client.league_manager_url == "http://example.com:9000/mcp"
        assert client.timeout == 30


class TestRegistrationSuccess:
    """Test successful registration scenarios."""

    @pytest.mark.asyncio
    async def test_register_success(self):
        """Test successful registration flow."""
        client = RegistrationClient()

        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "result": {
                "protocol": "league.v2",
                "message_type": "LEAGUE_REGISTER_RESPONSE",
                "auth_token": "test_token_123456",
                "status": "registered"
            },
            "id": 1
        }
        mock_response.raise_for_status = MagicMock()

        # Mock httpx.AsyncClient
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_client

            # Perform registration
            auth_token = await client.register(
                player_id="P01",
                display_name="Test Agent",
                callback_url="http://localhost:8101/mcp"
            )

            assert auth_token == "test_token_123456"

    @pytest.mark.asyncio
    async def test_register_with_different_player_ids(self):
        """Test registration with various player IDs."""
        client = RegistrationClient()

        player_ids = ["P01", "P02", "P99", "PLAYER_001"]

        for player_id in player_ids:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "jsonrpc": "2.0",
                "result": {"auth_token": f"token_{player_id}"},
                "id": 1
            }
            mock_response.raise_for_status = MagicMock()

            with patch("httpx.AsyncClient") as mock_client_class:
                mock_client = AsyncMock()
                mock_client.__aenter__.return_value = mock_client
                mock_client.__aexit__.return_value = None
                mock_client.post = AsyncMock(return_value=mock_response)
                mock_client_class.return_value = mock_client

                auth_token = await client.register(
                    player_id=player_id,
                    display_name="Test Agent",
                    callback_url="http://localhost:8101/mcp"
                )

                assert auth_token == f"token_{player_id}"


class TestRegistrationErrors:
    """Test error handling in registration."""

    @pytest.mark.asyncio
    async def test_register_http_error(self):
        """Test registration with HTTP error."""
        client = RegistrationClient()

        # Mock HTTP error
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client.post = AsyncMock(
                side_effect=httpx.HTTPError("Connection failed")
            )
            mock_client_class.return_value = mock_client

            with pytest.raises(httpx.HTTPError):
                await client.register(
                    player_id="P01",
                    display_name="Test Agent",
                    callback_url="http://localhost:8101/mcp"
                )

    @pytest.mark.asyncio
    async def test_register_no_auth_token_in_response(self):
        """Test registration when auth_token is missing."""
        client = RegistrationClient()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "result": {
                "protocol": "league.v2",
                "message_type": "LEAGUE_REGISTER_RESPONSE",
                "status": "registered"
                # Missing auth_token!
            },
            "id": 1
        }
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_client

            with pytest.raises(ValueError, match="No auth_token in registration response"):
                await client.register(
                    player_id="P01",
                    display_name="Test Agent",
                    callback_url="http://localhost:8101/mcp"
                )

    @pytest.mark.asyncio
    async def test_register_error_response(self):
        """Test registration with error in response."""
        client = RegistrationClient()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "error": {
                "code": -32600,
                "message": "Player already registered"
            },
            "id": 1
        }
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_client

            with pytest.raises(ValueError, match="Registration failed: Player already registered"):
                await client.register(
                    player_id="P01",
                    display_name="Test Agent",
                    callback_url="http://localhost:8101/mcp"
                )

    @pytest.mark.asyncio
    async def test_register_invalid_response_format(self):
        """Test registration with invalid response format."""
        client = RegistrationClient()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            # Missing both 'result' and 'error'
            "id": 1
        }
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_client

            with pytest.raises(ValueError, match="Invalid response format"):
                await client.register(
                    player_id="P01",
                    display_name="Test Agent",
                    callback_url="http://localhost:8101/mcp"
                )

    @pytest.mark.asyncio
    async def test_register_timeout(self):
        """Test registration with timeout."""
        client = RegistrationClient(timeout=1)

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client.post = AsyncMock(
                side_effect=httpx.TimeoutException("Request timed out")
            )
            mock_client_class.return_value = mock_client

            with pytest.raises(httpx.TimeoutException):
                await client.register(
                    player_id="P01",
                    display_name="Test Agent",
                    callback_url="http://localhost:8101/mcp"
                )


class TestEdgeCases:
    """Test edge cases for RegistrationClient."""

    @pytest.mark.asyncio
    async def test_empty_display_name(self):
        """Test registration with empty display name."""
        client = RegistrationClient()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "result": {"auth_token": "test_token"},
            "id": 1
        }
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_client

            # Should succeed even with empty display name
            auth_token = await client.register(
                player_id="P01",
                display_name="",
                callback_url="http://localhost:8101/mcp"
            )

            assert auth_token == "test_token"

    @pytest.mark.asyncio
    async def test_very_long_display_name(self):
        """Test registration with very long display name."""
        client = RegistrationClient()

        long_name = "A" * 1000

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "result": {"auth_token": "test_token"},
            "id": 1
        }
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_client

            auth_token = await client.register(
                player_id="P01",
                display_name=long_name,
                callback_url="http://localhost:8101/mcp"
            )

            assert auth_token == "test_token"

    @pytest.mark.asyncio
    async def test_special_characters_in_display_name(self):
        """Test registration with special characters in display name."""
        client = RegistrationClient()

        special_names = [
            "Agent 🤖",
            "Player-01",
            "Test_Agent_123",
            "Агент",  # Cyrillic
            "代理",    # Chinese
        ]

        for name in special_names:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "jsonrpc": "2.0",
                "result": {"auth_token": f"token_{name}"},
                "id": 1
            }
            mock_response.raise_for_status = MagicMock()

            with patch("httpx.AsyncClient") as mock_client_class:
                mock_client = AsyncMock()
                mock_client.__aenter__.return_value = mock_client
                mock_client.__aexit__.return_value = None
                mock_client.post = AsyncMock(return_value=mock_response)
                mock_client_class.return_value = mock_client

                auth_token = await client.register(
                    player_id="P01",
                    display_name=name,
                    callback_url="http://localhost:8101/mcp"
                )

                assert auth_token == f"token_{name}"
