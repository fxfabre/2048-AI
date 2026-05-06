"""
Play 2048 with a trained agent (console mode).

Usage
-----
    # Watch the agent play one game step by step
    python scripts/play.py --weights experiments/runs/my_run/weights_final.npz

    # Run N games silently and print statistics
    python scripts/play.py --weights experiments/runs/my_run/weights_final.npz --games 200

    # Slow down the display (seconds between moves)
    python scripts/play.py --weights experiments/runs/my_run/weights_final.npz --delay 0.3

    # Use the random baseline (no weights needed)
    python scripts/play.py --random --games 100

Options
-------
    --weights   Path to a .npz weights file produced by train.py.
    --random    Use the random baseline agent instead.
    --games     Number of games to play. Default: 1 (with display).
    --delay     Seconds between moves when displaying. Default: 0.05.
    --no-display  Run silently (useful with --games > 1).
    --seed      Random seed. Default: 0.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

from agent.random import RandomAgent
from agent.td_ntuple import TDNTupleAgent
from core.board import DOWN, LEFT, RIGHT, UP, Board, WIN_EXPONENT
from training.evaluator import evaluate

# Direction labels for display
DIRECTION_NAMES = {LEFT: "LEFT", RIGHT: "RIGHT", UP: "UP", DOWN: "DOWN"}

# Tile colours in terminal (ANSI). Falls back gracefully if not supported.
TILE_COLORS: dict[int, str] = {
    0:    "\033[0m",         # empty       — reset
    2:    "\033[37m",        # white
    4:    "\033[33m",        # yellow
    8:    "\033[91m",        # bright red
    16:   "\033[93m",        # bright yellow
    32:   "\033[92m",        # bright green
    64:   "\033[96m",        # bright cyan
    128:  "\033[94m",        # bright blue
    256:  "\033[95m",        # bright magenta
    512:  "\033[31m",        # red
    1024: "\033[32m",        # green
    2048: "\033[33;1m",      # bold yellow
}
RESET = "\033[0m"


def render_board(board: Board) -> str:
    """Return a coloured ASCII representation of the board."""
    values = board.tile_values()
    win_value = 2 ** WIN_EXPONENT
    lines = [f"Score: {board.score}"]
    lines.append("┌" + ("───────┬" * 3) + "───────┐")
    for r in range(4):
        cells = []
        for c in range(4):
            v = int(values[r, c])
            color = TILE_COLORS.get(v, "\033[35m")
            label = str(v) if v > 0 else "·"
            # Pad to width 5 and center
            padded = label.center(5)
            marker = "★" if v >= win_value else " "
            cells.append(f"{color}{marker}{padded}{marker}{RESET}")
        lines.append("│" + "│".join(cells) + "│")
        if r < 3:
            lines.append("├" + ("───────┼" * 3) + "───────┤")
    lines.append("└" + ("───────┴" * 3) + "───────┘")
    return "\n".join(lines)


def play_one_game(
    agent: TDNTupleAgent | RandomAgent,
    rng: np.random.Generator,
    display: bool = True,
    delay: float = 0.05,
) -> tuple[int, int, int]:
    """
    Play one complete game.

    Returns (score, max_tile, n_moves).
    """
    board = Board(rng=rng)
    n_moves = 0

    if display:
        print("\033[H\033[J", end="")  # clear screen
        print(render_board(board))
        time.sleep(delay)

    while not board.is_game_over() and not board.is_won():
        action = agent.select_action(board)
        board.move(action)
        n_moves += 1

        if display:
            print("\033[H\033[J", end="")  # clear screen
            print(render_board(board))
            print(f"Move: {DIRECTION_NAMES[action]}   Moves: {n_moves}")
            time.sleep(delay)

    if display:
        outcome = "🏆 WIN!" if board.is_won() else "Game over"
        print(f"\n{outcome}  Score: {board.score}  Max tile: {board.max_tile()}  Moves: {n_moves}")

    return board.score, board.max_tile(), n_moves


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Play 2048 with a trained agent.")
    group = p.add_mutually_exclusive_group()
    group.add_argument("--weights", default=None,
                       help="Path to .npz weights file (from train.py).")
    group.add_argument("--random", action="store_true",
                       help="Use the random baseline agent.")
    p.add_argument("--games", type=int, default=1,
                   help="Number of games to play.")
    p.add_argument("--delay", type=float, default=0.05,
                   help="Seconds between moves when displaying (default 0.05).")
    p.add_argument("--no-display", action="store_true",
                   help="Disable board display (useful with --games > 1).")
    p.add_argument("--seed", type=int, default=0,
                   help="Random seed.")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    # ------------------------------------------------------------------ #
    # Agent                                                                #
    # ------------------------------------------------------------------ #
    if args.random:
        rng = np.random.default_rng(args.seed)
        agent: TDNTupleAgent | RandomAgent = RandomAgent(rng=rng)
        print("Agent: Random baseline")
    elif args.weights:
        weights_path = pathlib.Path(args.weights)
        if not weights_path.exists():
            print(f"ERROR: weights file not found: {weights_path}", file=sys.stderr)
            sys.exit(1)
        agent = TDNTupleAgent.load(weights_path)
        print(f"Agent: {agent}")
        print(f"Weights: {weights_path}")
    else:
        print("ERROR: provide --weights <path> or --random", file=sys.stderr)
        sys.exit(1)

    rng = np.random.default_rng(args.seed)
    display = not args.no_display and args.games == 1

    print()

    # ------------------------------------------------------------------ #
    # Play                                                                 #
    # ------------------------------------------------------------------ #
    if args.games == 1:
        play_one_game(agent, rng=rng, display=display, delay=args.delay)

    else:
        # Multi-game: run silently then print statistics
        print(f"Running {args.games} games...", end="", flush=True)
        result = evaluate(agent, n_games=args.games, rng=rng, learn=False)
        print(" done.\n")
        print(result)


if __name__ == "__main__":
    main()
