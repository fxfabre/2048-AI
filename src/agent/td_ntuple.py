"""
TD-Learning agent with N-tuple networks for 2048.

Background — why N-tuple networks?
-------------------------------------
A neural network is the classical tool for function approximation in RL, but
for 2048 the board is small and structured enough that a much simpler approach
works better: N-tuple networks (Szubert & Jaskowski, 2014).

Instead of parameterizing V(s) with a deep network, we break the board into a
fixed set of cell groups ("tuples") and give each group its own lookup table.
The value of a state is just the *sum* of the relevant table entries:

    V(s) = sum_{tuple t} weights_t [ index_t(s) ]

where index_t(s) encodes the exponents of the N cells in tuple t as a single
integer (base-8 positional encoding).

This makes V(s) linear in the weights: fast to evaluate and easy to update.

After-state value function
--------------------------
A move from state s yields a deterministic "after-state" as(s,a): tiles slide
and merge, but no new tile has spawned yet.  We learn V over after-states, not
over the full states.  Advantage: the update target is deterministic — we don't
need to average over the random tile spawn.

Action selection (greedy)
--------------------------
    Q(s, a) = r(s, a) + V(as(s, a))
    a*      = argmax_a Q(s, a)

where r(s, a) is the score gained by move a (known immediately).

TD(0) update — one-step temporal difference
--------------------------------------------
After the environment spawns a tile (s -> s'), the trainer calls:

    target       = best_value(s') = max_a' [r(s', a') + V(as(s', a'))]
    td_error     = target - V(as(s, a*))
    weights_t[i] += alpha * td_error   for each active tuple t with index i

At game termination the target is 0 (no future reward).

Why not divide by n_tuples?
    The standard N-tuple update applies the *full* alpha * td_error to each
    active weight.  The effective step size therefore scales with the number of
    tuples, so you should use a smaller alpha with more tuples.  An alternative
    is alpha / n_tuples per weight — both are common; we follow the literature
    default here.

Reference: Szubert & Jaskowski (2014); Guei et al. (2022) arxiv:2212.11087.
"""

from __future__ import annotations

import pathlib

import numpy as np

from agent.base import Agent
from core.board import DOWN, LEFT, RIGHT, UP, Board

MOVES = [LEFT, RIGHT, UP, DOWN]

# Exponent range used for weight-table sizing: 0 (empty) .. MAX_EXP-1.
# We use 8 so the table covers exponents 0–7, matching the LUT range.
MAX_EXP: int = 8

# ---------------------------------------------------------------------------
# Default tuple definitions — flat cell indices on the 4×4 grid
#
# Layout (row-major):
#   0   1   2   3
#   4   5   6   7
#   8   9  10  11
#  12  13  14  15
#
# We use 8 four-tuples: the 4 rows + 4 columns.
# Each 4-tuple has 8^4 = 4 096 weight entries.
# Total parameters: 8 × 4 096 = 32 768 floats ≈ 256 KB (float64).
# ---------------------------------------------------------------------------
DEFAULT_TUPLES: list[tuple[int, ...]] = [
    # Rows
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (8, 9, 10, 11),
    (12, 13, 14, 15),
    # Columns
    (0, 4, 8, 12),
    (1, 5, 9, 13),
    (2, 6, 10, 14),
    (3, 7, 11, 15),
]


class TDNTupleAgent(Agent):
    """
    Temporal-difference learning agent using N-tuple networks.

    Parameters
    ----------
    tuples : list of tuple[int, ...], optional
        Each inner tuple lists the flat cell indices (0–15) that form one
        N-tuple.  All tuples must have the same length N.
        Defaults to DEFAULT_TUPLES (4 rows + 4 columns).
    alpha : float
        Learning rate.  Typical range: 0.01 – 0.5.
        With 8 four-tuples the effective per-state step is 8 × alpha.
    gamma : float
        Discount factor.  Use 1.0 for undiscounted return (standard for 2048).
    init_value : float
        Initial value for every weight.  0.0 = pessimistic start (safe).
        A small positive value (e.g. 1.0) is "optimistic" — it encourages the
        agent to explore under-visited patterns early in training.
    """

    def __init__(
        self,
        tuples: list[tuple[int, ...]] | None = None,
        alpha: float = 0.1,
        gamma: float = 1.0,
        init_value: float = 0.0,
    ) -> None:
        self.tuples: list[tuple[int, ...]] = tuples if tuples is not None else DEFAULT_TUPLES
        self.alpha: float = alpha
        self.gamma: float = gamma
        self.n_tuples: int = len(self.tuples)

        # Validate: all tuples should contain valid cell indices (0–15)
        for t in self.tuples:
            for idx in t:
                if not (0 <= idx <= 15):
                    msg = f"Cell index {idx} out of range [0, 15] in tuple {t}"
                    raise ValueError(msg)

        # One flat weight array per tuple.
        # For a tuple of size N, the table has MAX_EXP^N entries.
        # Positional encoding: index = e0 + 8*e1 + 64*e2 + ...
        self.weights: list[np.ndarray] = [
            np.full(MAX_EXP ** len(t), init_value, dtype=np.float64)
            for t in self.tuples
        ]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _tuple_index(self, grid_flat: np.ndarray, tup: tuple[int, ...]) -> int:
        """
        Compute the flat weight-table index for `tup` given the flat board.

        Positional (base-8) encoding:
            index = e0 * 8^0 + e1 * 8^1 + e2 * 8^2 + ...
        """
        idx = 0
        for power, cell in enumerate(tup):
            idx += int(grid_flat[cell]) * (MAX_EXP ** power)
        return idx

    def _get_value(self, board: Board) -> float:
        """
        Evaluate V(board) = sum over all tuples of their active weight.

        This is an O(n_tuples × tuple_size) operation — very fast.
        """
        grid_flat = board.grid.ravel()
        return sum(
            w[self._tuple_index(grid_flat, t)]
            for t, w in zip(self.tuples, self.weights)
        )

    def _best_action_value(self, board: Board) -> tuple[int, float]:
        """
        Greedy action selection.

        For each valid move a, compute:
            Q(s, a) = r(s, a) + V(after_state(s, a))

        Returns
        -------
        best_action : int
            The action with the highest Q value.  -1 if no valid move exists.
        best_q : float
            The corresponding Q value.  -inf if no valid move exists.
        """
        best_action = -1
        best_q = -np.inf

        for action in MOVES:
            # Compute after_state without modifying the real board.
            # _apply_move is a private Board method; using it here intentionally
            # because we own the class and need spawn=False for after-states.
            candidate = board.copy()
            changed, score = candidate._apply_move(action, spawn=False)
            if not changed:
                continue  # invalid move

            q = float(score) + self._get_value(candidate)
            if q > best_q:
                best_q = q
                best_action = action

        return best_action, best_q

    # ------------------------------------------------------------------
    # Agent interface
    # ------------------------------------------------------------------

    def select_action(self, board: Board) -> int:
        """
        Return the greedy action: argmax_a [r(s,a) + V(after_state(s,a))].

        Falls back to LEFT as a last resort (should never be needed if called
        before game-over).
        """
        action, _ = self._best_action_value(board)
        if action == -1:
            # Fallback: pick any valid move
            for a in MOVES:
                if board.is_move_valid(a):
                    return a
            return LEFT
        return action

    def best_value(self, board: Board) -> float:
        """
        Return max_a [r(s,a) + V(after_state(s,a))].

        This is the TD target the trainer uses to update the *previous*
        after-state's value.  Returns 0.0 when no valid move exists (terminal).
        """
        _, q = self._best_action_value(board)
        return q if q != -np.inf else 0.0

    def update(self, after_state: Board, target: float) -> None:
        """
        Apply a one-step TD(0) update to the weights of `after_state`.

        Math:
            current = V(after_state) = sum_t weights_t[i_t]
            td_error = target - current
            weights_t[i_t] += alpha * td_error   for all t

        Parameters
        ----------
        after_state : Board
            The after-state whose value we want to improve.
        target : float
            TD target.  During play: best_value(next_state).
            At terminal: 0.0.
        """
        current = self._get_value(after_state)
        td_error = target - current
        delta = self.alpha * td_error

        grid_flat = after_state.grid.ravel()
        for tup, w in zip(self.tuples, self.weights):
            w[self._tuple_index(grid_flat, tup)] += delta

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: str | pathlib.Path) -> None:
        """Save all weight tables to a .npz file."""
        np.savez(str(path), *self.weights)

    @classmethod
    def load(
        cls,
        path: str | pathlib.Path,
        tuples: list[tuple[int, ...]] | None = None,
        alpha: float = 0.1,
        gamma: float = 1.0,
    ) -> TDNTupleAgent:
        """
        Load weight tables from a .npz file produced by save().

        The tuple definitions are NOT stored in the file — you must pass the
        same `tuples` argument that was used when saving.
        """
        data = np.load(str(path))
        agent = cls(tuples=tuples, alpha=alpha, gamma=gamma)
        for i, key in enumerate(sorted(data.files)):
            agent.weights[i] = data[key]
        return agent

    def __repr__(self) -> str:
        size = sum(w.nbytes for w in self.weights) / 1024
        return (
            f"TDNTupleAgent("
            f"n_tuples={self.n_tuples}, "
            f"tuple_size={len(self.tuples[0])}, "
            f"alpha={self.alpha}, "
            f"weights={size:.1f} KB)"
        )
