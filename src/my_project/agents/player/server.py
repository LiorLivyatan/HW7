"""
FastAPI MCP Server - Building Block: MCPProtocolHandler

Purpose:
    HTTP server implementing JSON-RPC 2.0 protocol for MCP tool handling.
    Routes incoming requests to appropriate tool handlers.

Input Data:
    - HTTP POST requests at /mcp endpoint
    - JSON-RPC 2.0 formatted messages

Output Data:
    - JSON-RPC 2.0 formatted responses
    - Tool execution results

Setup/Configuration:
    - PlayerState, StrategyEngine, ToolHandlers instances
    - Server configuration (host, port)

CRITICAL:
    - MUST follow JSON-RPC 2.0 specification exactly
    - MUST route to correct tool handler based on method
    - MUST handle errors gracefully with proper JSON-RPC error responses

References:
    - CLAUDE.md: Lines 1103-1289 (Phase 0: MCP Server Setup)
    - Assignment Chapter 2: General League Protocol (JSON-RPC 2.0)
    - Assignment Chapter 5: Implementation Guide (FastAPI examples)
"""

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import traceback

from .handlers import ToolHandlers
from ...utils.logger import setup_logger

logger = setup_logger(__name__)


class MCPRequest(BaseModel):
    """
    JSON-RPC 2.0 request model.

    Specification: https://www.jsonrpc.org/specification

    Example:
        {
            "jsonrpc": "2.0",
            "method": "choose_parity",
            "params": {...},
            "id": 1
        }
    """
    jsonrpc: str = Field(default="2.0", description="JSON-RPC version")
    method: str = Field(..., description="Method name to call")
    params: Dict[str, Any] = Field(default_factory=dict, description="Method parameters")
    id: int = Field(default=1, description="Request ID")


class MCPResponse(BaseModel):
    """
    JSON-RPC 2.0 response model.

    Success response:
        {
            "jsonrpc": "2.0",
            "result": {...},
            "id": 1
        }

    Error response:
        {
            "jsonrpc": "2.0",
            "error": {
                "code": -32601,
                "message": "Method not found"
            },
            "id": 1
        }
    """
    jsonrpc: str = Field(default="2.0", description="JSON-RPC version")
    result: Optional[Dict[str, Any]] = Field(default=None, description="Success result")
    error: Optional[Dict[str, Any]] = Field(default=None, description="Error object")
    id: int = Field(default=1, description="Request ID")


# JSON-RPC 2.0 Error Codes
class JSONRPCError:
    """Standard JSON-RPC 2.0 error codes."""
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603


def create_app(handlers: ToolHandlers) -> FastAPI:
    """
    Create FastAPI application with MCP endpoints.

    Args:
        handlers: ToolHandlers instance with all 3 tool implementations

    Returns:
        FastAPI: Configured FastAPI application

    Example:
        >>> from my_project.agents.player.state import PlayerState
        >>> from my_project.agents.player.strategy import StrategyEngine
        >>> from my_project.agents.player.handlers import ToolHandlers
        >>>
        >>> state = PlayerState(player_id="P01")
        >>> strategy = StrategyEngine(mode="hybrid")
        >>> handlers = ToolHandlers(state, strategy)
        >>> app = create_app(handlers)
        >>>
        >>> import uvicorn
        >>> uvicorn.run(app, host="localhost", port=8101)
    """
    app = FastAPI(
        title="Player Agent MCP Server",
        description="Even/Odd League Player Agent with Agno+Gemini",
        version="1.0.0",
        docs_url="/docs",  # Swagger UI at /docs
        redoc_url="/redoc"  # ReDoc at /redoc
    )

    @app.get("/")
    async def root():
        """Health check endpoint."""
        return {
            "status": "online",
            "service": "Player Agent MCP Server",
            "player_id": handlers.state.player_id,
            "display_name": handlers.state.display_name,
            "registered": handlers.state.registered,
            "strategy_mode": handlers.strategy.mode,
            "stats": handlers.state.get_stats()
        }

    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy"}

    @app.get("/stats")
    async def stats():
        """Get player statistics."""
        return {
            "player_id": handlers.state.player_id,
            "display_name": handlers.state.display_name,
            "stats": handlers.state.get_stats(),
            "win_rate": handlers.state.get_win_rate(),
            "total_matches": handlers.state.stats["total_matches"]
        }

    @app.post("/mcp")
    async def mcp_endpoint(request: MCPRequest) -> MCPResponse:
        """
        Main MCP endpoint for JSON-RPC 2.0 tool calls.

        This endpoint receives JSON-RPC 2.0 requests and routes them
        to the appropriate tool handler:
        - handle_game_invitation → handlers.handle_game_invitation()
        - choose_parity → handlers.choose_parity()
        - notify_match_result → handlers.notify_match_result()

        Args:
            request: MCPRequest with method and params

        Returns:
            MCPResponse: JSON-RPC 2.0 formatted response

        Example Request:
            POST /mcp
            {
                "jsonrpc": "2.0",
                "method": "choose_parity",
                "params": {
                    "conversation_id": "conv-001",
                    "match_id": "R1M1",
                    "opponent_id": "P02",
                    "deadline": "2025-01-15T10:30:30.000000Z"
                },
                "id": 1
            }

        Example Response:
            {
                "jsonrpc": "2.0",
                "result": {
                    "protocol": "league.v2",
                    "message_type": "CHOOSE_PARITY_RESPONSE",
                    "sender": "player:P01",
                    "timestamp": "2025-01-15T10:30:05.123456Z",
                    "conversation_id": "conv-001",
                    "auth_token": "token-12345",
                    "match_id": "R1M1",
                    "player_id": "P01",
                    "parity_choice": "even"
                },
                "id": 1
            }

        Error Response (Method not found):
            {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32601,
                    "message": "Method not found: invalid_method"
                },
                "id": 1
            }

        CRITICAL:
            - MUST return JSON-RPC 2.0 compliant responses
            - MUST handle all errors gracefully
            - MUST log all requests and responses
        """
        logger.info(f"MCP request received - method={request.method}, params_keys={list(request.params.keys())}, request_id={request.id}")

        try:
            # Route to appropriate handler
            if request.method == "handle_game_invitation":
                result = await handlers.handle_game_invitation(request.params)

            elif request.method == "choose_parity":
                result = await handlers.choose_parity(request.params)

            elif request.method == "notify_match_result":
                result = await handlers.notify_match_result(request.params)

            else:
                # Method not found error
                logger.warning(f"Unknown method called - method={request.method}")
                return MCPResponse(
                    error={
                        "code": JSONRPCError.METHOD_NOT_FOUND,
                        "message": f"Method not found: {request.method}"
                    },
                    id=request.id
                )

            # Success response
            logger.info(f"MCP request completed - method={request.method}, request_id={request.id}, result_type={result.get('message_type', 'unknown')}")

            return MCPResponse(result=result, id=request.id)

        except ValueError as e:
            # Invalid parameters
            logger.error(f"Invalid parameters - method={request.method}, error={str(e)}, request_id={request.id}")
            return MCPResponse(
                error={
                    "code": JSONRPCError.INVALID_PARAMS,
                    "message": f"Invalid parameters: {str(e)}"
                },
                id=request.id
            )

        except Exception as e:
            # Internal error
            logger.error(f"Internal error processing request - method={request.method}, error={str(e)}, request_id={request.id}, traceback={traceback.format_exc()}")
            return MCPResponse(
                error={
                    "code": JSONRPCError.INTERNAL_ERROR,
                    "message": f"Internal error: {str(e)}"
                },
                id=request.id
            )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler for unexpected errors."""
        logger.error(f"Unhandled exception - path={request.url.path}, method={request.method}, error={str(exc)}, traceback={traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "jsonrpc": "2.0",
                "error": {
                    "code": JSONRPCError.INTERNAL_ERROR,
                    "message": "Internal server error"
                },
                "id": None
            }
        )

    logger.info(f"FastAPI MCP Server created - player_id={handlers.state.player_id}, strategy_mode={handlers.strategy.mode}")

    return app
