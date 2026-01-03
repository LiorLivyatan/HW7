# 🎮 Even/Odd League Player Agent - Testing Guide

## What Is This Assignment?

You built an **AI Player Agent** for the Even/Odd League game:
- **The Game**: Two players simultaneously choose "even" or "odd", referee draws a number 1-10, matching parity wins
- **Your Agent**: Responds to game invitations, chooses parity (randomly or with AI), tracks stats
- **The System**: League Manager (registration), Referee (runs matches), Player Agents (you!)

---

## ✅ Quick Verification (1 minute)

### Start Your Player Agent
```bash
cd "/Users/liorlivyatan/Desktop/Livyatan/MSc CS/LLM Course/HW7"
python -m src.my_project.agents.player.main --port 8101 --strategy random
```

**What you should see:**
```
============================================================
🎮 Starting Even/Odd League Player Agent
============================================================
Player ID: P01
Display Name: Gemini Agent
Port: 8101
Strategy: random
Host: localhost

✅ Player Agent ready!

Server running at: http://localhost:8101
MCP Endpoint: http://localhost:8101/mcp
API Docs: http://localhost:8101/docs
Health Check: http://localhost:8101/health
Player Stats: http://localhost:8101/stats

Press CTRL+C to stop
```

### Test It (in another terminal)
```bash
# 1. Health check
curl http://localhost:8101/health
# Expected: {"status":"healthy"}

# 2. Check stats
curl http://localhost:8101/stats
# Expected: {"player_id":"P01", "wins":0, "total_matches":0, ...}

# 3. View API documentation
open http://localhost:8101/docs
# Opens interactive API docs in browser
```

---

## 🧪 Run All Tests (Proves Everything Works)

```bash
pytest tests/ -v
```

**Expected:**
```
115 passed in 2.0s
```

**What these tests verify:**
- ✅ Game invitations accepted within 5 seconds
- ✅ Parity choices always lowercase ("even" or "odd")
- ✅ Timestamps always UTC with 'Z' suffix
- ✅ Auth tokens properly managed
- ✅ Match results update stats correctly
- ✅ Protocol compliance (64% code coverage)

---

## 📊 Check Test Coverage

```bash
pytest tests/ --cov=src/my_project --cov-report=html
open htmlcov/index.html
```

**Current Coverage: 64%**
- protocol.py: 100% ✅
- registration.py: 100% ✅
- state.py: 95% ✅
- timestamp.py: 91% ✅
- server.py: 87% ✅
- handlers.py: 79% ✅

---

## 🎯 Understanding What Each Test Does

### Integration Tests (`tests/integration/test_server.py`)

```bash
pytest tests/integration/test_server.py -v
```

These simulate a **real game**:

1. **test_handle_game_invitation**: Referee invites you → You accept ✅
2. **test_choose_parity**: Referee asks for choice → You respond "even" or "odd" ✅
3. **test_notify_match_result**: Referee announces winner → You update stats ✅
4. **test_parity_choice_always_lowercase**: CRITICAL! Never "Even" or "ODD" ✅
5. **test_all_responses_have_correct_timestamps**: CRITICAL! Always UTC+Z ✅

### Unit Tests

- **test_timestamp.py**: 25 tests verifying UTC timestamp handling
- **test_protocol.py**: 22 tests for message building
- **test_state.py**: 21 tests for stats tracking
- **test_strategy.py**: 15 tests for parity choice logic
- **test_registration.py**: 12 tests for League Manager registration
- **test_handlers.py**: 10 tests for tool implementations

---

## 🔍 Manual Testing with curl

### Test Game Invitation

```bash
curl -X POST http://localhost:8101/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "handle_game_invitation",
    "params": {
      "conversation_id": "test-001",
      "match_id": "M1",
      "opponent_id": "P02",
      "deadline": "2025-12-31T23:59:59Z"
    },
    "id": 1
  }'
```

**Note**: Will show error about missing auth_token - **this is CORRECT!**
In a real game, the League Manager would provide this after registration.

### Test Parity Choice

```bash
curl -X POST http://localhost:8101/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "choose_parity",
    "params": {
      "conversation_id": "test-002",
      "match_id": "M1",
      "opponent_id": "P02",
      "deadline": "2025-12-31T23:59:59Z"
    },
    "id": 2
  }'
```

**Expected**: Same auth_token error (correct behavior!)

---

## 🎲 Strategy Modes

Your agent has 3 modes:

### 1. Random Strategy (Default)
```bash
python -m src.my_project.agents.player.main --strategy random
```
- **How it works**: `random.choice(["even", "odd"])`
- **Response time**: < 1ms
- **Win rate**: ~50% (optimal for pure chance game)
- **Best for**: Fast, reliable testing

### 2. LLM Strategy (Google Gemini)
```bash
python -m src.my_project.agents.player.main --strategy llm
```
- **How it works**: Sends context to Google Gemini 2.0 Flash
- **Considers**: Opponent patterns, standings, match history
- **Response time**: 1-5 seconds
- **Win rate**: ~50% (same as random - it's a luck game!)
- **Best for**: Interesting reasoning, documentation, analysis

### 3. Hybrid Strategy (Recommended)
```bash
python -m src.my_project.agents.player.main --strategy hybrid
```
- **How it works**: Try Gemini with 25s timeout, fallback to random
- **Best for**: Real games (combines AI insight with reliability)

---

## 🏆 What Success Looks Like

### ✅ ALL CHECKS PASSED:

#### 1. Server Starts Successfully
```
✅ Player Agent ready!
Server running at: http://localhost:8101
```

#### 2. All Tests Pass
```
✅ 115 passed in 2.0s
```

#### 3. Health Check Works
```bash
$ curl http://localhost:8101/health
{"status":"healthy"}
```

#### 4. Stats Tracking Works
```bash
$ curl http://localhost:8101/stats
{
  "player_id": "P01",
  "wins": 0,
  "total_matches": 0,
  ...
}
```

#### 5. Protocol Compliance
- ✅ Timestamps: UTC with 'Z' (e.g., "2025-12-28T10:30:00.123456Z")
- ✅ Parity choices: lowercase only ("even" or "odd", never "Even" or "ODD")
- ✅ Auth tokens: Properly validated
- ✅ Response times: < 5s/30s/10s for different message types

---

## 🐛 Troubleshooting

### "Cannot import name X"
```bash
pip install -e ".[dev]"
```

### "GOOGLE_API_KEY not set"
For LLM/hybrid strategy, add to `.env`:
```
GOOGLE_API_KEY=your_key_here
```
Get free key from: https://aistudio.google.com/apikey

### "Port already in use"
```bash
# Find process on port 8101
lsof -ti:8101 | xargs kill -9

# Or use different port
python -m src.my_project.agents.player.main --port 8102
```

### Tests failing
```bash
# Re-run with verbose output
pytest tests/ -v --tb=short

# Run specific test
pytest tests/integration/test_server.py::TestMCPEndpoint::test_choose_parity -v
```

---

## 📚 Documentation

All documentation is complete (2,573 lines):

- **README.md** (332 lines): Installation, usage, configuration
- **docs/PRD.md** (343 lines): Product requirements
- **docs/ARCHITECTURE.md** (1,008 lines): System design, building blocks
- **docs/PROMPTS_BOOK.md** (890 lines): All AI prompts used

---

## ✨ Your Assignment is Ready for Submission

**Grade Target**: 100/100

**What You've Built**:
- ✅ MCP Player Agent with 3 required tools
- ✅ Google Gemini AI integration
- ✅ 115 passing tests (64% coverage)
- ✅ Complete documentation (2,573 lines)
- ✅ Protocol compliance verified
- ✅ Proper Python package structure

**To Submit**:
1. Make sure all tests pass: `pytest tests/`
2. Check documentation is complete
3. Verify `.env` has no secrets committed
4. Push to git repository
5. Submit according to assignment instructions

---

## 🚀 Next Steps (If League Manager Available)

If your professor provides a League Manager and Referee:

1. **Start your agent:**
   ```bash
   python -m src.my_project.agents.player.main --port 8101
   ```

2. **Your agent will**:
   - Auto-register with League Manager
   - Accept game invitations
   - Choose parity for each match
   - Track wins/losses/draws
   - Update stats after each game

3. **View results:**
   ```bash
   curl http://localhost:8101/stats
   ```

4. **Watch it play** using the API docs:
   ```
   http://localhost:8101/docs
   ```

---

**🎉 Congratulations! Your AI Player Agent is fully functional and ready!**
