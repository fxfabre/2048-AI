"""
Random baseline agent for 2048.

Always picks a uniformly random move among the currently valid moves.
Used as a sanity check: a learning agent should quickly outperform this.

Typical random-agent performance on this variant (win tile = 64):
  - Average score  : ~600–800
  - Win rate (≥64) : ~10–20%
"""

from __future__ import annotations

import numpy as np

from agent.base import Agent
from core.board import DOWN, LEFT, RIGHT, UP, Board

MOVES = [LEFT, RIGHT, UP, DOWN]


class RandomAgent(Agent):
    """
    Selects a uniformly random valid move at each step.

    Parameters
    ----------
    rng : np.random.Generator, optional
        Random number generator. A fresh generator is created if not supplied.
    """

    def __init__(self, rng: np.random.Generator | None = None) -> None:
        self.rng: np.random.Generator = rng if rng is not None else np.random.default_rng()

    def select_action(self, board: Board) -> int:
        """
        Return a uniformly random valid move.

        Falls back to a random move from all directions if — somehow — no move
        is valid (should not happen before game-over, but avoids an empty-choice
        crash in edge cases).
        """
        valid = [m for m in MOVES if board.is_move_valid(m)]
        pool = valid if valid else MOVES
        return int(self.rng.choice(pool))
