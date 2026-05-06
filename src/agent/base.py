"""
Abstract base class for all 2048 agents.

Every agent must implement select_action(board) -> int.
Learning agents override update() and best_value() for TD training.
Non-learning agents (e.g. random) leave them as no-ops.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from core.board import Board


class Agent(ABC):
    """
    Abstract interface for a 2048-playing agent.

    Parameters
    ----------
    None — subclasses define their own constructor arguments.

    Methods required by subclasses
    --------------------------------
    select_action : the only strictly required method.

    Methods with default no-op implementations
    -------------------------------------------
    update       : TD weight update (learning agents override this).
    best_value   : greedy state value used as TD target (learning agents override).
    """

    @abstractmethod
    def select_action(self, board: Board) -> int:
        """
        Choose an action for the given board state.

        Parameters
        ----------
        board : Board
            Current game state. Must not be modified.

        Returns
        -------
        int
            One of LEFT (0), RIGHT (1), UP (2), DOWN (3).
            Should be a valid move when possible, but the caller
            silently ignores invalid moves per game rules.
        """
        ...

    def best_value(self, board: Board) -> float:
        """
        Estimated value of the best reachable after-state from `board`.

        For TD agents: best_value(s) = max_a [r(s,a) + V(after_state(s,a))].
        For non-learning agents: returns 0.0 (no value function defined).

        This is used by the trainer as the TD target for the previous step.

        Parameters
        ----------
        board : Board
            Current game state (before any move).

        Returns
        -------
        float
            Estimated best achievable value. 0.0 for non-learning agents.
        """
        return 0.0

    def update(self, after_state: Board, target: float) -> None:
        """
        Apply a TD weight update.

        Called by the trainer after each move:
            V(after_state) += alpha * (target - V(after_state))

        Non-learning agents (random, etc.) leave this as a no-op.

        Parameters
        ----------
        after_state : Board
            The after-state whose value estimate should be updated.
            This is the board state *after* a move but *before* tile spawning.
        target : float
            The TD target:
              - best_value(next_state)  during the game
              - 0.0                     at game termination
        """
