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
