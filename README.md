# Even/Odd League Player Agent

**AI Player Agent for the Even/Odd League** using FastAPI, Agno framework, and Google Gemini.

**Status**: ✅ **Core Implementation Complete** (Phases 1-8 done)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in editable mode
pip install -e .

# Or install directly from requirements
pip install -r requirements.txt
```

### 2. Configure API Key

Get your **FREE** Google Gemini API key from: https://aistudio.google.com/apikey

Then add it to your `.env` file:

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your key
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Run the Player Agent

```bash
# Run with hybrid strategy (recommended - random with Gemini fallback)
python -m my_project.agents.player.main --port 8101 --strategy hybrid

# Or run with random strategy (fast and reliable)
python -m my_project.agents.player.main --port 8102 --strategy random

# Or run with LLM-only strategy (requires API key)
python -m my_project.agents.player.main --port 8103 --strategy llm --debug
```

### 4. Test the Server

Open another terminal:

```bash
# Health check
curl http://localhost:8101/health

# Get player stats
curl http://localhost:8101/stats

# Test MCP endpoint with choose_parity
curl -X POST http://localhost:8101/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "choose_parity",
    "params": {
      "conversation_id": "test-001",
      "match_id": "R1M1"
    },
    "id": 1
  }'
```

---

## 📁 Project Structure

```
HW7/
├── src/my_project/               # ✅ Main package (production-ready)
│   ├── agents/player/            # ✅ Player Agent implementation
│   │   ├── main.py               # ✅ Entry point & CLI
│   │   ├── server.py             # ✅ FastAPI MCP server
│   │   ├── handlers.py           # ✅ 3 MCP tools (invitation, parity, result)
│   │   ├── strategy.py           # ✅ Agno+Gemini strategy engine
│   │   └── state.py              # ✅ State management (stats, history)
│   ├── core/                     # ✅ Core protocol components
│   │   ├── protocol.py           # ✅ Message builders (league.v2)
│   │   ├── registration.py       # ✅ League Manager registration
│   │   └── validation.py         # 🔄 To be implemented
│   ├── utils/                    # ✅ Utilities
│   │   ├── timestamp.py          # ✅ UTC timestamp utilities
│   │   ├── logger.py             # ✅ Structured JSON logging
│   │   └── client.py             # 🔄 To be implemented
│   └── config/                   # ✅ Configuration
│       └── settings.py           # ✅ Config management
├── tests/                        # 🔄 To be implemented (Phase 9)
├── docs/                         # 🔄 To be completed (Phase 10)
├── config/                       # ✅ Configuration files
│   └── config.yaml               # ✅ Player settings
├── .env                          # ✅ Environment variables (with your API key)
├── .env.example                  # ✅ Example env file
├── pyproject.toml                # ✅ Package configuration
├── requirements.txt              # ✅ Dependencies
└── CLAUDE.md                     # ✅ Complete assignment guide (2195 lines)
```

---

## 🎯 Features Implemented (Phases 1-8 Complete!)

### ✅ Phase 1: Setup
- Package configuration (`pyproject.toml`, `requirements.txt`)
- Environment variables (`.env` with Gemini API key)
- Player configuration (`config/config.yaml`)

### ✅ Phase 2: Core Utilities
- **TimestampUtil**: UTC timestamp generation/validation (ISO-8601 with 'Z')
- **StructuredLogger**: JSON-formatted logging
- **ProtocolMessageBuilder**: league.v2 message construction

### ✅ Phase 3: State Management
- **PlayerState**: Game history, statistics (wins/draws/losses), auth token storage
- Match result processing
- Win rate calculation

### ✅ Phase 4: Strategy Engine (★ Innovation!)
- **Random Strategy**: Fast baseline
- **LLM Strategy**: Gemini-powered decisions with reasoning
- **Hybrid Strategy**: LLM with timeout fallback to random (RECOMMENDED)
- Agno framework integration
- Pydantic output schema for lowercase validation
- 25-second timeout with 5-second protocol buffer

### ✅ Phase 5: MCP Tool Handlers
- `handle_game_invitation`: Accepts invitations (≤5s timeout)
- `choose_parity`: Makes parity choice (≤30s timeout)
- `notify_match_result`: Updates state (≤10s timeout)

### ✅ Phase 6: FastAPI Server
- JSON-RPC 2.0 compliant MCP endpoint (`/mcp`)
- Health check (`/health`)
- Stats endpoint (`/stats`)
- Swagger UI documentation (`/docs`)
- Error handling with proper JSON-RPC error codes

### ✅ Phase 7: Registration Client
- Registers with League Manager
- Receives and stores auth_token
- Handles registration errors gracefully

### ✅ Phase 8: Configuration Management
- Loads from `config.yaml` and `.env`
- Environment variable overrides
- Centralized settings access

---

## 🔧 Configuration

### Environment Variables (`.env`)

```bash
# API Keys
GOOGLE_API_KEY=your_api_key_here

# Player Configuration
PLAYER_ID=P01
PLAYER_DISPLAY_NAME="Gemini Agent"
STRATEGY_MODE=hybrid  # random, llm, or hybrid

# League Configuration
LEAGUE_MANAGER_HOST=localhost
LEAGUE_MANAGER_PORT=8000
PLAYER_AGENT_PORT=8101

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### Strategy Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `random` | Fast random.choice(["even", "odd"]) | Baseline, testing, production |
| `llm` | Gemini-powered decisions with reasoning | Interesting AI showcase |
| `hybrid` | LLM with timeout fallback to random | **RECOMMENDED** - best of both worlds |

---

## 📊 8 Building Blocks (Chapter 15 Compliance)

1. **MCPProtocolHandler** (`server.py`) - FastAPI app, JSON-RPC 2.0 routing
2. **ToolHandlers** (`handlers.py`) - 3 MCP tools implementation
3. **PlayerState** (`state.py`) - State management
4. **ProtocolMessageBuilder** (`protocol.py`) - league.v2 messages
5. **StrategyEngine** (`strategy.py`) - Agno+Gemini decision-making
6. **RegistrationClient** (`registration.py`) - League Manager registration
7. **TimestampUtil** (`timestamp.py`) - UTC timestamp utilities
8. **StructuredLogger** (`logger.py`) - JSON logging

---

## 🧪 Testing (Phase 9 - Pending)

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest tests/ --cov=src/my_project --cov-report=html

# View coverage report
open htmlcov/index.html
```

---

## 📖 Documentation (Phase 10 - Pending)

### Pending Documentation Tasks:
- **PRD.md**: Product Requirements Document
- **ARCHITECTURE.md**: 8 building blocks with Input/Output/Setup
- **PROMPTS_BOOK.md**: All Gemini prompts with context
- **API_REFERENCE.md**: Complete API documentation

### Available Documentation:
- **CLAUDE.md**: Comprehensive implementation guide (2,195 lines)
- **agents_and_skills.md**: Claude Code agents configuration
- **Assignment chapters**: Full specification (Chapters 1-12)

---

## 🎮 Usage Examples

### Basic Usage

```python
from my_project import PlayerState, StrategyEngine, ToolHandlers, create_app

# Initialize components
state = PlayerState(player_id="P01", display_name="My Agent")
strategy = StrategyEngine(mode="hybrid")
handlers = ToolHandlers(state, strategy)

# Create FastAPI app
app = create_app(handlers)

# Run with uvicorn
import uvicorn
uvicorn.run(app, host="localhost", port=8101)
```

### Test Parity Choice

```python
import asyncio
from my_project import StrategyEngine

async def test_strategy():
    engine = StrategyEngine(mode="hybrid")
    context = {
        "opponent": "P02",
        "standings": {"P01": 3, "P02": 6},
        "history": []
    }
    choice = await engine.choose_parity(context)
    print(f"Choice: {choice}")  # Always lowercase "even" or "odd"

asyncio.run(test_strategy())
```

---

## 🚨 Critical Protocol Compliance

### ✅ MUST Follow:
- **Timestamps**: UTC with 'Z' suffix (`datetime.utcnow().isoformat() + "Z"`)
- **Parity Choice**: lowercase "even" or "odd" (NEVER "Even" or "ODD")
- **Auth Token**: Include in all messages after registration
- **Timeouts**: 5s (invitation), 30s (parity), 10s (result)
- **JSON Structure**: Exact match to Chapter 4 specifications

### ❌ Common Pitfalls (AVOIDED):
- ❌ Local timezone timestamps
- ❌ Capitalized parity choices
- ❌ Missing auth_token
- ❌ Timeout violations

---

## 🎯 Next Steps (Phases 9-11)

### Phase 9: Testing (Pending)
- Unit tests for all 8 building blocks
- Integration tests for HTTP server
- Protocol compliance tests
- **Target**: 70%+ code coverage

### Phase 10: Documentation (Pending)
- Complete PRD.md
- Complete ARCHITECTURE.md with building blocks
- Create PROMPTS_BOOK.md
- Generate API_REFERENCE.md

### Phase 11: Research & Analysis (Pending)
- Parameter exploration (random vs LLM strategies)
- Analysis notebook with visualizations
- Win rate comparison
- Performance metrics

---

## 📞 Support

- **Issues**: Check CLAUDE.md for troubleshooting
- **API Key**: Get free Gemini key at https://aistudio.google.com/apikey
- **Assignment**: See `/assignment/` directory for full specification

---

## 📄 License

MIT License - see LICENSE file for details

---

**Built with ❤️ using FastAPI, Agno, and Google Gemini**
