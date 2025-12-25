# 5 Implementation Guide
This chapter presents how to implement the agents. The examples are in Python with FastAPI. It is possible to use any language that supports HTTP.

## 5.1 General Architecture

### 5.1.1 Component Diagram
*(Diagram reference: Orchestrator/Host sends/receives HTTP to/from League Manager (:8000), Referee (:8001), Players (:8101-8104))*

### 5.1.2 Role of the Orchestrator
The Orchestrator coordinates between all agents. It:
- Sends HTTP requests to every server.
- Receives responses and processes them.
- Manages the flow of the league.

## 5.2 Simple MCP Server Implementation

### 5.2.1 Basic Structure in FastAPI

**Basic MCP Server**
```python
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: dict = {}
    id: int = 1

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: dict = {}
    id: int = 1

@app.post("/mcp")
async def mcp_endpoint(request: MCPRequest):
    if request.method == "tool_name":
        result = handle_tool(request.params)
        return MCPResponse(result=result, id=request.id)
    return MCPResponse(result={"error": "Unknown method"})

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8101)
```

## 5.3 Player Agent Implementation

### 5.3.1 Required Tools
A player agent must implement the following tools:
1. `handle_game_invitation` – Receiving invitation to a match.
2. `choose_parity` – Choosing "even" or "odd".
3. `notify_match_result` – Receiving match result.

### 5.3.2 Example Player Implementation

**Simple Player Agent**
```python
import random
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: dict = {}
    id: int = 1

@app.post("/mcp")
async def mcp_endpoint(request: MCPRequest):
    if request.method == "handle_game_invitation":
        return handle_invitation(request.params)
    elif request.method == "choose_parity":
        return handle_choose_parity(request.params)
    elif request.method == "notify_match_result":
        return handle_result(request.params)
    return {"error": "Unknown method"}

def handle_invitation(params):
    # Accept the invitation
    return {
        "message_type": "GAME_JOIN_ACK",
        "match_id": params.get("match_id"),
        "arrival_timestamp": datetime.now().isoformat(),
        "accept": True
    }

def handle_choose_parity(params):
    # Random strategy
    choice = random.choice(["even", "odd"])
    return {
        "message_type": "CHOOSE_PARITY_RESPONSE",
        "match_id": params.get("match_id"),
        "player_id": params.get("player_id"),
        "parity_choice": choice
    }

def handle_result(params):
    # Log result for learning
    print(f"Match result: {params}")
    return {"status": "ok"}
```

## 5.4 Referee Implementation

### 5.4.1 Required Tools
The referee must implement:
1. `register_to_league` – Self registration to League Manager.
2. `start_match` – Starting a new match.
3. `collect_choices` – Collecting choices from players.
4. `draw_number` – Number draw.
5. `finalize_match` – Ending the match and reporting.

### 5.4.2 Referee Registration to League

**Referee Registration to League Manager**
```python
import requests

def register_to_league(league_endpoint, referee_info):
    payload = {
        "jsonrpc": "2.0",
        "method": "register_referee",
        "params": {
            "referee_meta": {
                "display_name": referee_info["name"],
                "version": "1.0.0",
                "game_types": ["even_odd"],
                "contact_endpoint": referee_info["endpoint"],
                "max_concurrent_matches": 2
            }
        },
        "id": 1
    }
    response = requests.post(league_endpoint, json=payload)
    result = response.json()
    return result.get("result", {}).get("referee_id")
```

### 5.4.3 Winner Determination Logic – Even/Odd

**Determining Winner in Even/Odd Game**
```python
def determine_winner(choice_a, choice_b, number):
    is_even = (number % 2 == 0)
    parity = "even" if is_even else "odd"

    a_correct = (choice_a == parity)
    b_correct = (choice_b == parity)

    if a_correct and not b_correct:
        return "PLAYER_A"
    elif b_correct and not a_correct:
        return "PLAYER_B"
    else:
        return "DRAW"
```

## 5.5 League Manager Implementation

### 5.5.1 Required Tools
The League Manager must implement:
1. `register_referee` – New referee registration.
2. `register_player` – New player registration.
3. `create_schedule` – Creating match board.
4. `report_match_result` – Receiving result report.
5. `get_standings` – Returning standings table.

### 5.5.2 Referee Registration in League Manager

**Referee Registration in League Manager**
```python
class LeagueManager:
    def __init__(self):
        self.referees = {}  # referee_id -> referee_info
        self.players = {}   # player_id -> player_info
        self.next_referee_id = 1

    def register_referee(self, params):
        referee_meta = params.get("referee_meta", {})
        referee_id = f"REF{self.next_referee_id:02d}"
        self.next_referee_id += 1

        self.referees[referee_id] = {
            "referee_id": referee_id,
            "display_name": referee_meta.get("display_name"),
            "endpoint": referee_meta.get("contact_endpoint"),
            "game_types": referee_meta.get("game_types", []),
            "max_concurrent": referee_meta.get("max_concurrent_matches", 1)
        }

        return {
            "message_type": "REFEREE_REGISTER_RESPONSE",
            "status": "ACCEPTED",
            "referee_id": referee_id,
            "reason": None
        }
```

### 5.5.3 Creating Game Board

**Round-Robin Algorithm**
```python
from itertools import combinations

def create_schedule(players):
    matches = []
    round_num = 1
    match_num = 1

    for p1, p2 in combinations(players, 2):
        matches.append({
            "match_id": f"R{round_num}M{match_num}",
            "player_A_id": p1,
            "player_B_id": p2
        })
        match_num += 1

    return matches
```

## 5.6 Sending HTTP Requests

### 5.6.1 MCP Tool Call

**Sending Request to MCP Server**
```python
import requests

def call_mcp_tool(endpoint, method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": "method", # Note: 'method' here is likely a variable, corrected in example usage
        "params": params,
        "id": 1
    }
    response = requests.post(endpoint, json=payload)
    return response.json()

# Example: Call player's choose_parity
result = call_mcp_tool(
    "http://localhost:8101/mcp",
    "choose_parity",
    {"match_id": "R1M1", "player_id": "P01"}
)
```

## 5.7 State Management

### 5.7.1 Player State
The player can keep internal information:
- History of games.
- Personal statistics.
- Information on opponents.

**Player State Class**
```python
class PlayerState:
    def __init__(self, player_id):
        self.player_id = player_id
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.history = []

    def update(self, result):
        self.history.append(result)
        if result["winner"] == self.player_id:
            self.wins += 1
        elif result["winner"] == "DRAW":
            self.draws += 1
        else:
            self.losses += 1
```

## 5.8 Error Handling

### 5.8.1 Response Time
**Request with timeout**
```python
import requests

def call_with_timeout(endpoint, method, params, timeout=30):
    try:
        response = requests.post(
            endpoint,
            json={"jsonrpc": "2.0", "method": method, "params": params, "id": 1},
            timeout=timeout
        )
        return response.json()
    except requests.Timeout:
        return {"error": "TIMEOUT"}
    except requests.RequestException as e:
        return {"error": str(e)}
```

### 5.8.2 Response to Errors
If a player does not answer:
1. The referee waits until timeout.
2. If there is no response – Technical loss.
3. The referee reports to the League Manager.

## 5.9 Resilience Patterns
The system must cope with failures and delays. The protocol defines retry policy.

### 5.9.1 Implementation of Retry with Backoff

**Retry Logic with Backoff**
```python
import time
import requests
from typing import Optional, Dict, Any

class RetryConfig:
    MAX_RETRIES = 3
    BASE_DELAY = 2.0  # seconds
    BACKOFF_MULTIPLIER = 2.0

def call_with_retry(endpoint: str, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Send MCP request with retry logic."""
    last_error = None

    for attempt in range(RetryConfig.MAX_RETRIES):
        try:
            response = requests.post(
                endpoint,
                json={
                    "jsonrpc": "2.0",
                    "method": method,
                    "params": params,
                    "id": 1
                },
                timeout=30
            )
            return response.json()

        except (requests.Timeout, requests.ConnectionError) as e:
            last_error = e
            if attempt < RetryConfig.MAX_RETRIES - 1:
                delay = RetryConfig.BASE_DELAY * \
                        (RetryConfig.BACKOFF_MULTIPLIER ** attempt)
                time.sleep(delay)

    return {
        "error": {
            "error_code": "E005",
            "error_description": f"Max retries exceeded: {last_error}"
        }
    }
```

### 5.9.2 Circuit Breaker Pattern
When a server fails several times, we avoid additional attempts for a certain period.

**Simple Circuit Breaker**
```python
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failures = 0
        self.threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.last_failure = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def can_execute(self) -> bool:
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            if datetime.now() - self.last_failure > \
               timedelta(seconds=self.reset_timeout):
                self.state = "HALF_OPEN"
                return True
            return False
        return True  # HALF_OPEN allows one try

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failures += 1
        self.last_failure = datetime.now()
        if self.failures >= self.threshold:
            self.state = "OPEN"
```

## 5.10 Structured Logging
The protocol requires documentation in JSON format for analysis and debugging. Every log message must include the following fields:

**Table 12: Mandatory Fields in Log Message**

| Field | Mandatory | Type | Description |
| :--- | :--- | :--- | :--- |
| timestamp | Yes | ISO-8601 | Event time |
| level | Yes | string | DEBUG/INFO/WARN/ERROR |
| agent_id | Yes | string | Agent identifier |
| message_type | No | string | Message type |
| conversation_id | No | string | Conversation identifier |
| message | Yes | string | Event description |
| data | No | object | Additional data |

### 5.10.1 Structured Logger Implementation

**Structured Logger**
```python
import json
import sys
from datetime import datetime
from typing import Optional, Dict, Any

class StructuredLogger:
    LEVELS = ["DEBUG", "INFO", "WARN", "ERROR"]

    def __init__(self, agent_id: str, min_level: str = "INFO"):
        self.agent_id = agent_id
        self.min_level = self.LEVELS.index(min_level)

    def log(self, level: str, message: str,
            message_type: Optional[str] = None,
            conversation_id: Optional[str] = None,
            data: Optional[Dict[str, Any]] = None):

        if self.LEVELS.index(level) < self.min_level:
            return

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "agent_id": self.agent_id,
            "message": message
        }

        if message_type:
            log_entry["message_type"] = message_type
        if conversation_id:
            log_entry["conversation_id"] = conversation_id
        if data:
            log_entry["data"] = data

        print(json.dumps(log_entry), file=sys.stderr)

    def info(self, message, **kwargs):
        self.log("INFO", message, **kwargs)

    def error(self, message, **kwargs):
        self.log("ERROR", message, **kwargs)
```

### 5.10.2 Example Usage

**Usage in Logger**
```python
logger = StructuredLogger("player:P01")

# Log received message
logger.info(
    "Received game invitation",
    message_type="GAME_INVITATION",
    conversation_id="conv-12345",
    data={"match_id": "R1M1", "opponent": "P02"}
)

# Log error
logger.error(
    "Failed to connect to referee",
    data={"endpoint": "http://localhost:8001", "error": "timeout"}
)
```

**Log Output:**
```json
{
  "timestamp": "2025-01-15T10:30:00.123Z",
  "level": "INFO",
  "agent_id": "player:P01",
  "message": "Received game invitation",
  "message_type": "GAME_INVITATION",
  "conversation_id": "conv-12345",
  "data": {"match_id": "R1M1", "opponent": "P02"}
}
```

## 5.11 Authentication and Tokens (Authentication)
Starting from version 2.1.0 of the protocol, every message must include an `auth_token` for authentication. The token is received at the time of registration and serves to identify the agent in every request.

### 5.11.1 Token Registration and Receiving

**Registration and Receiving Token**
```python
import requests
from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentCredentials:
    agent_id: str
    auth_token: str
    league_id: str

def register_player(league_endpoint: str,
                   player_info: dict) -> Optional[AgentCredentials]:
    """Register player and store auth token."""
    payload = {
        "jsonrpc": "2.0",
        "method": "register_player",
        "params": {
            "protocol": "league.v2",
            "message_type": "LEAGUE_REGISTER_REQUEST",
            "sender": f"player:{player_info['name']}",
            "player_meta": player_info
        },
        "id": 1
    }

    response = requests.post(league_endpoint, json=payload)
    result = response.json().get("result", {})

    if result.get("status") == "ACCEPTED":
        return AgentCredentials(
            agent_id=result["player_id"],
            auth_token=result["auth_token"],
            league_id=result["league_id"]
        )
    return None
```

### 5.11.2 Usage of Token in Requests

**Request with Authentication Token**
```python
class AuthenticatedClient:
    def __init__(self, credentials: AgentCredentials):
        self.creds = credentials

    def send_message(self, endpoint: str, message_type: str,
                    params: dict) -> dict:
        """Send authenticated message."""
        payload = {
            "jsonrpc": "2.0",
            "method": "mcp_message",
            "params": {
                "protocol": "league.v2",
                "message_type": message_type,
                "sender": f"player:{self.creds.agent_id}",
                "auth_token": self.creds.auth_token,
                "league_id": self.creds.league_id,
                **params
            },
            "id": 1
        }

        response = requests.post(endpoint, json=payload)
        return response.json()
```

### 5.11.3 Handling Authentication Errors

**Handling Authentication Errors**
```python
def handle_auth_error(response: dict) -> bool:
    """Check for authentication errors."""
    error = response.get("error", {})
    error_code = error.get("error_code", "")

    if error_code == "E011":  # AUTH_TOKEN_MISSING
        print("Error: auth token required")
        return False
    elif error_code == "E012":  # AUTH_TOKEN_INVALID
        print("Error: auth token is invalid or expired")
        # May need to re-register
        return False
    elif error_code == "E013":  # REFEREE_NOT_REGISTERED
        print("Error: Referee must register first")
        return False

    return True  # No auth error
```

## 5.12 Local Testing

### 5.12.1 Local Run
Run every agent in a separate terminal:

**Running the Agents**
```bash
# Terminal 1: League Manager (start first)
python league_manager.py  # Port 8000

# Terminal 2: Referee
python referee.py  # Port 8001

# Terminal 3-6: Players
python player.py --port 8101
python player.py --port 8102
python player.py --port 8103
python player.py --port 8104
```

**Important Order:**
1. First the League Manager must run.
2. The referee registers to the League Manager at startup.
3. The players register to the League Manager.
4. Only then it is possible to start the league.

### 5.12.2 Server Check

**Server Check**
```python
import requests

def test_server(port):
    try:
        r = requests.post(
            f"http://localhost:{port}/mcp",
            json={"jsonrpc": "2.0", "method": "ping", "id": 1}
        )
        print(f"Port {port}: OK")
    except:
        print(f"Port {port}: FAILED")

# Test all servers
for port in [8000, 8001, 8101, 8102, 8103, 8104]:
    test_server(port)
```

## 5.13 Implementation Tips
1. **Start Simple** – Implement a random strategy first.
2. **Local Check** – Run a league with yourself.
3. **Save Logs** – Document every message.
4. **Handle Errors** – Use try/except.
5. **Follow the Protocol** – Use the JSON structure exactly.

```