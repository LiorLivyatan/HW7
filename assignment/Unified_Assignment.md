# Unified Assignment: AI Agents and MCP League

This document aggregates all chapters of the assignment into a single reference. For ease of navigation and specific file referencing, each chapter is also available as a separate file.

## Chapter Overview

*   **[Chapter 1: Introduction](Chapter_1.md)** - Definitions of AI Agents, the MCP Protocol, and the assignment goals.
*   **[Chapter 2: General League Protocol](Chapter_2.md)** - Architecture, agent types, communication layers, and agent lifecycle.
*   **[Chapter 3: Even/Odd Game](Chapter_3.md)** - Specific rules and logic for the game used in this exercise.
*   **[Chapter 4: JSON Message Structures](Chapter_4.md)** - The definitive API reference for all 18 protocol messages.
*   **[Chapter 5: Implementation Guide](Chapter_5.md)** - Code examples (Python/FastAPI) and implementation patterns.
*   **[Chapter 6: Homework Requirements](Chapter_6.md)** - Mandatory tasks, grading criteria, and submission guidelines.
*   **[Chapter 7: Learning through the League](Chapter_7.md)** - Theoretical background and educational objectives.
*   **[Chapter 8: Running the League System](Chapter_8.md)** - Step-by-step guide to running the system locally.
*   **[Chapter 9: League Data Protocol](Chapter_9.md)** - Structure of configuration, runtime data, and log files.
*   **[Chapter 10: Python Toolkit](Chapter_10.md)** - Documentation for the `league_sdk` library.
*   **[Chapter 11: Project Structure](Chapter_11.md)** - Recommended directory tree and file organization.
*   **[Chapter 12: References](Chapter_12.md)** - Bibliography.

---

# 1 Introduction: AI Agents and MCP Protocol

## 1.1 What is an AI Agent?
An AI agent is autonomous software. The agent receives information from the environment. It processes the information. After that, it performs actions.

An AI agent is different from a regular program. A regular program performs instructions set in advance. An AI agent decides by itself what to do. The decision is based on the current situation.

### 1.1.1 Characteristics of an AI Agent
Every AI agent has a number of characteristics:
- **Autonomy** – The agent operates independently.
- **Perception** – The agent receives information from the environment.
- **Action** – The agent influences the environment.
- **Goal-oriented** – The agent has a defined goal.

In the book by Dr. Yoram Segal "AI Agents with MCP" [1], it is explained how agents communicate. The book presents the MCP protocol in detail. We will use these principles in the exercise.

## 1.2 MCP Protocol – Model Context Protocol
MCP is a communication protocol. The protocol was developed by Anthropic. It allows AI agents to communicate with each other.

### 1.2.1 Protocol Principles
The protocol is based on a number of principles:
1. **Structured Messages** – Every message is a JSON object.
2. **JSON-RPC 2.0 Standard** – The protocol uses this standard.
3. **Tools** – Agents expose functions as "tools".
4. **Flexible Transport** – Possible to use HTTP or stdio.

### 1.2.2 Architecture Host/Server
In the MCP system there are two types of components:

**MCP Server** – A component that provides services. The server exposes "tools" that enable calling them. Every tool is a function with defined parameters.

**Host** – A component that coordinates between servers. The host sends requests to servers. It receives answers and processes them.

*(Diagram reference: Host (Orchestrator) connected via JSON-RPC to MCP Server 1, MCP Server 2, MCP Server 3)*

## 1.3 Communication HTTP on localhost
In this exercise we will use HTTP communication. Every agent will operate on a different port on localhost.

### 1.3.1 Port Definition
We will define fixed ports for every agent:
- League Manager – Port 8000
- Referee – Port 8001
- Players – Ports 8101 to 8104

Every agent implements a simple HTTP server. The server accepts POST requests at the path `/mcp`. The content of the request is JSON-RPC 2.0.

### 1.3.2 Example of Agent Address
Address of League Manager server:
`http://localhost:8000/mcp`

Address of first player server:
`http://localhost:8101/mcp`

## 1.4 Message Structure JSON-RPC
Every message in the protocol is a JSON object. The message has a fixed structure.

**Basic Structure of a Message**
```json
{
  "jsonrpc": "2.0",
  "method": "tool_name",
  "params": {
    "param1": "value1",
    "param2": "value2"
  },
  "id": 1
}
```

Fields in the message:
- `jsonrpc` – Protocol version, always "2.0".
- `method` – Name of the tool we want to operate.
- `params` – Parameters for the tool.
- `id` – Unique identifier for the request.

## 1.5 Goal of the Exercise
In this exercise we will build a league system for AI agents. The system will include three types of agents:
1. **League Manager** – Manages the league, including registration of players and referees.
2. **Referee** – Signs up to the league manager and manages single games.
3. **Player Agents** – Participate in the games.

**Registration Process:** Before the start of the league, referees and also players must register with the League Manager. The League Manager keeps a list of available referees and assigns them to games.

The specific game in the exercise is "Even/Odd". The general protocol allows replacing the game in the future. It will be possible to use Rock-Paper-Scissors, 12 Questions, or other games.

### 1.5.1 Learning Objective
At the end of the exercise you will be able to:
- Understand the MCP protocol.
- Build a simple MCP server.
- Communicate between different agents.
- Run a full league in your environment.
- Verify compatibility of the protocol with other students.

**Important:** All students will use the same protocol. This will allow your agents to play against this in the future.

---

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

---

# 3 Even/Odd Game

## 3.1 Description of the Game
Even/Odd is a simple game. The game is suitable for demonstrating the league protocol.

### 3.1.1 Game Rules
1. Two players participate in the game.
2. Each player chooses "Even" or "Odd".
3. The choices are made in parallel, without knowing the opponent's choice.
4. The referee draws a number between 1 and 10.
5. If the number is even – whoever chose "Even" wins.
6. If the number is odd – whoever chose "Odd" wins.
7. If both chose the same thing and lost – Draw.

### 3.1.2 Example of a Game
Assume a match between Player A and Player B:

**Table 7: Example of Even/Odd Game**

| Player A Choice | Player B Choice | Number | Result |
| :--- | :--- | :--- | :--- |
| even | odd | 8 (even) | A wins |
| even | odd | 7 (odd) | B wins |
| odd | odd | 4 (even) | Draw |

## 3.2 Single Match Flow

### 3.2.1 Step 1: Invitation to Match
The referee sends an invitation to both players. The invitation includes:
- Match identifier (`match_id`).
- Round identifier (`round_id`).
- Game type (`game_type`).

### 3.2.2 Step 2: Arrival Confirmation
Every player confirms receipt of the invitation. The confirmation includes a timestamp.

### 3.2.3 Step 3: Collection of Choices
The referee turns to every player separately. It requests a choice: "even" or "odd". The player returns their choice.

**Important:** The players do not see the opponent's choice.

### 3.2.4 Step 4: Number Draw
After receiving both choices, the referee draws a number. The number is between 1 and 10. The draw must be random.

### 3.2.5 Step 5: Determination of Winner
The referee checks:
- If the number is even and a player chose "even" – they win.
- If the number is odd and a player chose "odd" – they win.
- If both guessed correctly/incorrectly – Draw.

### 3.2.6 Step 6: Result Reporting
The referee sends:
1. `GAME_OVER` message to both players.
2. `MATCH_RESULT_REPORT` message to the League Manager.

## 3.3 Game States
The game passes between defined states:

**State Diagram**
*(Diagram reference: WAITING FOR_PLAYERS -> (Both ACK) -> COLLECTING CHOICES -> (Both chose) -> DRAWING NUMBER -> (Result) -> FINISHED)*

### 3.3.1 State WAITING_FOR_PLAYERS
The game starts in this state. The referee waits for the players to confirm arrival. Transition: When both players sent `GAME_JOIN_ACK`.

### 3.3.2 State COLLECTING_CHOICES
The referee collects choices from the players. It calls `choose_parity` for every player. Transition: When both choices are received.

### 3.3.3 State DRAWING_NUMBER
The referee draws a number and determines a winner. Transition: Automatic after calculation.

### 3.3.4 State FINISHED
The game is finished. The result is reported.

## 3.4 Scoring Method

### 3.4.1 Points for Match

**Table 8: Points Table**

| Result | Points to Winner | Points to Loser |
| :--- | :--- | :--- |
| Victory | 3 | 0 |
| Draw | 1 | 1 |
| Loss | 0 | 0 |

### 3.4.2 Ranking in League
The ranking is determined by:
1. Total points (descending).
2. Number of victories (descending).
3. Goal difference (descending) - *Note: In Even/Odd there are no goals, so this might refer to a tie-breaker if applicable, or just generic league rules.*

## 3.5 Round-Robin League
In a league with 4 players, every player plays against everyone.

### 3.5.1 Number of Matches
For $n$ players:
- Number of matches in the league: $\frac{n(n-1)}{2}$
- For 4 players: $6 = \frac{4 \times 3}{2}$ matches

### 3.5.2 Example Game Board

**Table 9: Game Board for 4 Players**

| Match | Player A | Player B |
| :--- | :--- | :--- |
| R1M1 | P01 | P02 |
| R1M2 | P03 | P04 |
| R2M1 | P01 | P03 |
| R2M2 | P02 | P04 |
| R3M1 | P01 | P04 |
| R3M2 | P02 | P03 |

## 3.6 Strategies for Players

### 3.6.1 Random Strategy
The simplest approach. The player chooses randomly "even" or "odd". The chance to win is 50%.

**Random Strategy**
```python
import random

def choose_parity_random():
    return random.choice(["even", "odd"])
```

### 3.6.2 History Based Strategy
The player remembers previous results. It tries to identify patterns in the draw.
**Note:** Since the draw is random, this strategy will not improve results in the long run.

### 3.6.3 LLM Based Strategy
The player can use a language model. It builds a prompt and asks the model.

**Example for prompt**
```python
prompt = """
You are playing Even/Odd game.
Choose "even" or "odd".
Previous results: even won 3 times, odd won 2 times.
Your choice (one word only):
"""
```

**Note:** Usage of LLM is interesting but will not improve performance statistically. The game is a game of luck.

## 3.7 Game Rules Module
The rules module is a separate component in the referee. It defines the specific logic for the game.

### 3.7.1 Module Interface
The module provides functions:
- `init_game_state()` – Initialization of game state.
- `validate_choice(choice)` – Verification of legal choice.
- `draw_number()` – Number draw.
- `determine_winner(choices, number)` – Determination of winner.

### 3.7.2 Benefit of Separation
In the future, it is possible to replace the module. Instead of Even/Odd, it is possible:
- Tic-Tac-Toe.
- 21 Questions.
- Memory Game.

The general protocol remains unchanged. Only the rules module changes.

## 3.8 Extension for Additional Games
The protocol is designed to be general and not specific to Even/Odd. This section describes the generic abstraction layer allowing the addition of additional games.

### 3.8.1 Generic Move Abstraction – GAME_MOVE
Generic `GAME_MOVE_CALL` and `choose_PARITY_RESPONSE` messages replace the private case of `CHOOSE_PARITY_*`.

**Table 10: Parallelism between Specific and Generic Messages**

| Specific Message | Generic Message |
| :--- | :--- |
| `CHOOSE_PARITY_CALL` | `GAME_MOVE_CALL` |
| `CHOOSE_PARITY_RESPONSE` | `GAME_MOVE_RESPONSE` |

### 3.8.2 Generic Move Message Structure

**Generic Move Request – GAME_MOVE_CALL**
```json
{
  "protocol": "league.v2",
  "message_type": "GAME_MOVE_CALL",
  "sender": "referee:REF01",
  "timestamp": "2025-01-15T10:30:15Z",
  "match_id": "R1M1",
  "player_id": "P01",
  "game_type": "even_odd",
  "move_request": {
    "move_type": "choose_parity",
    "valid_options": ["even", "odd"],
    "context": {}
  },
  "deadline": "2025-01-15T10:30:45Z"
}
```

**Generic Move Response – GAME_MOVE_RESPONSE**
```json
{
  "protocol": "league.v2",
  "message_type": "GAME_MOVE_RESPONSE",
  "sender": "player:P01",
  "timestamp": "2025-01-15T10:30:20Z",
  "match_id": "R1M1",
  "player_id": "P01",
  "game_type": "even_odd",
  "move_data": {
    "move_type": "choose_parity",
    "choice": "even"
  }
}
```

### 3.8.3 Registration of Game Types – Game Registry
The league manager holds a registry of supported game types:

**Game Registration**
```json
{
  "game_registry": {
    "even_odd": {
      "display_name": "Even/Odd",
      "move_types": ["choose_parity"],
      "valid_choices": {
        "choose_parity": ["even", "odd"]
      },
      "min_players": 2,
      "max_players": 2
    },
    "tic_tac_toe": {
      "display_name": "Tic-Tac-Toe",
      "move_types": ["place_mark"],
      "valid_choices": {
        "place_mark": ["0-8"]
      },
      "min_players": 2,
      "max_players": 2
    }
  }
}
```

### 3.8.4 Advantages of Abstraction
1. **Adding New Games** – Without change in the basic protocol.
2. **Discovery Capabilities** – A player can ask which games are supported.
3. **Uniform Validation** – The referee verifies that the move is legal according to the schema.
4. **Forward Compatibility** – Old agents can continue to work with specific messages.

**Note:** In the exercise we use the specific messages (`CHOOSE_PARITY_*`). The generic abstraction is presented for the purpose of understanding the architecture.

---

# 4 JSON Message Structures
This chapter defines all protocol messages. **Very important:** All students must use these structures exactly. This will allow your agents to communicate with each other.

## 4.1 Referee Registration Messages to League

### 4.1.1 Referee Registration Request – REFEREE_REGISTER_REQUEST
- **From:** referee (Referee)
- **To:** league_manager (League Manager)
- **Expected Response:** REFEREE_REGISTER_RESPONSE

A referee sends this request to the manager before the league starts.

**Referee Registration Request to League**
```json
{
  "message_type": "REFEREE_REGISTER_REQUEST",
  "referee_meta": {
    "display_name": "Referee Alpha",
    "version": "1.0.0",
    "game_types": ["even_odd"],
    "contact_endpoint": "http://localhost:8001/mcp",
    "max_concurrent_matches": 2
  }
}
```

**Mandatory Fields:**
- `display_name` – Display name of the referee.
- `version` – Version of the referee.
- `game_types` – List of game types the referee knows how to judge.
- `contact_endpoint` – Server address of the referee.
- `max_concurrent_matches` – Maximum number of games the referee can manage in parallel.

### 4.1.2 Referee Registration Response – REFEREE_REGISTER_RESPONSE
- **From:** league_manager (League Manager)
- **To:** referee (Referee who sent the request)
- **Expected Response:** None (Response message)

The League Manager returns this response to the referee.

**Referee Registration Response to League**
```json
{
  "message_type": "REFEREE_REGISTER_RESPONSE",
  "status": "ACCEPTED",
  "referee_id": "REF01",
  "reason": null
}
```

**Fields:**
- `status` – "ACCEPTED" or "REJECTED".
- `referee_id` – Identifier assigned to the referee (only if accepted).
- `reason` – Rejection reason (only if rejected).

## 4.2 Player Registration Messages to League

### 4.2.1 Player Registration Request – LEAGUE_REGISTER_REQUEST
- **From:** player (Player)
- **To:** league_manager (League Manager)
- **Expected Response:** LEAGUE_REGISTER_RESPONSE

A player sends this request to the League Manager.

**Registration Request to League**
```json
{
  "message_type": "LEAGUE_REGISTER_REQUEST",
  "player_meta": {
    "display_name": "Agent Alpha",
    "version": "1.0.0",
    "game_types": ["even_odd"],
    "contact_endpoint": "http://localhost:8101/mcp"
  }
}
```

**Mandatory Fields:**
- `display_name` – Display name of the player.
- `version` – Version of the agent.
- `game_types` – List of supported games.
- `contact_endpoint` – Server address of the player.

### 4.2.2 Registration Response – LEAGUE_REGISTER_RESPONSE
- **From:** league_manager (League Manager)
- **To:** player (Player who sent the request)
- **Expected Response:** None (Response message)

The League Manager returns this response.

**Registration Response to League**
```json
{
  "message_type": "LEAGUE_REGISTER_RESPONSE",
  "status": "ACCEPTED",
  "player_id": "P01",
  "reason": null
}
```

**Fields:**
- `status` – "ACCEPTED" or "REJECTED".
- `player_id` – Identifier assigned to the player (only if accepted).
- `reason` – Rejection reason (only if rejected).

## 4.3 Round Messages

### 4.3.1 Round Announcement – ROUND_ANNOUNCEMENT
- **From:** league_manager (League Manager)
- **To:** players (All registered players)
- **Expected Response:** None (Broadcast message)

The League Manager sends before every round.

**Round Announcement**
```json
{
  "message_type": "ROUND_ANNOUNCEMENT",
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
}
```

## 4.4 Match Messages

### 4.4.1 Match Invitation – GAME_INVITATION
- **From:** referee (League Manager/Referee - *Translation Note: Usually Referee based on previous context, PDF says Referee*)
- **To:** player (Every one of the two players in the match)
- **Expected Response:** GAME_JOIN_ACK

The referee sends to every player.

**Match Invitation**
```json
{
  "message_type": "GAME_INVITATION",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "match_id": "R1M1",
  "game_type": "even_odd",
  "role_in_match": "PLAYER_A",
  "opponent_id": "P02",
  "conversation_id": "conv-r1m1-001"
}
```

### 4.4.2 Arrival Confirmation – GAME_JOIN_ACK
- **From:** player (The player who received the invitation)
- **To:** referee (The referee who sent the invitation)
- **Expected Response:** CHOOSE_PARITY_CALL (After all players confirm)

The player confirms receiving the invitation.

**Match Arrival Confirmation**
```json
{
  "message_type": "GAME_JOIN_ACK",
  "match_id": "R1M1",
  "player_id": "P01",
  "arrival_timestamp": "2025-01-15T10:30:00Z",
  "accept": true
}
```

## 4.5 Messages of Choice in Even/Odd Game

### 4.5.1 Choice Request – CHOOSE_PARITY_CALL
- **From:** referee (The referee)
- **To:** player (Every one of the players in the match)
- **Expected Response:** CHOOSE_PARITY_RESPONSE

The referee asks the player to choose.

**Choice Request**
```json
{
  "message_type": "CHOOSE_PARITY_CALL",
  "match_id": "R1M1",
  "player_id": "P01",
  "game_type": "even_odd",
  "context": {
    "opponent_id": "P02",
    "round_id": 1,
    "your_standings": {
      "wins": 2,
      "losses": 1,
      "draws": 0
    }
  },
  "deadline": "2025-01-15T10:30:30Z"
}
```

### 4.5.2 Choice Response – CHOOSE_PARITY_RESPONSE
- **From:** player (The player)
- **To:** referee (The referee who sent the request)
- **Expected Response:** GAME_OVER (After all players answer)

The player returns their choice.

**Choice Response**
```json
{
  "message_type": "CHOOSE_PARITY_RESPONSE",
  "match_id": "R1M1",
  "player_id": "P01",
  "parity_choice": "even"
}
```

**Important:** Your value of `parity_choice` must be "even" or "odd" exactly.

## 4.6 Result Messages

### 4.6.1 Match End – GAME_OVER
- **From:** referee (The referee)
- **To:** players (Both players in the match)
- **Expected Response:** None (Update message)

The referee sends to both players.

**Match End Message**
```json
{
  "message_type": "GAME_OVER",
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
    }
  },
  "reason": "P01 chose even, number was 8 (even)"
}
```

**Possible Values for status:**
- "WIN" – There is a winner.
- "DRAW" – Draw.
- "TECHNICAL_LOSS" – Technical loss (timeout, etc.).

### 4.6.2 Result Report to League – MATCH_RESULT_REPORT
- **From:** referee (The referee managing the match)
- **To:** league_manager (League Manager)
- **Expected Response:** LEAGUE_STANDINGS_UPDATE (League Manager will broadcast to all players)

The referee sends to the League Manager.

**Result Report to League**
```json
{
  "message_type": "MATCH_RESULT_REPORT",
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
}
```

## 4.7 Standings Messages

### 4.7.1 Standings Update – LEAGUE_STANDINGS_UPDATE
- **From:** league_manager (League Manager)
- **To:** players (All registered players)
- **Expected Response:** None (Broadcast message)

League Manager sends to all players.

**Standings Table Update**
```json
{
  "message_type": "LEAGUE_STANDINGS_UPDATE",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "standings": [
    {
      "rank": 1,
      "player_id": "P01",
      "display_name": "Agent Alpha",
      "played": 2,
      "wins": 2,
      "draws": 0,
      "losses": 0,
      "points": 6
    },
    {
      "rank": 2,
      "player_id": "P03",
      "display_name": "Agent Gamma",
      "played": 2,
      "wins": 1,
      "draws": 1,
      "losses": 0,
      "points": 4
    }
  ]
}
```

## 4.8 Round and League End Messages

### 4.8.1 Round End – ROUND_COMPLETED
- **From:** league_manager (League Manager)
- **To:** players (All registered players)
- **Expected Response:** None (Broadcast message)

The League Manager sends this message at the end of round.

**Round End Message**
```json
{
  "protocol": "league.v2",
  "message_type": "ROUND_COMPLETED",
  "sender": "league_manager",
  "timestamp": "2025-01-15T12:00:00Z",
  "conversation_id": "conv-round1-complete",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "matches_completed": 2,
  "next_round_id": 2,
  "summary": {
    "total_matches": 2,
    "wins": 1,
    "draws": 1,
    "technical_losses": 0
  }
}
```

**Fields:**
- `round_id` – The round that ended.
- `matches_completed` – Number of matches that were completed.
- `next_round_id` – The next round, or null if this is the last round.
- `summary` – Statistical summary of the round.

### 4.8.2 League End – LEAGUE_COMPLETED
- **From:** league_manager (League Manager)
- **To:** all_agents (All players and referees)
- **Expected Response:** None (End notification)

The League Manager sends this message at the end of the league.

**League End Message**
```json
{
  "protocol": "league.v2",
  "message_type": "LEAGUE_COMPLETED",
  "sender": "league_manager",
  "timestamp": "2025-01-20T18:00:00Z",
  "conversation_id": "conv-league-complete",
  "league_id": "league_2025_even_odd",
  "total_rounds": 3,
  "total_matches": 6,
  "champion": {
    "player_id": "P01",
    "display_name": "Agent Alpha",
    "points": 9
  },
  "final_standings": [
    {"rank": 1, "player_id": "P01", "points": 9},
    {"rank": 2, "player_id": "P03", "points": 5},
    {"rank": 3, "player_id": "P02", "points": 3},
    {"rank": 4, "player_id": "P04", "points": 1}
  ]
}
```

**Fields:**
- `champion` – Details of the champion.
- `final_standings` – Final standings table.
- `total_matches`, `total_rounds` – Statistics of the league.

## 4.9 Query Messages

### 4.9.1 League Query – LEAGUE_QUERY
- **From:** player or referee (Player or Referee)
- **To:** league_manager (League Manager)
- **Expected Response:** LEAGUE_QUERY_RESPONSE

A player or referee sends a query to the League Manager to receive information.

**Next Match Query**
```json
{
  "protocol": "league.v2",
  "message_type": "LEAGUE_QUERY",
  "sender": "player:P01",
  "timestamp": "2025-01-15T14:00:00Z",
  "conversation_id": "conv-query-001",
  "auth_token": "tok_p01_abc123...",
  "league_id": "league_2025_even_odd",
  "query_type": "GET_NEXT_MATCH",
  "query_params": {
    "player_id": "P01"
  }
}
```

**Types of Queries (`query_type`):**
- `GET_STANDINGS` – Receiving standings table.
- `GET_SCHEDULE` – Receiving game schedule.
- `GET_NEXT_MATCH` – Receiving details of the next match.
- `GET_PLAYER_STATS` – Receiving statistics of a player.

### 4.9.2 Query Response – LEAGUE_QUERY_RESPONSE
- **From:** league_manager (League Manager)
- **To:** player or referee (Sender of the query)
- **Expected Response:** None (Response notification)

The League Manager returns a response to the query.

**Response to Next Match**
```json
{
  "protocol": "league.v2",
  "message_type": "LEAGUE_QUERY_RESPONSE",
  "sender": "league_manager",
  "timestamp": "2025-01-15T14:00:01Z",
  "conversation_id": "conv-query-001",
  "query_type": "GET_NEXT_MATCH",
  "success": true,
  "data": {
    "next_match": {
      "match_id": "R2M1",
      "round_id": 2,
      "opponent_id": "P03",
      "referee_endpoint": "http://localhost:8001/mcp"
    }
  }
}
```

**Fields:**
- `success` – Whether the query succeeded.
- `data` – Result of the query (Structure changes according to `query_type`).
- `error` – Error details if `success=false`.

## 4.10 Error Messages

### 4.10.1 League Level Error – LEAGUE_ERROR
- **From:** league_manager (League Manager)
- **To:** agent (Agent causing the error)
- **Expected Response:** None (Error notification)

When an error occurs in actions related to the league, the League Manager sends a `LEAGUE_ERROR` message.

**LEAGUE_ERROR – Example**
```json
{
  "protocol": "league.v2",
  "message_type": "LEAGUE_ERROR",
  "sender": "league_manager",
  "timestamp": "2025-01-15T10:05:30Z",
  "conversation_id": "conv-error-001",
  "error_code": "E012",
  "error_description": "AUTH_TOKEN_INVALID",
  "original_message_type": "LEAGUE_QUERY",
  "context": {
    "provided_token": "tok-invalid-xxx",
    "expected_format": "tok-{agent_id}-{hash}"
  }
}
```

**Fields:**
- `error_code` – Error code from table of error codes.
- `error_description` – Name of the error.
- `original_message_type` – Type of message that caused the error.
- `context` – Additional information for debugging.

### 4.10.2 Match Level Error – GAME_ERROR
- **From:** referee (The referee managing the match)
- **To:** player (The player causing the error or affected by it)
- **Expected Response:** None (Error notification)

When an error occurs during a match, the referee sends a `GAME_ERROR` message.

**GAME_ERROR – Match Error**
```json
{
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
  "retry_info": {
    "retry_count": 1,
    "max_retries": 3,
    "next_retry_at": "2025-01-15T10:16:02Z"
  },
  "consequence": "Technical loss if max retries exceeded"
}
```

**Fields:**
- `match_id` – Identifier of the match where the error occurred.
- `affected_player` – The affected player.
- `action_required` – The action that failed.
- `retry_info` – Information on retries (if relevant).
- `consequence` – The outcome if the error is not resolved.

## 4.11 Summary of Message Types

**Table 11: Summary of all 18 Message Types in Protocol v2.1**

| Message Type | Sender | Receiver | Purpose |
| :--- | :--- | :--- | :--- |
| REFEREE_REGISTER_REQUEST | Referee | League | Referee Registration |
| REFEREE_REGISTER_RESPONSE | League | Referee | Referee Confirmation |
| LEAGUE_REGISTER_REQUEST | Player | League | Player Registration |
| LEAGUE_REGISTER_RESPONSE | League | Player | Registration Confirmation |
| ROUND_ANNOUNCEMENT | League | Players | Round Publication |
| ROUND_COMPLETED | League | Players | Round End |
| LEAGUE_COMPLETED | League | Everyone | League End |
| GAME_INVITATION | Referee | Player | Match Invitation |
| GAME_JOIN_ACK | Player | Referee | Arrival Confirmation |
| CHOOSE_PARITY_CALL | Referee | Player | Choice Request |
| CHOOSE_PARITY_RESPONSE | Player | Referee | Choice Response |
| GAME_OVER | Referee | Players | Match End |
| MATCH_RESULT_REPORT | Referee | League | Result Report |
| LEAGUE_STANDINGS_UPDATE | League | Players | Standings Update |
| LEAGUE_ERROR | League | Agent | League Error |
| GAME_ERROR | Referee | Player | Match Error |
| LEAGUE_QUERY | Player/Referee | League | Information Query |
| LEAGUE_QUERY_RESPONSE | League | Player/Referee | Query Response |

## 4.12 Important Rules

### 4.12.1 Mandatory Fields
Every message must include:
- `message_type` – Always.
- `match_id` – In game messages.
- `player_id` – In player messages.

### 4.12.2 Allowed Values
- `parity_choice`: Only "even" or "odd" (lowercase letters).
- `status`: Only "WIN", "DRAW", "TECHNICAL_LOSS".
- `accept`: Only `true` or `false` (Boolean).

### 4.12.3 Time Format
All time stamps in format ISO-8601:
`YYYY-MM-DDTHH:MM:SSZ`

Example: `2025-01-15T10:30:00Z`

---

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
                json= {
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
            league_id=result["league_id"])
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

---

# 6 Homework Requirements

## 6.1 Goal of the Exercise
In this exercise you will implement an AI agent for the Even/Odd league. At this stage, your agent will run only in your local environment. It is recommended to coordinate with other students to verify protocol compatibility.

**Very Important:** Use the protocol defined in this document exactly. Otherwise your agent will not be able to communicate with others.

It is mandatory to build and program the project subject to the guidelines of Chapter 9 (Protocol data of the league), Chapter 10 (Tools kit in Python), and Chapter 11 (Project structure). Also verify that the project runs and functions as defined in Chapter 8 (Running the league system).
This exercise is based on the book:

**AI Agents with Model Context Protocol**
By Dr. Yoram Segal
December 9, 2025

Therefore it is highly recommended to read and learn the subject in depth.

## 6.2 Mandatory Tasks

### 6.2.1 Task 1: Player Agent Implementation
Implement an MCP server listening on a port on localhost. The server must support the following tools:
1. `handle_game_invitation` – Receiving invitation to a match and returning `GAME_JOIN_ACK`.
2. `choose_parity` – Choosing "even" or "odd" and returning `CHOOSE_PARITY_RESPONSE`.
3. `notify_match_result` – Receiving match result and updating internal state.

### 6.2.2 Task 2: Registration to League
The agent must send a registration request to the League Manager. The request will include:
- Unique display name (Your name or nickname).
- Agent version.
- Endpoint address of the server.

### 6.2.3 Task 3: Self Check
Before submission, check your agent:
1. Run a local league with 4 players.
2. Verify that the agent responds to every message type.
3. Verify that the JSON structures match the protocol.

## 6.3 Technical Requirements

### 6.3.1 Programming Language
You can choose any language you want. The main thing is that the agent:
- Implements an HTTP server.
- Responds to POST requests at path `/mcp`.
- Returns JSON in format JSON-RPC 2.0.

### 6.3.2 Response Times
- `GAME_JOIN_ACK` – Within 5 seconds.
- `CHOOSE_PARITY_RESPONSE` – Within 30 seconds.
- Every other response – Within 10 seconds.

### 6.3.3 Stability
The agent must:
- Operate without crashes.
- Handle exceptions (Exception Handling).
- Not stop operating in the middle of a league.

## 6.4 Work Process

### 6.4.1 Step 1: Local Development
1. Implement the agent.
2. Check locally with your code.
3. Fix bugs.

### 6.4.2 Step 2: Private League
1. Run a local league with 4 copies of the agent.
2. Check that all communication works.
3. Improve the strategy (optional).

### 6.4.3 Step 3: Compatibility Check with Other Students
1. Coordinate with another student to exchange agents.
2. Check that the agents communicate properly.
3. Verify that the JSON structures match the protocol.

### 6.4.4 Look to the Future: Class League
In the future, it is possible that there will be:
- Creation of new games (not only Even/Odd).
- Competition in the class as part of the summary project.
This topic has not been closed yet and changes are possible. You have to adapt the agent in a way that will allow expansion in the future.

## 6.5 Submission

### 6.5.1 Submission Files
1. Source code of the agent.
2. `README` file with running instructions.
3. Detailed report including:
   - Full description of the architecture and implementation.
   - Description of the strategy chosen and reasons for choice.
   - Difficulties encountered and solutions found.
   - Documentation of the development and testing process.
   - Conclusions from the exercise and recommendations for improvement.

### 6.5.2 Submission Format
There is to submit a link to a public repository. And there is to submit manually the report as requested above to the exercises checker.

## 6.6 General Highlights regarding Testing the Work
Updated to requirements The following next criteria will be checked:

**Table 13: Criteria for Testing**

| Description | Criteria |
| :--- | :--- |
| Basic functioning | The agent works, answers messages, plays in games |
| Protocol compatibility | JSON structures match exactly the protocol |
| Stability | The agent is stable, does not crash, handles errors |
| Code quality | Clean code, documented, organized |
| Documentation | Clear running instructions, detailed description |
| Strategy | Interesting strategy implementation (not only random) |

## 6.7 Common Questions

### 6.7.1 Is it possible to use external libraries?
Yes. You can use any library you want. Verify that you supply appropriate installation instructions.

### 6.7.2 Is it mandatory to use Python?
No. Use any language that suits you. The main thing is that the agent adheres to the protocol requirements.

### 6.7.3 What happens if the agent of the course?
The agent will suffer a technical loss in the current game. If it does not return to operation – it will leave the league.

### 6.7.4 Is it possible to update the agent after submission?
No. The final submission. Check well before submitting.

### 6.7.5 How do I know what is my rating?
Ranking table will be published after every round. You will be able to see your location relative to others.

## 6.8 Summary
1. Implement a player agent that adheres to the protocol.
2. Check locally before submission.
3. Submit the code and the report.
4. Your agent will play in the class league.

**Good Luck!**

**Additional Information:**
For questions and clarifications turn to Dr. Yoram Segal.
Recommended to read the book "AI Agents with MCP" [1].
For additional details on the MCP protocol see the official documentation [2].

---

# 7 Learning through the League Exercise
The Even/Odd league exercise is not only a programming exercise. It constitutes a pedagogical model for understanding the MCP protocol and AI agent principles. In this chapter we will explain how the exercise teaches the foundations of AI agents and the MCP protocol.

## 7.1 The Player as an AI Agent

### 7.1.1 Is the player an AI agent?
The first question to ask is: Is the player agent (Player Agent) in the league really an AI agent? The answer is unequivocally: Yes.

An AI agent is defined as an entity that maintains interaction with the environment in order to achieve defined goals [1]. Unlike a regular computer program executing predetermined instructions, an AI agent is autonomous software that receives information from the environment, processes it, and decides by itself what to perform based on the current situation.

### 7.1.2 The Four Characteristics of an AI Agent
We will examine the player in the league in light of the four main characteristics of an AI agent:
1. **Autonomy** – The agent operates independently. In the context of the game, the player decides absolutely autonomously which strategy to choose: "even" or "odd". No one dictates to it what to choose.
2. **Perception** – The agent receives information from the environment. The player receives game invitations (`GAME_INVITATION`), requests for choice (`CHOOSE_PARITY_CALL`), and game results (`GAME_OVER`) from the referee and the League Manager.
3. **Action** – The agent influences the environment. The player performs actions by sending choices (`CHOOSE_PARITY_RESPONSE`) and arrival confirmations (`GAME_JOIN_ACK`) to the games.
4. **Goal-oriented** – It has a defined goal. Its goal is to play, to win games and to update its internal state, such as history of victories and defeats.

The player can also use a large language model (LLM) to choose the best strategy. In this way it demonstrates "thinking" or "drawing conclusions" before executing the action.

## 7.2 The Player in MCP Architecture

### 7.2.1 Service or Client?
In the Even/Odd league architecture, the player is primarily an **MCP Server**.

An MCP server is a component that exposes capabilities and services, called "Tools", "Resources" or "Prompts". The server is defined as a separate process on a defined port and provides a "gateway" to the outside world [2].

Therefore the player is required to implement an HTTP server that accepts POST requests at the path `/mcp`. The rules that expose capabilities via the JSON-RPC 2.0 protocol. The tools that the player is obliged to implement include:
- `handle_game_invitation` – Handling a game invitation.
- `choose_parity` – Choosing "even" or "odd".
- `notify_match_result` – Receiving a notification on the game result.

### 7.2.2 Relationships against the Referee and the League Manager
Given that the player is a server, who calls its services is the Client. In the league system, the Referee and the League Manager are the Actuators or Orchestrators.

The referee is the one creating the JSON-RPC request calling the tool `choose_parity` of the player. When the referee wants to collect choices from the players, it sends a request `CHOOSE_PARITY_CALL` to each player.

**Summary:** Although usually the player is an AI agent autonomously, in terms of MCP implementation, it fulfills the role of the server providing capabilities to the orchestrators.

## 7.3 The Referee and League Manager as AI Agents

### 7.3.1 Agents of High Degree
Also the referee and the League Manager are defined as AI agents. They stand at the same level as four characteristics:
These agents are not passive. They manage the entire system in accordance with general rules and defined goals. This is the essence of autonomy and purposefulness of an AI agent.

### 7.3.2 MCP Servers acting also as Clients
These two agents are defined as MCP Servers:
- The League Manager operates as an MCP server on port 8000. It implements tools like `register_player`, `register_referee`, and `report_match_result`.
- The Referee operates as an MCP server on port 8001. It implements tools like `start_match` and `collect_choices`.

**Important Note:** The referee and the League Manager, although they are defined as servers, are required to act also as MCP Clients to fulfill their central roles. For example:

**Table 14: Characteristics of an AI Agent for Referee and League Manager**

| Characteristic | League Manager | Referee |
| :--- | :--- | :--- |
| **Purposefulness** | Management of the entire league, registration of referees and players, schedule, calculation of ranking | Registration to the League Manager, management of a single match, verification of legality of moves, declaration of winner |
| **Autonomy** | Operates independently for registration of referees and fixing the schedule | Operates independently for management of stages of the game |
| **Perception** | Receives registration requests, reports of results from referees | Receives arrival confirmations, choices (Even/Odd) from the players |
| **Action** | Approves registration requests, sends invitations, sends round broadcast, updates standings table | Sends request for match invitation, sends request for choice, sends declaration of results |

- The referee must act as a client to register to the League Manager (`REFEREE_REGISTER_REQUEST`).
- The referee must act as a client to call the tool `choose_parity` of the player agent.
- The League Manager must act as a client to send the round announcement to the player agents.

In this system, the central servers are practically Orchestrator-Clients when they need to move the action at the players' servers.

## 7.4 Reversal of Roles: Central Insight

### 7.4.1 The Traditional Paradigm
In a traditional client-server architecture, the client is the active component that sends a request, and the server is the passive component waiting for a request. In the AI league, the roles are reversed creatively.

### 7.4.2 Function Reversal in the League
**The Player (The Autonomous Agent) is the Server:** Although the player is the autonomous entity needing to perform an action, it is required to expose its capabilities as an MCP Server.

**The Referee and the League Manager (The Orchestrators) are the Clients:** The referee is the Orchestrator acting as an MCP Client calling the tool `choose_parity` of the player in order to get it to move in the game.

*(Diagram reference: Player 1 (MCP Server :8101) <- (choose_parity) - Referee (Orchestrator, Acts as MCP Client :8001) - (choose_parity) -> Player 2 (MCP Server :8102). Referee <- (ROUND_ANNOUNCEMENT) - League Manager (Acts as MCP Client :8000))*

## 7.5 Principle of Separation of Layers

### 7.5.1 Three Separate Layers
The MCP protocol enables clear separation between the roles:
1. **League Layer** (Managed by the League Manager) – Recruitment of players, game schedule (Round-Robin), and standings table.
2. **Refereeing Layer** (Managed by the Referee) – Management of a single match and verification of moves.
3. **Game Rules Layer** (Managed by a separate module) – Specific logic for Even/Odd.

### 7.5.2 Benefit of Separation
The player, in that it exposes a standard MCP interface (JSON-RPC 2.0 over HTTP), enables the league to remain agnostic to the development language or the internal strategy.
This is a solution to the fragmentation problem where every agent and every model demanded in the past a unique integration. The MCP protocol solves this by creating a universal interface [2].
When the player receives a request like `CHOOSE_PARITY_CALL`, the data arrives in a fixed JSON structure. The player responds with `CHOOSE_PARITY_RESPONSE`, also in a fixed structure. This ensures that every agent, regardless of the way it calculates the data, can communicate efficiently with every orchestrator respecting the protocol.

## 7.6 The Role of the LLM in the Agent

### 7.6.1 The Dilemma
An interesting question arises: On one hand, the player is defined as an MCP server that exposes capabilities. On the other hand, it is described as an autonomous AI agent that can use an LLM as a "brain" to choose a strategy. By traditional definition, a server is not an "operator" of a "brain" but fills a request.

### 7.6.2 The Solution: Separation of Roles
The solution lies in understanding that the MCP function (Client/Server) and the AI components (Brain/Tools) are separate but complementary concepts.

**The Agent is also a Server and also a Client (Effectively):** Every one of the agents acts in practice also as a server and also as a client. The role of the server is required for every agent so that the host can enable communication to others to call it. The role of the client is required for every agent needing to initiate interaction.

**The LLM as an Internal Component:** A large language model is the "Brain" of the AI agent. If the player implements an MCP server, the LLM is simply an internal component within the general agent.
When the server receives a request `choose_parity`:
1. The MCP layer (The Server) receives the request.
2. The internal logic of the agent (The LLM or another strategy) operates to determine the choice.
3. The MCP layer (The Server) sends the response back.

The LLM is the "Intelligence" of the server, and it is not a server-client model. The central idea in MCP is to ensure that even when the "Brain" is found within the server, external communication will remain standard via JSON-RPC.

### 7.6.3 Analogy: Customer Service Station
It is possible to imagine the architecture as a customer service station:
- **MCP (Protocol)** – is the telephone and the language in which people speak (JSON-RPC over HTTP).
- **The Player (Server)** – is the service office with a telephone line of its own.
- **The Strategy/LLM (The Brain)** – is the smart consultant sitting inside the office, who receives the call, calculates the answer, and dictates to the clerk what to write back in the MCP layer response to send.

The internal tools (The LLM and the logic) are not exposed directly to the MCP protocol, but serve the public tools that the agent exposes, such as `choose_parity`.

## 7.7 Role of the Orchestrator

### 7.7.1 League Manager – The Architect
The League Manager is an agent at the highest level in terms of strategy, the manager of the league layer. It is not involved in the rules of the game itself, but in the general management: The schedule and the standings table.

**Benefit of Separation:** If the league wants to replace the game from Even/Odd to Tic-Tac-Toe, the League Manager almost does not change. This is a perfect example of the principle of Separation of Concerns promoted by MCP.

### 7.7.2 The Referee – The Internal Implementer
The referee embodies the refereeing layer. It does not know the general rules of the game (handled separately), but acts as responsible for managing the conversation (Conversation Lifecycle) between the players.
The referee verifies that the players meet the deadlines (Deadlines). It is the one activating the loop of the external agent for the players – it calls `choose_parity` so that they perform the autonomous action of the player.
**MCP allows splitting the clear roles:** The referee manages and the League Manager is responsible for the "id" (The communication protocol), while the players are responsible for the "what" (The strategy and the content).

## 7.8 What does the Exercise Teach

### 7.8.1 Basic Principles of AI Agents
The exercise teaches the four characteristics of an AI agent in a practical way:
- **Autonomy** – The player decides by itself.
- **Perception** – The player receives notifications from the system.
- **Action** – The player sends responses.
- **Goal-oriented** – The player strives to win.

### 7.8.2 Basic Principles of MCP
The exercise teaches the core principles of the MCP protocol:
1. **Standard Interface** – Every agent exposes tools via JSON-RPC 2.0.
2. **Separation of Roles** – League layer, refereeing layer, and game rules layer.
3. **Language Agnosticism** – Possible to implement an agent in any programming language.
4. **Communication via Orchestrator** – Agents do not talk directly, but via the referee or the League Manager.
5. **Registration of Agents** – Referees and players register to the League Manager before the start of the games.

### 7.8.3 The Learning Experience
At the end of the exercise, the student will understand:
- How an AI agent communicates with other agents.
- How to build a simple MCP server.
- What is the meaning of "Tools" in the MCP protocol.
- How an orchestrator manages interaction between agents.
- Why separation of layers is important for designing AI systems.

## 7.9 Summary
The Even/Odd league exercise constitutes a pedagogical model integrated for understanding the MCP protocol and AI agents. The simple game allows focusing on the architectural principles without getting complicated with complex logic.

The student learns that an AI agent can be also an MCP server – reversal of roles creates the possibility for the orchestrator to call the agents and activate their actions. The separation of layers ensures that it will be possible to replace the game in the future without changing the general protocol.

For additional details on the MCP protocol, see the book "AI Agents with MCP" [1] and the official documentation of Anthropic [2].

---

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

---

# 9 League Data Protocol

## 9.1 Introduction: The Genetic Code of Agent Society
When we build a society of autonomous agents – players, referees and league managers – we are actually creating a new digital culture. Like in every human society, here too three foundations are required:
1. **Shared Rules** – The protocol we defined in previous chapters.
2. **Collective Memory** – The ability to keep and restore historical information.
3. **Genetic Code** – The configuration that defines the DNA of every agent.

This appendix describes the "Database on JSON files" – a three-layer architecture allowing the system to grow to a scale of thousands of agents and leagues.

## 9.2 Three Layers Architecture

*(Diagram reference: Static Settings (Config Layer: config/), Dynamic State and History (Run Data Layer: data/), Tracking and Debugging (Logs Layer: logs/))* 

### 9.2.1 Guiding Principles
Every file in the system stands by the following principles:
- **Unique Identifier (id):** Every main object receives a single-value identifier.
- **Schema Version (schema_version):** Allows future migrations.
- **Time Stamp (last_updated):** In format UTC/ISO-8601.
- **Protocol Compatibility:** All fields match `league.v2`.

## 9.3 Configuration Layer – `config/`
This layer contains the "Genetic Code" of the system – static settings read at startup.

### 9.3.1 Global System File – `config/system.json`
- **Goal:** Global parameters for the entire system.
- **Users:** All agents, Orchestrator.
- **Location:** `SHARED/config/system.json`

This file defines the default values for:
- Network settings (network) – Ports and addresses.
- Security settings (security) – Tokens and TTL.
- Wait times (timeouts) – Matching the protocol definitions in Chapter 2.
- Retry policy (retry_policy) – Matching the protocol definitions.

**Example: Structure of `system.json` (Segment)**
```json
{
  "schema_version": "1.0.0",
  "system_id": "league_system_prod",
  "protocol_version": "league.v2",
  "timeouts": {
    "move_timeout_sec": 30,
    "generic_response_timeout_sec": 10
  },
  "retry_policy": {
    "max_retries": 3,
    "backoff_strategy": "exponential"
  }
}
```

### 9.3.2 Agents Registration – `config/agents/agents_config.json`
- **Goal:** Central management of thousands of agents.
- **Users:** League Manager, Deployment tool.
- **Location:** `SHARED/config/agents/agents_config.json`

This file contains the "Phone Book" of the agent society:
- `league_manager` – Details of League Manager.
- `referees[]` – List of all registered referees.
- `players[]` – List of all registered players.

### 9.3.3 League Configuration – `config/leagues/<league_id>.json`
- **Goal:** Specific settings for the league.
- **Users:** League Manager, Referees.
- **Location:** `SHARED/config/leagues/league_2025_even_odd.json`

Every league is an independent "State" with rules of its own:

**Example: League Configuration (Segment)**
```json
{
  "league_id": "league_2025_even_odd",
  "game_type": "even_odd",
  "status": "ACTIVE",
  "scoring": {
    "win_points": 3,
    "draw_points": 1,
    "loss_points": 0
  },
  "participants": {
    "min_players": 2,
    "max_players": 10000
  }
}
```

### 9.3.4 Registration of Game Types – `config/games/games_registry.json`
- **Goal:** Registration of all supported game types.
- **Users:** Referees (To load rules module), League Manager.
- **Location:** `SHARED/config/games/games_registry.json`

The system supports multiple game types. Every game defines:
- `game_type` – Unique identifier.
- `rules_module` – Rules module to load.
- `max_round_time_sec` – Maximum time for a round.

### 9.3.5 Defaults for Agents – `config/defaults/`
- **Goal:** Default values by agent type.
- **Files:** `player.json`, `referee.json`
- **Location:** `SHARED/config/defaults/`

These files allow a new agent to start operating with reasonable settings without defining everything separately.

## 9.4 Run Data Layer – `data/`
If the configuration layer is the "Genetic Code", the run data layer is the "Historical Memory" of the society. Here the events happening in the system are saved.

### 9.4.1 Standings Table – `data/leagues/<league_id>/standings.json`
- **Goal:** Current ranking state of the league.
- **Updater:** League Manager (After `MATCH_RESULT_REPORT`).
- **Location:** `SHARED/data/leagues/league_2025_even_odd/standings.json`

**Example: Standings Table Structure**
```json
{
  "schema_version": "1.0.0",
  "league_id": "league_2025_even_odd",
  "version": 12,
  "rounds_completed": 3,
  "standings": [
    {
      "rank": 1,
      "player_id": "P01",
      "display_name": "Agent Alpha",
      "wins": 4, "draws": 1, "losses": 1,
      "points": 13
    }
  ]
}
```

### 9.4.2 Rounds History – `data/leagues/<league_id>/rounds.json`
- **Goal:** Documentation of all rounds that took place.
- **Updater:** League Manager (After `ROUND_COMPLETED`).
- **Location:** `SHARED/data/leagues/league_2025_even_odd/rounds.json`

### 9.4.3 Single Match Data – `data/matches/<league_id>/<match_id>.json`
- **Goal:** Full documentation of a single match.
- **Updater:** The referee managing the match.
- **Location:** `SHARED/data/matches/league_2025_even_odd/R1M1.json`

This file is the "Identity Card" of the match and contains:
- `lifecycle` – Match state and times.
- `transcript[]` – All messages exchanged (History of moves).
- `result` – Final result (Matches `GAME_OVER`).

### 9.4.4 Player History – `data/players/<player_id>/history.json`
- **Goal:** "Personal Memory" of the player.
- **User:** The player itself (To build strategy).
- **Location:** `SHARED/data/players/P01/history.json`

A smart player can use this file as "Memory" to improve its strategy:

**Example: Player History**
```json
{
  "player_id": "P01",
  "stats": {
    "total_matches": 20,
    "wins": 12, "losses": 5, "draws": 3
  },
  "matches": [
    {
      "match_id": "R1M1",
      "opponent_id": "P02",
      "result": "WIN",
      "my_choice": "even",
      "opponent_choice": "odd"
    }
  ]
}
```

## 9.5 Logs Layer – `logs/`
This layer is the "Nervous System" of the society – it allows us to see what really happened in the distributed system.

### 9.5.1 Central League Log – `logs/league/<league_id>/league.log.jsonl`
- **Format:** JSON Lines (Every line is a separate JSON object).
- **Users:** DevOps, Technical Support.
- **Location:** `SHARED/logs/league/league_2025_even_odd/league.log.jsonl`

**Example: League Log List**
```json
{
  "timestamp": "2025-01-15T10:15:00Z",
  "component": "league_manager",
  "event_type": "ROUND_ANNOUNCEMENT_SENT",
  "level": "INFO",
  "details": {"round_id": 1, "matches_count": 2}
}
```

### 9.5.2 Agent Log – `logs/agents/<agent_id>.log.jsonl`
- **Goal:** Tracking per-agent for debugging.
- **Users:** Agent developers.
- **Location:** `SHARED/logs/agents/P01.log.jsonl`

Every agent documents the messages it sends and receives, which enables End-to-End Trace of all interaction in the system.

## 9.6 Files Summary Table

**Table 18: Summary of Configuration and Data Files**

| Layer | Path | Purpose | User |
| :--- | :--- | :--- | :--- |
| Config | `config/system.json` | Global parameters | All agents |
| Config | `config/agents/` | Registration of agents | League Manager |
| Config | `config/leagues/` | League settings | League Manager |
| Config | `config/games/` | Registration of games | Referees |
| Config | `config/defaults/` | Defaults | Agents |
| Run Data | `data/.../standings.json` | Standings table | Everyone |
| Run Data | `data/.../rounds.json` | Rounds history | League Manager |
| Run Data | `data/matches/` | Match details | Analytics |
| Run Data | `data/players/` | Personal history | Player |
| Logs | `logs/league/` | Central log | DevOps |
| Logs | `logs/agents/` | Agent log | Developers |

## 9.7 Usage of Shared Files
All example files described in the appendix are available in the shared folder:
`L07/SHARED/`

Students are invited to use these files as a base for their agent implementation. The files include:
- Full examples for every file type.
- Data matching the protocol `league.v2`.
- Folder structure recommended for the project.

## 9.8 Summary
The architecture of the three layers we presented – Configuration, Run Data, and Logs – provides the required infrastructure for building a large scale agent system.
Like in human society, here too:
- **Configuration is the "Constitution"** – The basic rules that everyone knows.
- **Run Data is the "Historical Archive"** – The collective memory.
- **Logs are the "Journalism"** – Documentation of what happened in real time.

This structure prepares the system for growth to thousands of agents and leagues, while keeping order, consistency, and tracking capability.

---

# 10 Python Toolkit

## 10.1 Introduction: From Configuration to Code
In Appendix B we presented the data architecture based on JSON files – three layers of configuration, run data, and logs. But how does a single agent access this data in practice?
This appendix presents `league_sdk` – a Python library that bridges between JSON files and the objects the agents use. The library implements two central design patterns:
1. **Dataclasses** – Typed models reflecting the JSON structure.
2. **Repository Pattern** – Abstraction layer for data access.

## 10.2 Library Structure

*(Diagram reference: league_sdk/ -> `__init__.py` (Entry point), `config_models.py` (Data classes), `config_loader.py` (Configuration loading), `repositories.py` (Run data management), `logger.py` (Log registration))*

## 10.3 Typed Models – `config_models.py`

### 10.3.1 Approach: Dataclasses
Python 3.7+ provides the `@dataclass` decorator allowing class definition of data in a concise way. Every field in JSON becomes a field in the class with a defined type:

**Example: Dataclass Definition**
```python
from dataclasses import dataclass
from typing import List

@dataclass
class NetworkConfig:
    base_host: str
    default_league_manager_port: int
    default_referee_port_range: List[int]
    default_player_port_range: List[int]
```

### 10.3.2 System Configuration Models
The file defines all the models matching `config/system.json`:

**Global Configuration Models**
```python
@dataclass
class SecurityConfig:
    enable_auth_tokens: bool
    token_length: int
    token_ttl_hours: int

@dataclass
class TimeoutsConfig:
    register_referee_timeout_sec: int
    register_player_timeout_sec: int
    game_join_ack_timeout_sec: int
    move_timeout_sec: int
    generic_response_timeout_sec: int

@dataclass
class SystemConfig:
    schema_version: str
    system_id: str
    protocol_version: str
    default_league_id: str
    network: NetworkConfig
    security: SecurityConfig
    timeouts: TimeoutsConfig
    # ...additional fields
```

### 10.3.3 Agent Models
Every agent type receives a configuration class of its own:

**Agent Configuration Models**
```python
@dataclass
class RefereeConfig:
    referee_id: str
    display_name: str
    endpoint: str
    version: str
    game_types: List[str]
    max_concurrent_matches: int
    active: bool = True

@dataclass
class PlayerConfig:
    player_id: str
    display_name: str
    version: str
    preferred_leagues: List[str]
    game_types: List[str]
    default_endpoint: str
    active: bool = True
```

### 10.3.4 League Models
Specific definitions for the league including scheduling, scoring, and participants:

**League Configuration Models**
```python
@dataclass
class ScoringConfig:
    win_points: int
    draw_points: int
    loss_points: int
    technical_loss_points: int
    tiebreakers: List[str]

@dataclass
class LeagueConfig:
    schema_version: str
    league_id: str
    display_name: str
    game_type: str
    status: str
    scoring: ScoringConfig
    # ...additional fields
```

## 10.4 Configuration Loader – `ConfigLoader`

### 10.4.1 Principle: Lazy Loading with Caching
The `ConfigLoader` class implements the Lazy Loading pattern – configuration files are loaded only when needed, and kept in cache for repeat access:

**ConfigLoader Structure**
```python
class ConfigLoader:
    def __init__(self, root: Path = CONFIG_ROOT):
        self.root = root
        self.system = None       # lazy cache
        self.agents = None       # lazy cache
        self.leagues = {}        # league_id -> LeagueConfig

    def load_system(self) -> SystemConfig:
        """Load global system configuration."""
        if self.system:
            return self.system
        path = self.root / "system.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.system = SystemConfig(...)
        return self.system
```

### 10.4.2 Loading Methods
`ConfigLoader` provides a unified interface for loading all configuration types:

**Table 19: Methods of ConfigLoader**

| Method | Return Type | Description |
| :--- | :--- | :--- |
| `load_system()` | `SystemConfig` | Global configuration |
| `load_agents()` | `AgentsConfig` | List of all agents |
| `load_league(id)` | `LeagueConfig` | Specific league configuration |
| `load_games_registry()` | `GamesRegistry` | Registration of game types |

### 10.4.3 Helper Methods
In addition to direct loading, the class provides convenient methods for searching:

**Helper Methods**
```python
def get_referee_by_id(self, referee_id: str) -> RefereeConfig:
    """Get referee configuration by ID."""
    agents = self.load_agents()
    for ref in agents.referees:
        if ref.referee_id == referee_id:
            return ref
    raise ValueError(f"Referee not found: {referee_id}")

def get_player_by_id(self, player_id: str) -> PlayerConfig:
    """Get player configuration by ID."""
    agents = self.load_agents()
    for player in agents.players:
        if player.player_id == player_id:
            return player
    raise ValueError(f"Player not found: {player_id}")
```

## 10.5 Repositories – Data Stores

### 10.5.1 Repository Pattern
While `ConfigLoader` handles static configuration, the Repository layer handles dynamic data. Every repository is responsible for reading, updating, and saving a specific data type.

### 10.5.2 Standings Table Repository

**Standings Table Repository**
```python
class StandingsRepository:
    def __init__(self, league_id: str, data_root: Path = DATA_ROOT):
        self.league_id = league_id
        self.path = data_root / "leagues" / league_id / "standings.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict:
        """Load standings from JSON file."""
        if not self.path.exists():
            return {"schema_version": "1.0.0", "standings": []}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, standings: Dict) -> None:
        """Save standings to JSON file."""
        standings["last_updated"] = datetime.utcnow().isoformat() + "Z"
        self.path.write_text(json.dumps(standings, indent=2))

    def update_player(self, player_id: str, result: str, points: int):
        """Update a player's standings after a match."""
        standings = self.load()
        # ... update logic
        self.save(standings)
```

### 10.5.3 Additional Repositories
The library includes additional repositories for run data management:

**Table 20: Available Data Repositories**

| Repository | File |
| :--- | :--- |
| `StandingsRepository` | `standings.json` |
| `RoundsRepository` | `rounds.json` |
| `MatchRepository` | `<match_id>.json` |
| `PlayerHistoryRepository` | `history.json` |

## 10.6 Log Registration – `JsonLogger`

### 10.6.1 JSON Lines Format
The library uses the format JSONL (JSON Lines) – every line in the log file is a JSON object by itself. This format allows:
- Adding new records efficiently (append-only).
- Reading and analysis via standard tools.
- Streaming of logs in real time.

### 10.6.2 Logger Class

**JsonLogger Class**
```python
class JsonLogger:
    def __init__(self, component: str, league_id: str | None = None):
        self.component = component
        # Determine log directory
        if league_id:
            subdir = LOG_ROOT / "league" / league_id
        else:
            subdir = LOG_ROOT / "system"
        subdir.mkdir(parents=True, exist_ok=True)
        self.log_file = subdir / f"{component}.log.jsonl"

    def log(self, event_type: str, level: str = "INFO", **details):
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "component": self.component,
            "event_type": event_type,
            "level": level,
            **details,
        }
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
```

### 10.6.3 Convenience Methods
The logger provides convenience methods for log levels and common events:

**Logger Convenience Methods**
```python
def debug(self, event_type: str, **details):
    self.log(event_type, level="DEBUG", **details)

def info(self, event_type: str, **details):
    self.log(event_type, level="INFO", **details)

def warning(self, event_type: str, **details):
    self.log(event_type, level="WARNING", **details)

def error(self, event_type: str, **details):
    self.log(event_type, level="ERROR", **details)

def log_message_sent(self, message_type: str, recipient: str, **details):
    self.debug("MESSAGE_SENT", message_type=message_type,
               recipient=recipient, **details)
```

## 10.7 Usage in Agents

### 10.7.1 Example: League Manager

**Usage of ConfigLoader in League Manager**
```python
from league_sdk import ConfigLoader, JsonLogger

class LeagueManager:
    def __init__(self, league_id: str):
        loader = ConfigLoader()
        self.system_cfg = loader.load_system()
        self.agents_cfg = loader.load_agents()
        self.league_cfg = loader.load_league(league_id)

        self.logger = JsonLogger("league_manager", league_id)

        # Build lookup maps
        self.referees_by_id = {
            r.referee_id: r.endpoint
            for r in self.agents_cfg.referees if r.active
        }

    def get_timeout_for_move(self) -> int:
        return self.system_cfg.timeouts.move_timeout_sec
```

### 10.7.2 Example: Referee Agent

**Usage of ConfigLoader in Referee**
```python
from league_sdk import ConfigLoader, JsonLogger

class RefereeAgent:
    def __init__(self, referee_id: str, league_id: str):
        loader = ConfigLoader()
        self.system_cfg = loader.load_system()
        self.league_cfg = loader.load_league(league_id)
        self.self_cfg = loader.get_referee_by_id(referee_id)

        self.logger = JsonLogger(f"referee:{referee_id}", league_id)

    def register_to_league(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "register_referee",
            "params": {
                "protocol": self.system_cfg.protocol_version,
                "message_type": "REFEREE_REGISTER_REQUEST",
                "referee_meta": {
                    "display_name": self.self_cfg.display_name,
                    "version": self.self_cfg.version,
                    "game_types": self.self_cfg.game_types,
                }
            }
        }
        # ... send request
```

### 10.7.3 Example: Error Logging

**TIMEOUT Error Logging**
```python
logger = JsonLogger("referee:REF01", "league_2025_even_odd")

logger.error(
    "GAME_ERROR",
    match_id="R1M1",
    error_code="TIMEOUT_MOVE",
    player_id="P02",
    timeout_sec=30,
)
# Output to logs/league/league_2025_even_odd/referee_REF01.log.jsonl:
# {"timestamp":"2025-01-15T10:15:00Z","component":"referee:REF01",
#  "event_type":"GAME_ERROR","level":"ERROR","match_id":"R1M1",...}
```

## 10.8 Summary
The library `league_sdk` provides a clean abstraction layer between the JSON files and the agent code:
- `config_models.py` – Defines safe types (type-safe) for every data structure.
- `config_loader.py` – Provides convenient access to configuration with caching.
- `repositories.py` – Manages run data in Repository pattern.
- `logger.py` – Allows structured log registration in JSONL format.

Use of the library ensures:
1. **Consistency** – All agents use the same models and data.
2. **Maintainability** – Changes in data structure concentrate in one place.
3. **Typing Safety** – Catching typos at the time of writing the code.
4. **Debugging Capability** – Logs structured allowing easy tracking of every problem.

The library is available in the folder:
`L07/SHARED/league_sdk/`

---

# 11 Project Structure

## 11.1 Introduction: Road Map
After we got to know the protocol, the JSON messages, the data architecture, and the Python library – the time has come to see the full picture. This appendix presents the recommended directory structure for the league project, so that every student can start working on an organized and prepared base.

## 11.2 Main Directory Tree

*(Diagram reference: L07/ -> SHARED/ , agents/ , doc/)*

**Table 21: Project Base Directories**

| Directory | Description |
| :--- | :--- |
| `SHARED/` | Shared resources – Configuration, data, logs, and SDK library |
| `agents/` | Agents code – Every agent in a separate directory |
| `doc/` | Project documentation – Documents and specifications |

## 11.3 Shared Resources Directory – `SHARED/`
This directory contains all the resources shared by all agents in the system.

```text
SHARED/
├── config/                     # Configuration layer
│   ├── system.json             # Global system settings
│   ├── agents/
│   │   └── agents_config.json  # All agents registry
│   ├── leagues/
│   │   └── league_2025_even_odd.json
│   ├── games/
│   │   └── games_registry.json # Supported game types
│   └── defaults/
│       ├── referee.json        # Default referee settings
│       └── player.json         # Default player settings
│
├── data/                       # Runtime data layer
│   ├── leagues/
│   │   └── league_2025_even_odd/
│   │       ├── standings.json  # Current standings
│   │       └── rounds.json     # Round history
│   ├── matches/
│   │   └── league_2025_even_odd/
│   │       ├── R1M1.json       # Match R1M1 data
│   │       └── R1M2.json       # Match R1M2 data
│   └── players/
│       ├── P01/
│       │   └── history.json    # P01 match history
│       └── P02/
│           └── history.json    # P02 match history
│
├── logs/                       # Logging layer
│   ├── league/
│   │   └── league_2025_even_odd/
│   │       └── league.log.jsonl
│   ├── agents/
│   │   ├── REF01.log.jsonl
│   │   ├── P01.log.jsonl
│   │   └── P02.log.jsonl
│   └── system/
│       └── orchestrator.log.jsonl
│
└── league_sdk/
    ├── __init__.py
    ├── config_models.py        # Dataclass definitions
    ├── config_loader.py        # ConfigLoader class
    ├── repositories.py         # Data repositories
    └── logger.py               # JsonLogger class
```

## 11.4 Agents Directory – `agents/`
Every agent lives in a separate folder with a similar structure:

```text
agents/
├── league_manager/
│   ├── main.py                 # Entry point
│   ├── handlers.py             # Message handlers
│   ├── scheduler.py            # Round scheduling
│   └── requirements.txt
│
├── referee_REF01/
│   ├── main.py                 # Entry point
│   ├── game_logic.py           # Even/Odd rules
│   ├── handlers.py             # Message handlers
│   └── requirements.txt
│
├── player_P01/
│   ├── main.py                 # Entry point
│   ├── strategy.py             # Playing strategy
│   ├── handlers.py             # Message handlers
│   └── requirements.txt
│
└── player_P02/
    ├── main.py
    ├── strategy.py
    ├── handlers.py
    └── requirements.txt
```

### 11.4.1 Typical Agent Structure
Every agent contains the following files:

**Table 22: Typical Agent Files**

| File | Role |
| :--- | :--- |
| `main.py` | Entry point – Server initialization and configuration loading |
| `handlers.py` | Handling incoming notifications by type |
| `strategy.py` | Decision making logic (For players) |
| `game_logic.py` | Game rules (For referees) |
| `requirements.txt` | Python dependencies |

## 11.5 Documentation Directory – `doc/`

```text
doc/
├── protocol-spec.md            # Protocol specification
├── message-examples/
│   ├── registration/
│   │   ├── referee_register_request.json
│   │   └── player_register_request.json
│   ├── game-flow/
│   │   ├── game_start.json
│   │   ├── move_request.json
│   │   └── game_over.json
│   └── errors/
│       ├── timeout_error.json
│       └── invalid_move.json
└── diagrams/
    ├── architecture.png
    └── message-flow.png
```

## 11.6 Architecture Diagram
*(Diagram reference: League Manager <---> Referee REF01 / Player P01 / Player P02. All connected to Config reading, Data writing, Logs, Python SDK)*

## 11.7 Data Flow

### 11.7.1 Reading and Writing

**Table 23: Permissions Access to Files**

| File/Folder | Reader | Writer | Comments |
| :--- | :--- | :--- | :--- |
| `config/*` | System Manager | Everyone | Read only for agents |
| `standings.json` | League Manager | Everyone | Update after match |
| `rounds.json` | League Manager | Everyone | Rounds history |
| `matches/*.json` | Referee | Everyone | Single match file |
| `history.json` | The Player | The Player | Personal history |
| `logs/*` | All agents | DevOps | Log only |

## 11.8 Installation and Running

### 11.8.1 Prerequisites
- Python 3.10+
- `pip` or `poetry` for package management
- Access to folder `SHARED/`

### 11.8.2 Dependency Installation

```bash
# Install league_sdk
cd SHARED
pip install -e league_sdk/

# Install agent dependencies
cd ../agents/player_P01
pip install -r requirements.txt
```

### 11.8.3 Running an Agent

```bash
# Start League Manager
cd agents/league_manager
python main.py --league-id league_2025_even_odd

# Start Referee
cd agents/referee_REF01
python main.py --referee-id REF01 \
               --league-id league_2025_even_odd

# Start Player
cd agents/player_P01
python main.py --player-id P01 \
               --league-id league_2025_even_odd
```

## 11.9 Full Files List
Below is a full list of all files in the project:

```text
L07/
├── SHARED/
│   ├── config/
│   │   ├── system.json
│   │   ├── agents/agents_config.json
│   │   ├── leagues/league_2025_even_odd.json
│   │   ├── games/games_registry.json
│   │   └── defaults/{referee,player}.json
│   ├── data/
│   │   ├── leagues/<league_id>/{standings,rounds}.json
│   │   ├── matches/<league_id>/<match_id>.json
│   │   └── players/<player_id>/history.json
│   ├── logs/
│   │   ├── league/<league_id>/*.log.jsonl
│   │   ├── agents/*.log.jsonl
│   │   └── system/*.log.jsonl
│   └── league_sdk/
│       ├── __init__.py
│       ├── config_models.py
│       ├── config_loader.py
│       ├── repositories.py
│       └── logger.py
├── agents/
│   ├── league_manager/{main,handlers,scheduler}.py
│   ├── referee_REF01/{main,handlers,game_logic}.py
│   └── player_*/{main,handlers,strategy}.py
└── doc/
    ├── protocol-spec.md
    └── message-examples/**/*.json
```

## 11.10 Summary
This project structure provides:
1. **Clear Separation** – Every component in its folder.
2. **Shared Resources** – `SHARED/` concentrates all the data.
3. **Agent Independence** – Every agent can operate independently.
4. **Structured Documentation** – Examples and specifications in `doc/`.
5. **Extensibility** – Easy to add new agents and new leagues.

Full files are available in the folder:
`L07/SHARED/`

Recommended to duplicate the structure and start building the agents yours!

---

# 12 References

1. Y. Segal, *AI Agents with MCP*. Dr. Yoram Segal, 2025, Hebrew edition.
2. Anthropic, *Model context protocol specification*, 2024. [Online]. Available: https://modelcontextprotocol.io/
3. JSON-RPC Working Group, *Json-rpc 2.0 specification*, 2010. [Online]. Available: https://www.jsonrpc.org/specification
4. K. Stratis, *AI Agents with MCP*. O'Reilly Media, 2025, Early Release.
```