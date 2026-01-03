"""
Console Visualization Utilities

Provides rich terminal output for the Player Agent with professional formatting.
Uses the rich library for colored panels, tables, progress indicators, and more.
"""

from typing import Dict, Optional, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from datetime import datetime


# Global console instance
console = Console()


def print_startup_banner(
    player_id: str,
    display_name: str,
    port: int,
    strategy: str,
    host: str = "localhost"
):
    """
    Display a professional startup banner when the agent starts.

    Args:
        player_id: Player identifier (e.g., "P01")
        display_name: Human-readable name
        port: Server port number
        strategy: Strategy mode ("random", "hybrid", "llm")
        host: Server hostname
    """
    # Strategy emoji mapping
    strategy_emoji = {
        "random": "🎲",
        "hybrid": "🧠",
        "llm": "🤖"
    }
    emoji = strategy_emoji.get(strategy, "🎮")

    # Build banner content
    content = Text()
    content.append("🎮 Even/Odd League Player Agent\n\n", style="bold cyan")
    content.append(f"Player ID:     ", style="dim")
    content.append(f"{player_id}\n", style="bold yellow")
    content.append(f"Display Name:  ", style="dim")
    content.append(f"{display_name}\n", style="bold green")
    content.append(f"Strategy:      ", style="dim")
    content.append(f"{emoji} {strategy.upper()}\n", style="bold magenta")
    content.append(f"Server:        ", style="dim")
    content.append(f"http://{host}:{port}\n", style="bold blue")
    content.append(f"MCP Endpoint:  ", style="dim")
    content.append(f"http://{host}:{port}/mcp\n", style="bold blue")

    panel = Panel(
        content,
        title="[bold white]PLAYER AGENT STARTING[/bold white]",
        border_style="bright_cyan",
        expand=False
    )
    console.print(panel)
    console.print()


def print_game_invitation(
    match_id: str,
    opponent_id: str,
    game_type: str,
    deadline: str,
    accepted: bool = True,
    response_time: Optional[float] = None
):
    """
    Display game invitation details.

    Args:
        match_id: Match identifier
        opponent_id: Opponent player ID
        game_type: Type of game
        deadline: ISO-8601 deadline
        accepted: Whether invitation was accepted
        response_time: Time taken to respond in seconds
    """
    content = Text()
    content.append(f"Match ID:  ", style="dim")
    content.append(f"{match_id}\n", style="bold white")
    content.append(f"Opponent:  ", style="dim")
    content.append(f"{opponent_id}\n", style="bold yellow")
    content.append(f"Game Type: ", style="dim")
    content.append(f"{game_type}\n", style="bold cyan")
    content.append(f"Deadline:  ", style="dim")
    content.append(f"{deadline}\n", style="dim cyan")

    if response_time is not None:
        content.append(f"\n", style="dim")
        status_emoji = "✅" if accepted else "❌"
        status_text = "ACCEPTED" if accepted else "DECLINED"
        content.append(f"{status_emoji} {status_text} ", style="bold green" if accepted else "bold red")
        content.append(f"(responded in {response_time:.2f}s)", style="dim")

    panel = Panel(
        content,
        title="[bold white]🎮 GAME INVITATION RECEIVED[/bold white]",
        border_style="green" if accepted else "red",
        expand=False
    )
    console.print(panel)
    console.print()


def print_parity_thinking(
    match_id: str,
    opponent_id: str,
    standings: Optional[Dict[str, int]] = None,
    strategy_mode: str = "random"
):
    """
    Display parity choice context before thinking.

    Args:
        match_id: Match identifier
        opponent_id: Opponent player ID
        standings: Current league standings
        strategy_mode: Strategy being used
    """
    content = Text()
    content.append(f"Match ID:  ", style="dim")
    content.append(f"{match_id}\n", style="bold white")
    content.append(f"Opponent:  ", style="dim")
    content.append(f"{opponent_id}\n", style="bold yellow")

    if standings:
        content.append(f"\nCurrent Standings:\n", style="bold cyan")
        for player, points in sorted(standings.items(), key=lambda x: x[1], reverse=True):
            content.append(f"  {player}: ", style="dim")
            content.append(f"{points} pts\n", style="bold white")

    content.append(f"\nStrategy: ", style="dim")
    strategy_emoji = {"random": "🎲", "hybrid": "🧠", "llm": "🤖"}.get(strategy_mode, "🎮")
    content.append(f"{strategy_emoji} {strategy_mode.upper()}", style="bold magenta")

    panel = Panel(
        content,
        title="[bold white]🎲 PARITY CHOICE REQUESTED[/bold white]",
        border_style="yellow",
        expand=False
    )
    console.print(panel)


def print_parity_choice(choice: str, response_time: float, used_llm: bool = False):
    """
    Display the parity choice made.

    Args:
        choice: "even" or "odd"
        response_time: Time taken to decide in seconds
        used_llm: Whether LLM was used for decision
    """
    choice_upper = choice.upper()
    choice_emoji = "⚡" if choice == "even" else "⭐"

    text = Text()
    text.append(f"💭 My Choice: ", style="dim")
    text.append(f"{choice_emoji} {choice_upper}\n", style="bold green")

    if used_llm:
        text.append(f"🤖 Decision made by LLM ", style="dim cyan")
    else:
        text.append(f"🎲 Random choice ", style="dim yellow")

    text.append(f"({response_time:.2f}s)", style="dim")

    console.print(text)
    console.print()


def print_match_result(
    match_id: str,
    drawn_number: int,
    my_choice: str,
    opponent_choice: str,
    my_player_id: str,
    opponent_id: str,
    winner: Optional[str] = None,
    points_earned: int = 0
):
    """
    Display match result with dramatic formatting.

    Args:
        match_id: Match identifier
        drawn_number: Number drawn by referee (1-10)
        my_choice: Our parity choice
        opponent_choice: Opponent's parity choice
        my_player_id: Our player ID
        opponent_id: Opponent player ID
        winner: Winner player ID (None for draw)
        points_earned: Points we earned (3, 1, or 0)
    """
    # Determine outcome
    if winner is None:
        outcome = "DRAW"
        title_style = "yellow"
        emoji = "🤝"
    elif winner == my_player_id:
        outcome = "VICTORY"
        title_style = "green"
        emoji = "🏆"
    else:
        outcome = "DEFEAT"
        title_style = "red"
        emoji = "💔"

    # Check if number matches choices
    is_even = drawn_number % 2 == 0
    my_correct = (is_even and my_choice == "even") or (not is_even and my_choice == "odd")
    opp_correct = (is_even and opponent_choice == "even") or (not is_even and opponent_choice == "odd")

    content = Text()
    content.append(f"Drawn Number: ", style="dim")
    content.append(f"{drawn_number} ", style="bold white")
    content.append(f"({'even' if is_even else 'odd'})\n\n", style="dim")

    content.append(f"{my_player_id} (You):    ", style="dim")
    content.append(f"{my_choice} ", style="bold cyan")
    content.append(f"{'✅' if my_correct else '❌'}\n", style="")

    content.append(f"{opponent_id} (Them): ", style="dim")
    content.append(f"{opponent_choice} ", style="bold yellow")
    content.append(f"{'✅' if opp_correct else '❌'}\n\n", style="")

    content.append(f"Result: ", style="dim")
    content.append(f"{emoji} {outcome}\n", style=f"bold {title_style}")
    content.append(f"Points Earned: ", style="dim")
    content.append(f"+{points_earned}", style="bold white")

    panel = Panel(
        content,
        title=f"[bold white]{emoji} MATCH RESULT[/bold white]",
        border_style=title_style,
        expand=False
    )
    console.print(panel)
    console.print()


def print_stats_summary(
    wins: int,
    losses: int,
    draws: int,
    total_points: int,
    matches_played: int
):
    """
    Display player statistics in a table.

    Args:
        wins: Number of wins
        losses: Number of losses
        draws: Number of draws
        total_points: Total points accumulated
        matches_played: Total matches played
    """
    win_rate = (wins / matches_played * 100) if matches_played > 0 else 0.0

    table = Table(title="📊 YOUR STATS", show_header=False, border_style="cyan")
    table.add_column("Metric", style="dim", width=15)
    table.add_column("Value", style="bold white", width=10)

    table.add_row("Wins", f"🏆 {wins}")
    table.add_row("Losses", f"💔 {losses}")
    table.add_row("Draws", f"🤝 {draws}")
    table.add_row("Matches", str(matches_played))
    table.add_row("Win Rate", f"{win_rate:.1f}%")
    table.add_row("Total Points", f"⭐ {total_points}")

    console.print(table)
    console.print()


def print_error(error_message: str, context: Optional[str] = None):
    """
    Display an error message in a red panel.

    Args:
        error_message: The error message
        context: Optional context about where the error occurred
    """
    content = Text()
    if context:
        content.append(f"{context}\n\n", style="bold yellow")
    content.append(error_message, style="red")

    panel = Panel(
        content,
        title="[bold white]❌ ERROR[/bold white]",
        border_style="red",
        expand=False
    )
    console.print(panel)
    console.print()


def print_info(message: str, title: str = "INFO"):
    """
    Display an informational message.

    Args:
        message: The information to display
        title: Panel title
    """
    panel = Panel(
        message,
        title=f"[bold white]ℹ️  {title}[/bold white]",
        border_style="blue",
        expand=False
    )
    console.print(panel)
    console.print()
