"""
Player State Management - Building Block: PlayerState

Purpose:
    Manages player agent state including identity, authentication, statistics, and match history.
    Provides persistence and state updates based on game results.

Input Data:
    - player_id (str): Player identifier (e.g., "P01")
    - display_name (str): Human-readable name
    - Game result messages (GAME_OVER)

Output Data:
    - Current player state (ID, auth token, stats)
    - Match history
    - Statistics (wins, draws, losses, points)

Setup/Configuration:
    - persistence_enabled (bool): Whether to save state to file
    - history_max_entries (int): Maximum match history size
    - state_file_path (str): Path to persistence file

References:
    - Assignment Chapter 3: Even/Odd Game Rules (scoring system)
    - config.yaml: state section
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import json
from datetime import datetime

from ...utils.timestamp import utc_now


@dataclass
class MatchResult:
    """Single match result record."""
    match_id: str
    opponent_id: str
    player_choice: str  # "even" or "odd"
    opponent_choice: str
    drawn_number: int  # 1-10
    result: str  # "win", "draw", or "loss"
    points_earned: int  # 3 for win, 1 for draw, 0 for loss
    timestamp: str  # When match completed


class PlayerState:
    """
    Player agent state management.

    This building block tracks:
    1. Player identity (ID, display name)
    2. Authentication (auth token from registration)
    3. Statistics (wins, draws, losses, total points)
    4. Match history (recent game results)
    5. Persistence (optional save/load from file)

    Example:
        >>> state = PlayerState(player_id="P01", display_name="Gemini Agent")
        >>> state.set_auth_token("auth-token-12345")
        >>> state.update_from_result({
        ...     "match_id": "R1M1",
        ...     "winner": "P01",
        ...     "drawn_number": 4,
        ...     ...
        ... })
        >>> print(state.get_stats())
        {'wins': 1, 'draws': 0, 'losses': 0, 'total_points': 3}
    """

    def __init__(
        self,
        player_id: str,
        display_name: str = "Player",
        max_history_entries: int = 100,
        persistence_enabled: bool = False,
        state_file_path: Optional[str] = None
    ):
        """
        Initialize player state.

        Args:
            player_id: Player identifier (e.g., "P01")
            display_name: Human-readable player name
            max_history_entries: Maximum number of matches to keep in history
            persistence_enabled: Whether to auto-save state to file
            state_file_path: Path to state persistence file

        Raises:
            ValueError: If player_id is None or empty
        """
        if not player_id:
            raise ValueError("player_id cannot be None or empty")

        self.player_id = player_id
        self.display_name = display_name
        self.max_history_entries = max_history_entries
        self.persistence_enabled = persistence_enabled
        self.state_file_path = state_file_path

        # Authentication
        self.auth_token: Optional[str] = None
        self.registered: bool = False

        # Statistics
        self.stats = {
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "total_points": 0,
            "total_matches": 0,
        }

        # Match history
        self.match_history: List[MatchResult] = []

        # Load persisted state if enabled
        if self.persistence_enabled and self.state_file_path:
            self._load_state()

    def set_auth_token(self, auth_token: str) -> None:
        """
        Set authentication token after registration.

        Args:
            auth_token: Token from LEAGUE_REGISTER_RESPONSE

        Important:
            This should be called immediately after successful registration.
            The auth_token must be included in all subsequent protocol messages.
        """
        self.auth_token = auth_token
        self.registered = True
        self._maybe_save_state()

    def update_from_result(self, game_over_msg: Dict[str, Any]) -> None:
        """
        Update state based on GAME_OVER message from Referee.

        Extracts match details, determines win/loss/draw, updates statistics,
        and adds to match history.

        Args:
            game_over_msg: GAME_OVER message from Referee

        Expected structure:
            {
                "match_id": "R1M1",
                "winner": "P01" or None (for draw),
                "drawn_number": 4,
                "choices": {
                    "P01": "even",
                    "P02": "odd"
                },
                "opponent_id": "P02",
                ...
            }

        Example:
            >>> state.update_from_result({
            ...     "match_id": "R1M1",
            ...     "winner": "P01",
            ...     "drawn_number": 4,
            ...     "choices": {"P01": "even", "P02": "odd"},
            ...     "opponent_id": "P02"
            ... })
            >>> state.stats["wins"]
            1
        """
        match_id = game_over_msg.get("match_id", "unknown")
        winner = game_over_msg.get("winner")
        drawn_number = game_over_msg.get("drawn_number", 0)
        choices = game_over_msg.get("choices", {})
        opponent_id = game_over_msg.get("opponent_id", "unknown")

        # Get player and opponent choices
        player_choice = choices.get(self.player_id, "unknown")
        opponent_choice = choices.get(opponent_id, "unknown")

        # Determine result
        if winner is None:
            result = "draw"
            points_earned = 1
            self.stats["draws"] += 1
        elif winner == self.player_id:
            result = "win"
            points_earned = 3
            self.stats["wins"] += 1
        else:
            result = "loss"
            points_earned = 0
            self.stats["losses"] += 1

        # Update statistics
        self.stats["total_points"] += points_earned
        self.stats["total_matches"] += 1

        # Add to match history
        match_record = MatchResult(
            match_id=match_id,
            opponent_id=opponent_id,
            player_choice=player_choice,
            opponent_choice=opponent_choice,
            drawn_number=drawn_number,
            result=result,
            points_earned=points_earned,
            timestamp=utc_now()
        )

        self.match_history.append(match_record)

        # Trim history if exceeds max entries
        if len(self.match_history) > self.max_history_entries:
            self.match_history = self.match_history[-self.max_history_entries:]

        # Persist if enabled
        self._maybe_save_state()

    def get_stats(self) -> Dict[str, int]:
        """
        Get current statistics.

        Returns:
            dict: Statistics with wins, draws, losses, total_points, total_matches

        Example:
            >>> stats = state.get_stats()
            >>> print(f"Win rate: {stats['wins'] / stats['total_matches']:.2%}")
        """
        return self.stats.copy()

    def get_win_rate(self) -> float:
        """
        Calculate win rate as percentage.

        Returns:
            float: Win rate (0.0 to 1.0), or 0.0 if no matches played

        Example:
            >>> state.stats = {"wins": 7, "total_matches": 10}
            >>> state.get_win_rate()
            0.7
        """
        if self.stats["total_matches"] == 0:
            return 0.0
        return self.stats["wins"] / self.stats["total_matches"]

    def get_match_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get match history records.

        Args:
            limit: Optional limit on number of recent matches to return

        Returns:
            list: List of match records (most recent last)

        Example:
            >>> recent_matches = state.get_match_history(limit=5)
            >>> for match in recent_matches:
            ...     print(f"{match['result']}: {match['match_id']}")
        """
        history = [asdict(m) for m in self.match_history]

        if limit:
            return history[-limit:]
        return history

    def get_opponent_history(self, opponent_id: str) -> List[Dict[str, Any]]:
        """
        Get match history against specific opponent.

        Args:
            opponent_id: Opponent player ID

        Returns:
            list: List of matches against this opponent

        Example:
            >>> p02_matches = state.get_opponent_history("P02")
            >>> wins_vs_p02 = sum(1 for m in p02_matches if m['result'] == 'win')
        """
        return [
            asdict(m) for m in self.match_history
            if m.opponent_id == opponent_id
        ]

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize state to dictionary.

        Returns:
            dict: Complete state as dictionary

        Example:
            >>> state_dict = state.to_dict()
            >>> json.dumps(state_dict, indent=2)
        """
        return {
            "player_id": self.player_id,
            "display_name": self.display_name,
            "auth_token": self.auth_token,
            "registered": self.registered,
            "stats": self.stats,
            "match_history": self.get_match_history(),
            "last_updated": utc_now(),
        }

    def _maybe_save_state(self) -> None:
        """Save state to file if persistence is enabled."""
        if self.persistence_enabled and self.state_file_path:
            try:
                state_path = Path(self.state_file_path)
                state_path.parent.mkdir(parents=True, exist_ok=True)

                with open(state_path, 'w') as f:
                    json.dump(self.to_dict(), f, indent=2)
            except Exception as e:
                # Don't fail if save fails - just log it
                print(f"Warning: Failed to save state: {e}")

    def _load_state(self) -> None:
        """Load state from file if it exists."""
        if not self.state_file_path:
            return

        state_path = Path(self.state_file_path)
        if not state_path.exists():
            return

        try:
            with open(state_path, 'r') as f:
                data = json.load(f)

            # Restore state
            self.auth_token = data.get("auth_token")
            self.registered = data.get("registered", False)
            self.stats = data.get("stats", self.stats)

            # Restore match history
            history_data = data.get("match_history", [])
            self.match_history = [
                MatchResult(**m) for m in history_data
            ]
        except Exception as e:
            print(f"Warning: Failed to load state: {e}")
