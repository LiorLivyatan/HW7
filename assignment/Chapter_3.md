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
