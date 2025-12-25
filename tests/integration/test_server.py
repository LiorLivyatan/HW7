"""
Integration Tests for FastAPI MCP Server

Tests the complete HTTP server with JSON-RPC 2.0 endpoint.

Coverage Target: End-to-end server functionality
"""

import pytest
from fastapi.testclient import TestClient
from my_project.agents.player.state import PlayerState
from my_project.agents.player.strategy import StrategyEngine
from my_project.agents.player.handlers import ToolHandlers
from my_project.agents.player.server import create_app


@pytest.fixture
def test_app():
    """Create test FastAPI app with initialized components."""
    state = PlayerState(player_id="P01", display_name="Test Agent")
    state.set_auth_token("test-token-12345")

    strategy = StrategyEngine(mode="random")
    handlers = ToolHandlers(state, strategy)
    app = create_app(handlers)

    return app


@pytest.fixture
def client(test_app):
    """Create test client."""
    return TestClient(test_app)


class TestServerEndpoints:
    """Test server HTTP endpoints."""

    def test_root_endpoint(self, client):
        """Test GET / returns server info."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "online"
        assert data["player_id"] == "P01"
        assert data["display_name"] == "Test Agent"
        assert "stats" in data

    def test_health_endpoint(self, client):
        """Test GET /health returns healthy status."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"

    def test_stats_endpoint(self, client):
        """Test GET /stats returns player statistics."""
        response = client.get("/stats")

        assert response.status_code == 200
        data = response.json()

        assert data["player_id"] == "P01"
        assert "stats" in data
        assert "win_rate" in data
        assert data["total_matches"] == 0  # No matches yet


class TestMCPEndpoint:
    """Test JSON-RPC 2.0 MCP endpoint."""

    def test_handle_game_invitation(self, client):
        """Test handle_game_invitation tool via MCP endpoint."""
        request = {
            "jsonrpc": "2.0",
            "method": "handle_game_invitation",
            "params": {
                "conversation_id": "conv-test-001",
                "match_id": "R1M1",
                "opponent_id": "P02",
                "game_type": "even_odd",
                "deadline": "2025-01-15T10:30:05.000000Z"
            },
            "id": 1
        }

        response = client.post("/mcp", json=request)

        assert response.status_code == 200
        data = response.json()

        # Check JSON-RPC 2.0 format
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 1
        assert "result" in data

        # Check result message
        result = data["result"]
        assert result["protocol"] == "league.v2"
        assert result["message_type"] == "GAME_JOIN_ACK"
        assert result["match_id"] == "R1M1"
        assert result["accept"] is True
        assert result["timestamp"].endswith('Z')

    def test_choose_parity(self, client):
        """Test choose_parity tool via MCP endpoint."""
        request = {
            "jsonrpc": "2.0",
            "method": "choose_parity",
            "params": {
                "conversation_id": "conv-test-002",
                "match_id": "R1M1",
                "opponent_id": "P02",
                "deadline": "2025-01-15T10:30:30.000000Z"
            },
            "id": 2
        }

        response = client.post("/mcp", json=request)

        assert response.status_code == 200
        data = response.json()

        # Check JSON-RPC 2.0 format
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 2
        assert "result" in data

        # Check result message
        result = data["result"]
        assert result["protocol"] == "league.v2"
        assert result["message_type"] == "CHOOSE_PARITY_RESPONSE"
        assert result["match_id"] == "R1M1"
        assert result["parity_choice"] in ["even", "odd"]
        assert result["parity_choice"] == result["parity_choice"].lower()  # MUST be lowercase

    def test_notify_match_result(self, client):
        """Test notify_match_result tool via MCP endpoint."""
        request = {
            "jsonrpc": "2.0",
            "method": "notify_match_result",
            "params": {
                "conversation_id": "conv-test-003",
                "match_id": "R1M1",
                "winner": "P01",
                "drawn_number": 4,
                "choices": {
                    "P01": "even",
                    "P02": "odd"
                },
                "opponent_id": "P02"
            },
            "id": 3
        }

        response = client.post("/mcp", json=request)

        assert response.status_code == 200
        data = response.json()

        # Check JSON-RPC 2.0 format
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 3
        assert "result" in data

        # Check result
        result = data["result"]
        assert result["status"] == "acknowledged"

    def test_method_not_found(self, client):
        """Test error response for unknown method."""
        request = {
            "jsonrpc": "2.0",
            "method": "invalid_method",
            "params": {},
            "id": 999
        }

        response = client.post("/mcp", json=request)

        assert response.status_code == 200
        data = response.json()

        # Check JSON-RPC 2.0 error format
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 999
        assert "error" in data
        assert data["error"]["code"] == -32601  # Method not found
        assert "Method not found" in data["error"]["message"]


class TestProtocolCompliance:
    """Test protocol compliance in server responses."""

    def test_all_responses_have_correct_timestamps(self, client):
        """Test that all responses include UTC timestamps with 'Z'."""
        methods = [
            ("handle_game_invitation", {"conversation_id": "c1", "match_id": "M1"}),
            ("choose_parity", {"conversation_id": "c2", "match_id": "M2"}),
        ]

        for method, params in methods:
            request = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": 1
            }

            response = client.post("/mcp", json=request)
            data = response.json()

            result = data.get("result", {})
            if "timestamp" in result:
                assert result["timestamp"].endswith('Z'), f"Timestamp missing 'Z' in {method}"

    def test_parity_choice_always_lowercase(self, client):
        """Test that parity choice is ALWAYS lowercase."""
        request = {
            "jsonrpc": "2.0",
            "method": "choose_parity",
            "params": {
                "conversation_id": "conv-test",
                "match_id": "R1M1"
            },
            "id": 1
        }

        # Test multiple times
        for _ in range(10):
            response = client.post("/mcp", json=request)
            data = response.json()

            result = data["result"]
            parity = result["parity_choice"]

            assert parity in ["even", "odd"]
            assert parity == parity.lower(), f"Parity not lowercase: {parity}"


class TestStateUpdates:
    """Test that server updates state correctly."""

    def test_match_result_updates_stats(self, client):
        """Test that notify_match_result updates player statistics."""
        # Check initial stats
        stats_before = client.get("/stats").json()
        assert stats_before["stats"]["wins"] == 0

        # Send match result (win)
        request = {
            "jsonrpc": "2.0",
            "method": "notify_match_result",
            "params": {
                "conversation_id": "conv-test",
                "match_id": "R1M1",
                "winner": "P01",  # We won!
                "drawn_number": 4,
                "choices": {"P01": "even", "P02": "odd"},
                "opponent_id": "P02"
            },
            "id": 1
        }

        client.post("/mcp", json=request)

        # Check updated stats
        stats_after = client.get("/stats").json()
        assert stats_after["stats"]["wins"] == 1
        assert stats_after["stats"]["total_points"] == 3
        assert stats_after["total_matches"] == 1
