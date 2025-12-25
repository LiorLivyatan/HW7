# 2 The General League Protocol

## 2.1 Protocol Principles
The protocol defines uniform rules. The rules allow different agents to communicate. Every student can implement an agent in any language they want. As long as the agent respects the protocol – it will participate in the league.

### 2.1.1 Separation into Three Layers
The system consists of three layers:
1. **League Layer** – Tournament management, player registration, standings table.
2. **Refereeing Layer** – Management of a single match, move verification, winner declaration.
3. **Game Rules Layer** – Logic of a specific game (Even/Odd, Rock-Paper-Scissors, etc.).

This separation is important. It allows replacing the game layer. The general protocol remains fixed.

## 2.2 Agent Types

### 2.2.1 League Manager
The League Manager is a single agent. It is responsible for:
- Registration of players to the league.
- Creating a game schedule (Round-Robin).
- Receiving results from referees.
- Calculation and publication of the standings table.

The League Manager operates as an MCP server on port 8000.

### 2.2.2 Referee
The referee manages a single match. Important: Before the referee can referee matches, they must register with the League Manager.
The referee is responsible for:
- **Registration to the League Manager** – Before the start of the league.
- Inviting two players to a match.
- Managing match turns.
- Verifying legality of moves.
- Declaring a result and reporting to the league.

The referee operates as an MCP server on port 8001. Multiple referees can be in the system (Ports 8001-8010).

### 2.2.3 Player Agent
The player agent represents a player in the league. It is responsible for:
- Registration to the league.
- Accepting invitations to matches.
- Choosing moves in the game.
- Updating internal state according to results.

Every player operates on a separate port (8101-8104).

## 2.3 Identifiers in the Protocol
Every component in the system is identified uniquely.

**Table 1: Identifiers in the League Protocol**

| Identifier Name | Type | Description |
| :--- | :--- | :--- |
| `league_id` | String | Unique league identifier |
| `round_id` | Integer | Round number in the league |
| `match_id` | String | Single match identifier |
| `game_type` | String | Game type |
| `player_id` | String | Player identifier |
| `referee_id` | String | Referee identifier |
| `conversation_id` | String | Conversation identifier |

### 2.3.1 Examples of Identifiers
- `league_id`: "league_2025_even_odd"
- `round_id`: 1, 2, 3...
- `match_id`: "R1M1" (Round 1, Match 1)
- `game_type`: "even_odd" or "tic_tac_toe"
- `player_id`: "P01", "P02", ..., "P20"
- `referee_id`: "REF01", "REF02"...

## 2.4 General Message Structure – Envelope
Every message in the protocol must include an "Envelope" with fixed fields. The envelope ensures consistency and enables tracking after messages.

**Message Envelope Structure**
```json
{
  "protocol": "league.v2",
  "message_type": "GAME_INVITATION",
  "sender": "referee:REF01",
  "timestamp": "2025-01-15T10:30:00Z",
  "conversation_id": "conv-r1m1-001",
  "auth_token": "tok_abc123def456...",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "match_id": "R1M1"
}
```

### 2.4.1 Mandatory Fields in the Envelope

**Table 2: Mandatory Fields in Every Message**

| Field | Type | Description |
| :--- | :--- | :--- |
| `protocol` | String | Protocol version, fixed "league.v2" |
| `message_type` | String | Message type (e.g., GAME_INVITATION) |
| `sender` | String | Sender identifier in format type:id |
| `timestamp` | String | Time stamp ISO 8601 in UTC zone |
| `conversation_id` | String | Unique conversation identifier |

### 2.4.2 Time Zone Requirement – UTC/GMT
**Mandatory:** All timestamps in the protocol must be in UTC/GMT time zone. This requirement ensures consistency between agents operating from different geographical locations.

**Table 3: Valid and Invalid Formats for Timestamp**

| Format | Valid? | Explanation |
| :--- | :--- | :--- |
| `2025-01-15T10:30:00Z` | ✅ | Z indicates UTC |
| `2025-01-15T10:30:00+00:00` | ✅ | Difference +00:00 equals UTC |
| `2025-01-15T10:30:00+02:00` | ❌ | Local time zone – Forbidden |
| `2025-01-15T10:30:00` | ❌ | No time zone – Forbidden |

**Important Note:** An agent sending a message with a time zone that is not UTC will receive error E021 (INVALID_TIMESTAMP).

### 2.4.3 Optional Fields

**Table 4: Optional Fields According to Context**

| Field | Type | Description |
| :--- | :--- | :--- |
| `auth_token` | String | Authentication token (Mandatory after registration) |
| `league_id` | String | League identifier |
| `round_id` | Integer | Round number |
| `match_id` | String | Match identifier |

### 2.4.4 `sender` Field Format
The `sender` field identifies the message sender:
- `league_manager` – League Manager.
- `referee:REF01` – Referee with identifier REF01.
- `player:P01` – Player with identifier P01.

### 2.4.5 Authentication Token – `auth_token`
After successful registration, every agent receives an `auth_token`. The token must appear in every message sent after registration. This prevents impersonation of other agents.

**Receiving Token in Registration Response**
```json
{
  "message_type": "LEAGUE_REGISTER_RESPONSE",
  "status": "ACCEPTED",
  "player_id": "P01",
  "auth_token": "tok_p01_abc123def456ghi789..."
}
```

## 2.5 General League Flow

### 2.5.1 Step 1: Referee Registration
In the first stage, every referee registers to the league. The referee sends a registration request to the League Manager. The manager assigns a `referee_id` and saves the referee's address.

*(Diagram reference: Referee sends REFEREE_REGISTER_REQUEST to League Manager, receives REFEREE_REGISTER_RESPONSE)*

### 2.5.2 Step 2: Player Registration
After referee registration, every player registers to the league. The player sends a registration request to the League Manager. The League Manager assigns a `player_id` and approves.

*(Diagram reference: Player Agent sends REGISTER_REQUEST to League Manager, receives REGISTER_RESPONSE)*

### 2.5.3 Step 3: Creating Game Schedule
After all players are registered, the League Manager creates a game schedule. The schedule is based on the Round-Robin method. Every player plays against every other player.

### 2.5.4 Step 4: Announcement of Round
Before every round, the League Manager publishes a `ROUND_ANNOUNCEMENT` message. The message details all the matches in the round. The League Manager assigns to every referee a list of matches from the registered list.

### 2.5.5 Step 5: Game Management
The referee invites players to a match. It manages the match according to the game rules. At the end, it reports a result to the League Manager.

### 2.5.6 Step 6: Updating Standings
After every round, the League Manager updates the standings table. It publishes the table to all players.

## 2.6 General Flow Diagram

*(Diagram reference: Start -> Register Referees -> Register Players -> Create Schedule -> More Matches? (Yes -> Run Match -> More Matches?) (No -> Update Standings -> End))*

## 2.7 Response Times – Timeouts
For every message type a maximum response time is defined. If the agent does not answer in time, the action is considered a failure.

**Table 5: Response Times by Message Type**

| Message Type | Timeout | Comments |
| :--- | :--- | :--- |
| `REFEREE_REGISTER` | 10 sec | Referee registration to league |
| `LEAGUE_REGISTER` | 10 sec | Player registration to league |
| `GAME_JOIN_ACK` | 5 sec | Confirmation of arrival to match |
| `CHOOSE_PARITY` | 30 sec | Choice of Even/Odd |
| `GAME_OVER` | 5 sec | Receiving match result |
| `MATCH_RESULT_REPORT` | 10 sec | Reporting result to league |
| `LEAGUE_QUERY` | 10 sec | Information query |
| All the rest | 10 sec | Default |

## 2.8 Agent Lifecycle
Every agent (player, referee) goes through defined states during the league.

### 2.8.1 Agent States
- **INIT** – The agent has started but not yet registered.
- **REGISTERED** – The agent registered successfully and received `auth_token`.
- **ACTIVE** – The agent is active and participating in games.
- **SUSPENDED** – The agent is temporarily suspended (not responding).
- **SHUTDOWN** – The agent has finished activity.

### 2.8.2 State Transition Diagram

*(Diagram reference: INIT -> (register) -> REGISTERED -> (league_start) -> ACTIVE -> (league_end) -> SHUTDOWN. ACTIVE <-> (timeout recover / max_fail) <-> SUSPENDED)*

## 2.9 Error Handling
The protocol defines two types of error messages:

### 2.9.1 League Error – LEAGUE_ERROR
The League Manager sends this message when an error occurs at the league level.

**Example of League Error**
```json
{
  "protocol": "league.v2",
  "message_type": "LEAGUE_ERROR",
  "sender": "league_manager",
  "timestamp": "2025-01-15T10:35:00Z",
  "error_code": "E005",
  "error_name": "PLAYER_NOT_REGISTERED",
  "error_description": "Player ID not found in registry",
  "context": {
    "player_id": "P99"
  },
  "retryable": false
}
```

### 2.9.2 Game Error – GAME_ERROR
The referee sends this message when an error occurs in the game.

**Example of Game Error**
```json
{
  "protocol": "league.v2",
  "message_type": "GAME_ERROR",
  "sender": "referee:REF01",
  "timestamp": "2025-01-15T10:31:00Z",
  "match_id": "R1M1",
  "player_id": "P01",
  "error_code": "E001",
  "error_name": "TIMEOUT_ERROR",
  "error_description": "Response not received within 30 seconds",
  "game_state": "COLLECTING_CHOICES",
  "retryable": true,
  "retry_count": 1,
  "max_retries": 3
}
```

### 2.9.3 Common Error Codes

**Table 6: Main Error Codes**

| Code | Name | Description |
| :--- | :--- | :--- |
| E001 | `TIMEOUT_ERROR` | Response not received in time |
| E003 | `MISSING_REQUIRED_FIELD` | Mandatory field missing |
| E004 | `INVALID_PARITY_CHOICE` | Illegal choice |
| E005 | `PLAYER_NOT_REGISTERED` | Player not registered |
| E009 | `CONNECTION_ERROR` | Connection failure |
| E011 | `AUTH_TOKEN_MISSING` | Authentication token missing |
| E012 | `AUTH_TOKEN_INVALID` | Token invalid |

### 2.9.4 Retry Policy
Certain errors are retryable:
- **Maximum Retries:** 3
- **Wait between Retries:** 2 seconds
- **Retryable Errors:** E001 (timeout), E009 (connection)

After exhausting retries – Technical Loss (TECHNICAL_LOSS).

## 2.10 Version Compatibility

### 2.10.1 Version Recognition
At the time of registration, every agent declares the protocol version it supports. The League Manager checks compatibility before registration approval.

**Version Declaration in Registration Request**
```json
{
  "message_type": "LEAGUE_REGISTER_REQUEST",
  "player_meta": {
    "display_name": "Agent Alpha",
    "version": "1.0.0",
    "protocol_version": "2.1.0",
    "game_types": ["even_odd"]
  }
}
```

### 2.10.2 Compatibility Policy
- **Current Version:** 2.1.0
- **Minimum Supported Version:** 2.0.0
- **Agents with older version will receive error E018 (PROTOCOL_VERSION_MISMATCH).**

## 2.11 Important Principles

### 2.11.1 Single Source of Truth
The referee is the source of truth for the game state. Players do not keep their own state. They rely on the information the referee sends.

### 2.11.2 Communication via Orchestrator
Players do not talk directly with each other. All communication passes through the referee or the League Manager. This ensures the protocol is kept.

### 2.11.3 Handling Failures
If a player does not respond:
1. The referee sends a `GAME_ERROR` message with `retryable=true`.
2. The player receives up to 3 attempts.
3. After exhausting attempts – Technical Loss (TECHNICAL_LOSS).
