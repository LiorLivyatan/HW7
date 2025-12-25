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
