# 8 Running the League System
This appendix presents a practical guide to running the complete league system. We will demonstrate how to operate all the agents: one League Manager, two referees, and four players. The examples are based on the protocol `league.v2` described in previous chapters.

## 8.1 System Configuration

### 8.1.1 Ports and Terminals
Every agent in the system operates as a separate HTTP server on a dedicated port on localhost. In this example we will run 7 terminals:

**Table 15: Allocation of Ports and Terminals**

| Terminal | Agent | Port | Endpoint |
| :--- | :--- | :--- | :--- |
| 1 | League Manager | 8000 | `http://localhost:8000/mcp` |
| 2 | Referee REF01 | 8001 | `http://localhost:8001/mcp` |
| 3 | Referee REF02 | 8002 | `http://localhost:8002/mcp` |
| 4 | Player P01 | 8101 | `http://localhost:8101/mcp` |
| 5 | Player P02 | 8102 | `http://localhost:8102/mcp` |
| 6 | Player P03 | 8103 | `http://localhost:8103/mcp` |
| 7 | Player P04 | 8104 | `http://localhost:8104/mcp` |

### 8.1.2 Roles of the Orchestrators
In the system there are two types of Orchestrators:
- **League Manager** – Upper orchestrator of the league. It is the source of truth for the standings table, the match board, and the state of the rounds.
- **Referees** – Local orchestrators for a single match. Every referee is the source of truth for the state of the match they manage.

## 8.2 Order of Operation

### 8.2.1 Principle of Order of Operation
The order of operation is critical for the proper functioning of the system:
1. **League Manager** – Must come up first.
2. **Referees** – Come up and register to the League Manager.
3. **Players** – Come up and register to the League Manager.
4. **Start of League** – Only after the completion of all registrations.

### 8.2.2 Terminal 1 – League Manager

**Running the League Manager**
```bash
# Terminal 1 - League Manager
python league_manager.py  # Listening on :8000
```

The League Manager listens for POST requests at address `http://localhost:8000/mcp`.

### 8.2.3 Terminals 2-3 – Referees

**Running Referees**
```bash
# Terminal 2 - Referee Alpha
python referee.py --port 8001

# Terminal 3 - Referee Beta
python referee.py --port 8002
```

Every referee, at startup, activates the function `register_to_league` sending `REFEREE_REGISTER_REQUEST` to the League Manager.

### 8.2.4 Terminals 4-7 – Players

**Running Players**
```bash
# Terminal 4 - Player P01
python player.py --port 8101

# Terminal 5 - Player P02
python player.py --port 8102

# Terminal 6 - Player P03
python player.py --port 8103

# Terminal 7 - Player P04
python player.py --port 8104
```

Every player sends `LEAGUE_REGISTER_REQUEST` to the League Manager.

## 8.3 Step 1: Referee Registration
Every referee, immediately upon getting up, calls the client side to the League Manager.

### 8.3.1 Referee Registration Request

**Referee Registration Request – REFEREE_REGISTER_REQUEST**
```json
{
  "jsonrpc": "2.0",
  "method": "register_referee",
  "params": {
    "protocol": "league.v2",
    "message_type": "REFEREE_REGISTER_REQUEST",
    "sender": "referee:alpha",
    "timestamp": "2025-01-15T10:00:00Z",
    "conversation_id": "conv-ref-alpha-reg-001",
    "referee_meta": {
      "display_name": "Referee Alpha",
      "version": "1.0.0",
      "game_types": ["even_odd"],
      "contact_endpoint": "http://localhost:8001/mcp",
      "max_concurrent_matches": 2
    }
  },
  "id": 1
}
```

### 8.3.2 League Manager Response

**Referee Registration Response – REFEREE_REGISTER_RESPONSE**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "REFEREE_REGISTER_RESPONSE",
    "sender": "league_manager",
    "timestamp": "2025-01-15T10:00:01Z",
    "conversation_id": "conv-ref-alpha-reg-001",
    "status": "ACCEPTED",
    "referee_id": "REF01",
    "auth_token": "tok-ref01-abc123",
    "league_id": "league_2025_even_odd",
    "reason": null
  },
  "id": 1
}
```

The second referee (on port 8002) sends a similar request and receives `referee_id: "REF02"`.

## 8.4 Step 2: Player Registration
After the referees are registered, every player sends a registration request.

### 8.4.1 Player Registration Request

**Player Registration Request – LEAGUE_REGISTER_REQUEST**
```json
{
  "jsonrpc": "2.0",
  "method": "register_player",
  "params": {
    "protocol": "league.v2",
    "message_type": "LEAGUE_REGISTER_REQUEST",
    "sender": "player:alpha",
    "timestamp": "2025-01-15T10:05:00Z",
    "conversation_id": "conv-player-alpha-reg-001",
    "player_meta": {
      "display_name": "Agent Alpha",
      "version": "1.0.0",
      "game_types": ["even_odd"],
      "contact_endpoint": "http://localhost:8101/mcp"
    }
  },
  "id": 1
}
```

### 8.4.2 League Manager Response

**Player Registration Response – LEAGUE_REGISTER_RESPONSE**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "LEAGUE_REGISTER_RESPONSE",
    "sender": "league_manager",
    "timestamp": "2025-01-15T10:05:01Z",
    "conversation_id": "conv-player-alpha-reg-001",
    "status": "ACCEPTED",
    "player_id": "P01",
    "auth_token": "tok-p01-xyz789",
    "league_id": "league_2025_even_odd",
    "reason": null
  },
  "id": 1
}
```

Similarly:
- Player on port 8102 receives `player_id: "P02"`
- Player on port 8103 receives `player_id: "P03"`
- Player on port 8104 receives `player_id: "P04"`

The League Manager saves a map `player_id -> contact_endpoint` and `referee_id -> contact_endpoint`.

## 8.5 Step 3: Creating Game Board
After all players and referees are registered, the League Manager operates the logic `create_schedule` on the list of players for Round-Robin.

### 8.5.1 Game Board for Four Players

**Table 16: Round-Robin Game Board for Four Players**

| Match ID | Player A | Player B |
| :--- | :--- | :--- |
| R1M1 | P01 | P02 |
| R1M2 | P03 | P04 |
| R2M1 | P03 | P01 |
| R2M2 | P04 | P02 |
| R3M1 | P04 | P01 |
| R3M2 | P03 | P02 |

## 8.6 Step 4: Round Announcement

The League Manager sends to all players a `ROUND_ANNOUNCEMENT` notification. The games themselves start only when the referee invites the participants.

**Round Announcement – ROUND_ANNOUNCEMENT**
```json
{
  "jsonrpc": "2.0",
  "method": "notify_round",
  "params": {
    "protocol": "league.v2",
    "message_type": "ROUND_ANNOUNCEMENT",
    "sender": "league_manager",
    "timestamp": "2025-01-15T10:10:00Z",
    "conversation_id": "conv-round-1-announce",
    "league_id": "league_2025_even_odd",
    "round_id": 1,
    "matches": [
      {
        "match_id": "R1M1",
        "game_type": "even_odd",
        "player_A_id": "P01",
        "player_B_id": "P02",
        "referee_endpoint": "http://localhost:8001/mcp"
      },
      {
        "match_id": "R1M2",
        "game_type": "even_odd",
        "player_A_id": "P03",
        "player_B_id": "P04",
        "referee_endpoint": "http://localhost:8001/mcp"
      }
    ]
  },
  "id": 10
}
```

## 8.7 Step 5: Management of Single Match
We will describe the flow of Match R1M1: Player P01 against Player P02, Referee REF01.

### 8.7.1 Step 5.1: Invitation to Match
The referee passes the state of the match to `WAITING_FOR_PLAYERS` and sends `GAME_INVITATION` to every player.

**Invitation to P01:**
**GAME_INVITATION to P01**
```json
{
  "jsonrpc": "2.0",
  "method": "handle_game_invitation",
  "params": {
    "protocol": "league.v2",
    "message_type": "GAME_INVITATION",
    "sender": "referee:REF01",
    "timestamp": "2025-01-15T10:15:00Z",
    "conversation_id": "conv-r1m1-001",
    "auth_token": "tok-ref01-abc123",
    "league_id": "league_2025_even_odd",
    "round_id": 1,
    "match_id": "R1M1",
    "game_type": "even_odd",
    "role_in_match": "PLAYER_A",
    "opponent_id": "P02"
  },
  "id": 1001
}
```

**Invitation to P02:**
**GAME_INVITATION to P02**
```json
{
  "jsonrpc": "2.0",
  "method": "handle_game_invitation",
  "params": {
    "protocol": "league.v2",
    "message_type": "GAME_INVITATION",
    "sender": "referee:REF01",
    "timestamp": "2025-01-15T10:15:00Z",
    "conversation_id": "conv-r1m1-001",
    "auth_token": "tok-ref01-abc123",
    "league_id": "league_2025_even_odd",
    "round_id": 1,
    "match_id": "R1M1",
    "game_type": "even_odd",
    "role_in_match": "PLAYER_B",
    "opponent_id": "P01"
  },
  "id": 1002
}
```

### 8.7.2 Step 5.2: Arrival Confirmations
Every player returns `GAME_JOIN_ACK` within 5 seconds.

**Confirmation from P01:**
**GAME_JOIN_ACK from P01**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "GAME_JOIN_ACK",
    "sender": "player:P01",
    "timestamp": "2025-01-15T10:15:01Z",
    "conversation_id": "conv-r1m1-001",
    "auth_token": "tok-p01-xyz789",
    "match_id": "R1M1",
    "player_id": "P01",
    "arrival_timestamp": "2025-01-15T10:15:01Z",
    "accept": true
  },
  "id": 1001
}
```

**Confirmation from P02:**
**GAME_JOIN_ACK from P02**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "GAME_JOIN_ACK",
    "sender": "player:P02",
    "timestamp": "2025-01-15T10:15:02Z",
    "conversation_id": "conv-r1m1-001",
    "auth_token": "tok-p02-def456",
    "match_id": "R1M1",
    "player_id": "P02",
    "arrival_timestamp": "2025-01-15T10:15:02Z",
    "accept": true
  },
  "id": 1002
}
```

When the referee receives two positive ACKs in time, it passes the match state to `COLLECTING_CHOICES`.

### 8.7.3 Step 5.3: Collecting Choices
The referee sends `CHOOSE_PARITY_CALL` to every player.

**Choice Request to P01:**
**CHOOSE_PARITY_CALL to P01**
```json
{
  "jsonrpc": "2.0",
  "method": "choose_parity",
  "params": {
    "protocol": "league.v2",
    "message_type": "CHOOSE_PARITY_CALL",
    "sender": "referee:REF01",
    "timestamp": "2025-01-15T10:15:05Z",
    "conversation_id": "conv-r1m1-001",
    "auth_token": "tok-ref01-abc123",
    "match_id": "R1M1",
    "player_id": "P01",
    "game_type": "even_odd",
    "context": {
      "opponent_id": "P02",
      "round_id": 1,
      "your_standings": {
        "wins": 0,
        "losses": 0,
        "draws": 0
      }
    },
    "deadline": "2025-01-15T10:15:35Z"
  },
  "id": 1101
}
```

**Response P01 (Chose "even"):**
**CHOOSE_PARITY_RESPONSE from P01**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "CHOOSE_PARITY_RESPONSE",
    "sender": "player:P01",
    "timestamp": "2025-01-15T10:15:10Z",
    "conversation_id": "conv-r1m1-001",
    "auth_token": "tok-p01-xyz789",
    "match_id": "R1M1",
    "player_id": "P01",
    "parity_choice": "even"
  },
  "id": 1101
}
```

**Response P02 (Chose "odd"):**
**CHOOSE_PARITY_RESPONSE from P02**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "CHOOSE_PARITY_RESPONSE",
    "sender": "player:P02",
    "timestamp": "2025-01-15T10:15:12Z",
    "conversation_id": "conv-r1m1-001",
    "auth_token": "tok-p02-def456",
    "match_id": "R1M1",
    "player_id": "P02",
    "parity_choice": "odd"
  },
  "id": 1102
}
```

When two choices are received properly and in time, the referee passes the state to `DRAWING_NUMBER`.

### 8.7.4 Step 5.4: Number Draw and Winner Determination
The referee draws a number between 1 and 10, for example 8. It runs the module of game rules:
- `drawn_number = 8`
- `number_parity = "even"`
- P01 Choice -> "even" = Correct
- P02 Choice -> "odd" = Mistake
- `winner_player_id = "P01"`
- `status = "WIN"`

The match passes to `FINISHED`.

### 8.7.5 Step 5.5: Game End Notification
The referee sends `GAME_OVER` to the two players:

**Match End – GAME_OVER**
```json
{
  "jsonrpc": "2.0",
  "method": "notify_match_result",
  "params": {
    "protocol": "league.v2",
    "message_type": "GAME_OVER",
    "sender": "referee:REF01",
    "timestamp": "2025-01-15T10:15:30Z",
    "conversation_id": "conv-r1m1-001",
    "auth_token": "tok-ref01-abc123",
    "match_id": "R1M1",
    "game_type": "even_odd",
    "game_result": {
      "status": "WIN",
      "winner_player_id": "P01",
      "drawn_number": 8,
      "number_parity": "even",
      "choices": {
        "P01": "even",
        "P02": "odd"
      },
      "reason": "P01 chose even, number was 8 (even)"
    }
  },
  "id": 1201
}
```

Every player updates internal state (statistics, history) and returns a generic response.

### 8.7.6 Step 5.6: Reporting to League Manager
The referee reports `MATCH_RESULT_REPORT` to the league:

**Result Report – MATCH_RESULT_REPORT**
```json
{
  "jsonrpc": "2.0",
  "method": "report_match_result",
  "params": {
    "protocol": "league.v2",
    "message_type": "MATCH_RESULT_REPORT",
    "sender": "referee:REF01",
    "timestamp": "2025-01-15T10:15:35Z",
    "conversation_id": "conv-r1m1-report",
    "auth_token": "tok-ref01-abc123",
    "league_id": "league_2025_even_odd",
    "round_id": 1,
    "match_id": "R1M1",
    "game_type": "even_odd",
    "result": {
      "winner": "P01",
      "score": {
        "P01": 3,
        "P02": 0
      },
      "details": {
        "drawn_number": 8,
        "choices": {
          "P01": "even",
          "P02": "odd"
        }
      }
    }
  },
  "id": 1301
}
```

The League Manager updates the points table (Victory = 3 points).

## 8.8 Step 6: Round End and Standings Update
Round number 1 ends when all matches of the round (R1M1, R1M2) are received.
The League Manager:
1. Declares the round closed (Possible to move to `round_id=2`).
2. Calculates standings table: `points`, `wins`, `draws`, `losses`, `played` for every player.
3. Sends to all players a `LEAGUE_STANDINGS_UPDATE` message.

**Standings Update – LEAGUE_STANDINGS_UPDATE**
```json
{
  "jsonrpc": "2.0",
  "method": "update_standings",
  "params": {
    "protocol": "league.v2",
    "message_type": "LEAGUE_STANDINGS_UPDATE",
    "sender": "league_manager",
    "timestamp": "2025-01-15T10:20:00Z",
    "conversation_id": "conv-round-1-standings",
    "league_id": "league_2025_even_odd",
    "round_id": 1,
    "standings": [
      {
        "rank": 1,
        "player_id": "P01",
        "display_name": "Agent Alpha",
        "played": 1,
        "wins": 1,
        "draws": 0,
        "losses": 0,
        "points": 3
      },
      {
        "rank": 2,
        "player_id": "P03",
        "display_name": "Agent Gamma",
        "played": 1,
        "wins": 0,
        "draws": 1,
        "losses": 0,
        "points": 1
      },
      {
        "rank": 3,
        "player_id": "P04",
        "display_name": "Agent Delta",
        "played": 1,
        "wins": 0,
        "draws": 1,
        "losses": 0,
        "points": 1
      },
      {
        "rank": 4,
        "player_id": "P02",
        "display_name": "Agent Beta",
        "played": 1,
        "wins": 0,
        "draws": 0,
        "losses": 1,
        "points": 0
      }
    ]
  },
  "id": 1501
}
```

After sending the standings update, the League Manager sends a `ROUND_COMPLETED` message to mark the end of the round:

**Round End – ROUND_COMPLETED**
```json
{
  "jsonrpc": "2.0",
  "method": "notify_round_completed",
  "params": {
    "protocol": "league.v2",
    "message_type": "ROUND_COMPLETED",
    "sender": "league_manager",
    "timestamp": "2025-01-15T10:20:05Z",
    "conversation_id": "conv-round-1-complete",
    "league_id": "league_2025_even_odd",
    "round_id": 1,
    "matches_played": 2,
    "next_round_id": 2
  },
  "id": 1402
}
```

## 8.9 Step 7: League End
After the completion of all rounds, the League Manager sends a `LEAGUE_COMPLETED` message:

**League End – LEAGUE_COMPLETED**
```json
{
  "jsonrpc": "2.0",
  "method": "notify_league_completed",
  "params": {
    "protocol": "league.v2",
    "message_type": "LEAGUE_COMPLETED",
    "sender": "league_manager",
    "timestamp": "2025-01-15T12:00:00Z",
    "conversation_id": "conv-league-complete",
    "league_id": "league_2025_even_odd",
    "total_rounds": 3,
    "total_matches": 6,
    "champion": {
      "player_id": "P01",
      "display_name": "Agent Alpha",
      "points": 7
    },
    "final_standings": [
      {"rank": 1, "player_id": "P01", "points": 7},
      {"rank": 2, "player_id": "P03", "points": 5},
      {"rank": 3, "player_id": "P04", "points": 4},
      {"rank": 4, "player_id": "P02", "points": 2}
    ]
  },
  "id": 2001
}
```

## 8.10 Error Handling
When an error occurs, the League Manager or the Referee sends an error notification suitable to the schema.

### 8.10.1 Authentication Error

**Authentication Error – LEAGUE_ERROR**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "LEAGUE_ERROR",
    "sender": "league_manager",
    "timestamp": "2025-01-15T10:05:30Z",
    "conversation_id": "conv-error-001",
    "error_code": "E012",
    "error_description": "AUTH_TOKEN_INVALID",
    "context": {
      "provided_token": "tok-invalid-xxx",
      "action": "LEAGUE_QUERY"
    }
  },
  "id": 1502
}
```

### 8.10.2 Match Error – Response Time

**Match Error – GAME_ERROR**
```json
{
  "jsonrpc": "2.0",
  "method": "notify_game_error",
  "params": {
    "protocol": "league.v2",
    "message_type": "GAME_ERROR",
    "sender": "referee:REF01",
    "timestamp": "2025-01-15T10:16:00Z",
    "conversation_id": "conv-r1m1-001",
    "match_id": "R1M1",
    "error_code": "E001",
    "error_description": "TIMEOUT_ERROR",
    "affected_player": "P02",
    "action_required": "CHOOSE_PARITY_RESPONSE",
    "retry_count": 0,
    "max_retries": 3,
    "consequence": "Technical loss if no response after retries"
  },
  "id": 1103
}
```

## 8.11 Query Tools
The document defines a generic MCP tool for every agent allowing for debugging and clarification.

### 8.11.1 Standings Query from League Manager
A player wanting to verify their ranking calls the League Manager:

**Standings Query – LEAGUE_QUERY**
```json
{
  "jsonrpc": "2.0",
  "method": "league_query",
  "params": {
    "protocol": "league.v2",
    "message_type": "LEAGUE_QUERY",
    "sender": "player:P01",
    "timestamp": "2025-01-15T10:25:00Z",
    "conversation_id": "conv-query-standings-001",
    "auth_token": "tok-p01-xyz789",
    "league_id": "league_2025_even_odd",
    "query_type": "GET_STANDINGS"
  },
  "id": 1501
}
```

The League Manager returns a `result` containing a `standings` object identical to `LEAGUE_STANDINGS_UPDATE`.

### 8.11.2 Additional Tools
- **Tool in League Manager:** `get_standings` – Returns the standings table status.
- **Tool in Referee:** `get_match_state` – Returns the state of an existing match (for debugging needs).
- **Tool in Player:** `get_player_state` – Gives history of the games.

## 8.12 Full Flow Diagram
*(Diagram reference: Start -> League Manager Up -> Referees Register -> Players Register -> Create Schedule -> Round Announcement -> More Matches? (Yes -> Run Match -> No -> Update Standings -> More Rounds? -> Yes -> Round Announcement) (No -> End))*

## 8.13 Agents Roles Table

**Table 17: Roles of Agents in the System**

| Communicates with | Role in League | Port | Agent |
| :--- | :--- | :--- | :--- |
| Referees and Players | Orchestrator League, Table, Rounds | 8000 | League Manager |
| League Manager, Players | Orchestrator Games | 8001 | ahplA Referee |
| League Manager, Players | Orchestrator Games | 8002 | ateB Referee |
| Referee, League Manager | Player, `even/odd` Chooser | 8101 | P01 Player Agent |
| Referee, League Manager | Player | 8102 | P02 Player Agent |
| Referee, League Manager | Player | 8103 | P03 Player Agent |
| Referee, League Manager | Player | 8104 | P04 Player Agent |

## 8.14 Summary
This appendix presented the:
- **System Configuration:** Allocation of ports and terminals for 7 agents.
- **Order of Operation:** League Manager -> Referees -> Players.
- **Registration Flow:** `REFEREE_REGISTER` and `LEAGUE_REGISTER` with receiving `auth_token`.
- **Round Management:** `ROUND_ANNOUNCEMENT` and `ROUND_COMPLETED`.
- **Match Management:** From `GAME_INVITATION` to `GAME_OVER`.
- **Standings Update:** `MATCH_RESULT_REPORT` and `LEAGUE_STANDINGS_UPDATE`.
- **League End:** `LEAGUE_COMPLETED` with proclamation of champion.
- **Handling Errors:** `LEAGUE_ERROR` and `GAME_ERROR`.
- **Queries:** `LEAGUE_QUERY` for receiving updated information.

All communication is done via standard JSON-RPC 2.0 over HTTP. All messages include an Envelope unified with mandatory fields: `protocol`, `message_type`, `sender`, `timestamp` (in UTC zone), and `conversation_id`. The orchestrators (League Manager and Referees) manage the flow of notifications at every moment.
