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
└── league_sdk/                 # Python SDK
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
├── message-examples/           # JSON message examples
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
