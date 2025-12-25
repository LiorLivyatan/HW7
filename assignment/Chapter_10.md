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

| Repository | File | Role |
| :--- | :--- | :--- |
| `StandingsRepository` | `standings.json` | League standings table |
| `RoundsRepository` | `rounds.json` | Rounds history |
| `MatchRepository` | `<match_id>.json` | Single match data |
| `PlayerHistoryRepository` | `history.json` | Player history |

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

```