"""
2048 board logic for a 4x4 grid.

Tile representation
-------------------
Tiles are stored as exponents of 2 in a 4x4 numpy array (dtype=int8):
  0  -> empty cell
  1  -> tile 2   (2^1)
  2  -> tile 4   (2^2)
  3  -> tile 8   (2^3)
  4  -> tile 16  (2^4)
  5  -> tile 32  (2^5)
  6  -> tile 64  (2^6)  <- winning tile

This representation makes merging trivial (exponent + 1) and keeps the
board compact (values fit in int8).

Move directions
---------------
  0 = LEFT
  1 = RIGHT
  2 = UP
  3 = DOWN

UP/DOWN are handled by transposing the board, applying LEFT/RIGHT, then
transposing back — reusing the same row-level lookup table.

Random tile spawning
---------------------
After each valid move, a new tile spawns on a random empty cell:
  - tile 2  (exponent 1) with probability 0.9
  - tile 4  (exponent 2) with probability 0.1
This matches the original 2048 rules.
"""

from __future__ import annotations

import numpy as np

from core.moves_lut import LUT

# Direction constants
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

# Winning tile exponent: 2^6 = 64
WIN_EXPONENT = 6

# Spawn probabilities: (exponent, probability)
SPAWN_TILES = [(1, 0.9), (2, 0.1)]


class Board:
    """
    Represents a 2048 game board.

    Attributes
    ----------
    grid : np.ndarray, shape (4, 4), dtype int8
        Tile exponents. 0 = empty, k = tile 2^k.
    score : int
        Cumulative score for the current game.
    rng : np.random.Generator
        Random number generator (seeded for reproducibility if needed).
    """

    def __init__(self, rng: np.random.Generator | None = None) -> None:
        self.grid: np.ndarray = np.zeros((4, 4), dtype=np.int8)
        self.score: int = 0
        self.rng: np.random.Generator = rng if rng is not None else np.random.default_rng()

        # Spawn two tiles to start the game
        self._spawn_tile()
        self._spawn_tile()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _spawn_tile(self) -> None:
        """Spawn a new tile (2 or 4) on a random empty cell."""
        empty_cells = list(zip(*np.where(self.grid == 0)))
        if not empty_cells:
            return

        row, col = empty_cells[self.rng.integers(len(empty_cells))]
        exponents, probs = zip(*SPAWN_TILES)
        new_exp = self.rng.choice(exponents, p=probs)
        self.grid[row, col] = new_exp

    def _apply_move_to_row(self, row: np.ndarray, direction: int) -> tuple[np.ndarray, int]:
        """
        Apply a left or right move to a single row using the lookup table.

        Parameters
        ----------
        row : np.ndarray, shape (4,)
            A single row of tile exponents.
        direction : int
            LEFT or RIGHT.

        Returns
        -------
        new_row : np.ndarray, shape (4,)
        score_gained : int
        """
        key = tuple(int(x) for x in row)
        result = LUT[key]["left" if direction == LEFT else "right"]
        return np.array(result.row, dtype=np.int8), result.score

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def is_move_valid(self, direction: int) -> bool:
        """
        Return True if the given move changes the board state.
        A move is invalid if no tile would move or merge.
        """
        test = Board.__new__(Board)
        test.grid = self.grid.copy()
        test.score = self.score
        test.rng = self.rng
        changed, _ = test._apply_move(direction, spawn=False)
        return changed

    def _apply_move(self, direction: int, spawn: bool = True) -> tuple[bool, int]:
        """
        Apply a move to the board in-place.

        Parameters
        ----------
        direction : int
            One of LEFT, RIGHT, UP, DOWN.
        spawn : bool
            Whether to spawn a new tile after a valid move.

        Returns
        -------
        changed : bool
            True if the board state changed.
        score_gained : int
            Score gained by merges in this move.
        """
        original = self.grid.copy()
        score_gained = 0

        # UP/DOWN: transpose -> apply as LEFT/RIGHT -> transpose back
        if direction in (UP, DOWN):
            self.grid = self.grid.T.copy()
            row_direction = LEFT if direction == UP else RIGHT
        else:
            row_direction = direction

        # Apply move row by row
        for i in range(4):
            new_row, row_score = self._apply_move_to_row(self.grid[i], row_direction)
            self.grid[i] = new_row
            score_gained += row_score

        # Transpose back after UP/DOWN
        if direction in (UP, DOWN):
            self.grid = self.grid.T.copy()

        changed = not np.array_equal(self.grid, original)

        if changed:
            self.score += score_gained
            if spawn:
                self._spawn_tile()

        return changed, score_gained

    def move(self, direction: int) -> tuple[bool, int]:
        """
        Public move interface. Invalid moves are silently ignored.

        Parameters
        ----------
        direction : int
            One of LEFT (0), RIGHT (1), UP (2), DOWN (3).

        Returns
        -------
        changed : bool
            True if the board changed (move was valid).
        score_gained : int
            Score gained by merges in this move (0 if move was invalid).
        """
        return self._apply_move(direction, spawn=True)

    def is_won(self) -> bool:
        """Return True if any tile has reached the winning exponent (64)."""
        return bool(np.any(self.grid >= WIN_EXPONENT))

    def is_game_over(self) -> bool:
        """
        Return True if no valid move exists in any direction.
        The board is full and no adjacent tiles can merge.
        """
        if np.any(self.grid == 0):
            return False
        for direction in (LEFT, RIGHT, UP, DOWN):
            if self.is_move_valid(direction):
                return False
        return True

    def tile_values(self) -> np.ndarray:
        """Return the board as actual tile values (2^exponent, 0 for empty)."""
        result = np.zeros((4, 4), dtype=np.int32)
        mask = self.grid > 0
        result[mask] = 2 ** self.grid[mask].astype(np.int32)
        return result

    def empty_count(self) -> int:
        """Return the number of empty cells."""
        return int(np.sum(self.grid == 0))

    def max_tile(self) -> int:
        """Return the highest tile value currently on the board."""
        exp = int(np.max(self.grid))
        return 2 ** exp if exp > 0 else 0

    def copy(self) -> Board:
        """Return a deep copy of this board (same rng state)."""
        new = Board.__new__(Board)
        new.grid = self.grid.copy()
        new.score = self.score
        new.rng = self.rng
        return new

    def __repr__(self) -> str:
        values = self.tile_values()
        rows = []
        for row in values:
            rows.append(" ".join(f"{v:5d}" for v in row))
        return f"Board(score={self.score})\n" + "\n".join(rows)

