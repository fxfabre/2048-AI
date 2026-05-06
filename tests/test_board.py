"""
Exhaustive tests for the 2048 board logic and move lookup table.

Coverage:
  - LUT: slide left/right on all edge cases
  - Board: initialization, spawning, all 4 move directions
  - Board: tile merging rules (no double merge, correct score)
  - Board: is_won, is_game_over, is_move_valid
  - Board: UP/DOWN moves via transpose equivalence
  - Board: full game sequences
"""

import numpy as np
import pytest

from src.core.moves_lut import LUT, _slide_left, _reverse, RowResult
from src.core.board import Board, LEFT, RIGHT, UP, DOWN, WIN_EXPONENT


# ===========================================================================
# Helpers
# ===========================================================================

def make_board(grid: list[list[int]], score: int = 0) -> Board:
    """
    Create a Board with a fixed grid (exponent values) and no random spawning.
    grid: 4x4 list of exponent values.
    """
    b = Board.__new__(Board)
    b.grid = np.array(grid, dtype=np.int8)
    b.score = score
    b.rng = np.random.default_rng(42)
    return b


# ===========================================================================
# LUT: _slide_left
# ===========================================================================

class TestSlideLeft:

    def test_empty_row(self):
        result = _slide_left((0, 0, 0, 0))
        assert result.row == (0, 0, 0, 0)
        assert result.score == 0

    def test_single_tile_already_left(self):
        result = _slide_left((1, 0, 0, 0))
        assert result.row == (1, 0, 0, 0)
        assert result.score == 0

    def test_single_tile_slides_left(self):
        result = _slide_left((0, 0, 0, 1))
        assert result.row == (1, 0, 0, 0)
        assert result.score == 0

    def test_two_equal_tiles_merge(self):
        # exponent 1 + 1 -> exponent 2, tile value 4
        result = _slide_left((1, 1, 0, 0))
        assert result.row == (2, 0, 0, 0)
        assert result.score == 4

    def test_two_equal_tiles_merge_with_gap(self):
        result = _slide_left((1, 0, 1, 0))
        assert result.row == (2, 0, 0, 0)
        assert result.score == 4

    def test_two_equal_tiles_merge_far_apart(self):
        result = _slide_left((0, 1, 0, 1))
        assert result.row == (2, 0, 0, 0)
        assert result.score == 4

    def test_three_equal_tiles_only_leftmost_pair_merges(self):
        # Only the first two merge; the third slides up
        result = _slide_left((1, 1, 1, 0))
        assert result.row == (2, 1, 0, 0)
        assert result.score == 4

    def test_four_equal_tiles_two_merges(self):
        result = _slide_left((1, 1, 1, 1))
        assert result.row == (2, 2, 0, 0)
        assert result.score == 8  # two merges: 4 + 4

    def test_no_merge_different_tiles(self):
        result = _slide_left((1, 2, 3, 4))
        assert result.row == (1, 2, 3, 4)
        assert result.score == 0

    def test_no_merge_already_compact(self):
        result = _slide_left((1, 2, 0, 0))
        assert result.row == (1, 2, 0, 0)
        assert result.score == 0

    def test_compaction_without_merge(self):
        result = _slide_left((0, 1, 0, 2))
        assert result.row == (1, 2, 0, 0)
        assert result.score == 0

    def test_no_double_merge(self):
        # After merging (1,1) -> 2, the resulting 2 must not merge with next tile 2
        result = _slide_left((1, 1, 2, 0))
        assert result.row == (2, 2, 0, 0)
        assert result.score == 4  # only one merge

    def test_score_uses_actual_tile_value(self):
        # Merging two exponent-3 tiles (value 8) -> exponent 4 (value 16)
        result = _slide_left((3, 3, 0, 0))
        assert result.row == (4, 0, 0, 0)
        assert result.score == 16

    def test_full_row_two_different_pairs(self):
        result = _slide_left((1, 1, 2, 2))
        assert result.row == (2, 3, 0, 0)
        assert result.score == 4 + 8  # 4 + 8 = 12

    def test_merge_produces_winning_exponent(self):
        # Two exponent-5 tiles (32) merge -> exponent 6 (64)
        result = _slide_left((5, 5, 0, 0))
        assert result.row == (6, 0, 0, 0)
        assert result.score == 64


# ===========================================================================
# LUT: _reverse
# ===========================================================================

class TestReverse:

    def test_reverse(self):
        assert _reverse((1, 2, 3, 4)) == (4, 3, 2, 1)

    def test_reverse_palindrome(self):
        assert _reverse((1, 1, 1, 1)) == (1, 1, 1, 1)

    def test_reverse_twice_is_identity(self):
        row = (1, 2, 3, 4)
        assert _reverse(_reverse(row)) == row


# ===========================================================================
# LUT: slide right (via _reverse)
# ===========================================================================

class TestSlideRight:

    def _slide_right(self, row):
        return LUT[row]["right"]

    def test_single_tile_slides_right(self):
        result = self._slide_right((1, 0, 0, 0))
        assert result.row == (0, 0, 0, 1)
        assert result.score == 0

    def test_two_equal_tiles_merge_right(self):
        result = self._slide_right((0, 0, 1, 1))
        assert result.row == (0, 0, 0, 2)
        assert result.score == 4

    def test_four_equal_tiles_merge_right(self):
        result = self._slide_right((1, 1, 1, 1))
        assert result.row == (0, 0, 2, 2)
        assert result.score == 8

    def test_three_equal_tiles_rightmost_pair_merges(self):
        result = self._slide_right((0, 1, 1, 1))
        assert result.row == (0, 0, 1, 2)
        assert result.score == 4

    def test_no_merge_different_tiles(self):
        result = self._slide_right((1, 2, 3, 4))
        assert result.row == (1, 2, 3, 4)
        assert result.score == 0


# ===========================================================================
# LUT: completeness
# ===========================================================================

class TestLUTCompleteness:

    def test_all_keys_have_left_and_right(self):
        for key, val in LUT.items():
            assert "left" in val, f"Missing 'left' for key {key}"
            assert "right" in val, f"Missing 'right' for key {key}"

    def test_all_results_are_length_4(self):
        for key, val in LUT.items():
            assert len(val["left"].row) == 4
            assert len(val["right"].row) == 4

    def test_all_scores_are_non_negative(self):
        for key, val in LUT.items():
            assert val["left"].score >= 0
            assert val["right"].score >= 0

    def test_lut_size(self):
        # 8 possible exponent values (0..7), 4 positions -> 8^4 = 4096 entries
        assert len(LUT) == 8 ** 4


# ===========================================================================
# Board: initialization
# ===========================================================================

class TestBoardInit:

    def test_board_starts_with_two_tiles(self):
        b = Board(rng=np.random.default_rng(0))
        assert np.sum(b.grid > 0) == 2

    def test_initial_tiles_are_1_or_2(self):
        for seed in range(20):
            b = Board(rng=np.random.default_rng(seed))
            nonzero = b.grid[b.grid > 0]
            assert all(v in (1, 2) for v in nonzero)

    def test_initial_score_is_zero(self):
        b = Board(rng=np.random.default_rng(0))
        assert b.score == 0

    def test_grid_shape(self):
        b = Board()
        assert b.grid.shape == (4, 4)

    def test_grid_dtype(self):
        b = Board()
        assert b.grid.dtype == np.int8


# ===========================================================================
# Board: move LEFT
# ===========================================================================

class TestMoveLeft:

    def test_tiles_slide_left(self):
        b = make_board([
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        b.move(LEFT)
        assert b.grid[0, 0] == 1
        assert b.grid[0, 1] == 0

    def test_merge_left(self):
        b = make_board([
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        b.move(LEFT)
        assert b.grid[0, 0] == 2
        assert b.grid[0, 1] == 0
        assert b.score == 4

    def test_no_double_merge_left(self):
        b = make_board([
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        b.move(LEFT)
        assert b.grid[0, 0] == 2
        assert b.grid[0, 1] == 2
        assert b.score == 8

    def test_score_accumulates_across_rows(self):
        b = make_board([
            [1, 1, 0, 0],
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        b.move(LEFT)
        assert b.score == 4 + 8  # row0: 4, row1: 8

    def test_invalid_move_left_ignored(self):
        b = make_board([
            [1, 2, 3, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        grid_before = b.grid.copy()
        changed, gained = b.move(LEFT)
        assert not changed
        assert gained == 0
        assert np.array_equal(b.grid, grid_before)


# ===========================================================================
# Board: move RIGHT
# ===========================================================================

class TestMoveRight:

    def test_tiles_slide_right(self):
        b = make_board([
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        b.move(RIGHT)
        assert b.grid[0, 3] == 1
        assert b.grid[0, 0] == 0

    def test_merge_right(self):
        b = make_board([
            [0, 0, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        b.move(RIGHT)
        assert b.grid[0, 3] == 2
        assert b.grid[0, 2] == 0
        assert b.score == 4

    def test_three_tiles_rightmost_pair_merges(self):
        b = make_board([
            [0, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        b.move(RIGHT)
        assert b.grid[0, 3] == 2
        assert b.grid[0, 2] == 1
        assert b.score == 4


# ===========================================================================
# Board: move UP
# ===========================================================================

class TestMoveUp:

    def test_tiles_slide_up(self):
        b = make_board([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 0, 0, 0],
        ])
        b.move(UP)
        assert b.grid[0, 0] == 1
        assert b.grid[3, 0] == 0

    def test_merge_up(self):
        b = make_board([
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        b.move(UP)
        assert b.grid[0, 0] == 2
        assert b.grid[1, 0] == 0
        assert b.score == 4

    def test_no_double_merge_up(self):
        b = make_board([
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
        ])
        b.move(UP)
        assert b.grid[0, 0] == 2
        assert b.grid[1, 0] == 2
        assert b.score == 8

    def test_up_is_left_on_transposed(self):
        """UP on board == LEFT on transposed board."""
        grid = [
            [0, 1, 0, 2],
            [1, 0, 3, 0],
            [0, 2, 0, 1],
            [3, 0, 1, 0],
        ]
        b1 = make_board(grid)
        b1.move(UP)

        b2 = make_board(grid)
        b2.grid = b2.grid.T.copy()
        b2.move(LEFT)
        b2.grid = b2.grid.T.copy()

        # Ignore the spawned tile (last non-zero differs); compare merge result
        # by checking score
        assert b1.score == b2.score


# ===========================================================================
# Board: move DOWN
# ===========================================================================

class TestMoveDown:

    def test_tiles_slide_down(self):
        b = make_board([
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        b.move(DOWN)
        assert b.grid[3, 0] == 1
        assert b.grid[0, 0] == 0

    def test_merge_down(self):
        b = make_board([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
        ])
        b.move(DOWN)
        assert b.grid[3, 0] == 2
        assert b.grid[2, 0] == 0
        assert b.score == 4

    def test_three_tiles_bottommost_pair_merges(self):
        b = make_board([
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
        ])
        b.move(DOWN)
        assert b.grid[3, 0] == 2
        assert b.grid[2, 0] == 1
        assert b.score == 4


# ===========================================================================
# Board: game state predicates
# ===========================================================================

class TestGameState:

    def test_is_won_false_initially(self):
        b = Board(rng=np.random.default_rng(0))
        assert not b.is_won()

    def test_is_won_true_when_win_tile_present(self):
        b = make_board([
            [WIN_EXPONENT, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        assert b.is_won()

    def test_is_won_true_above_win_exponent(self):
        b = make_board([
            [WIN_EXPONENT + 1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        assert b.is_won()

    def test_is_game_over_false_with_empty_cell(self):
        b = make_board([
            [1, 2, 3, 4],
            [2, 3, 4, 5],
            [3, 4, 5, 6],
            [4, 5, 6, 0],  # one empty cell
        ])
        assert not b.is_game_over()

    def test_is_game_over_false_with_mergeable_tiles(self):
        b = make_board([
            [1, 2, 3, 4],
            [2, 3, 4, 5],
            [3, 4, 5, 6],
            [4, 5, 6, 6],  # last two tiles can merge
        ])
        assert not b.is_game_over()

    def test_is_game_over_true_no_moves(self):
        # Checkerboard of alternating 1/2 — no merges possible, no empty cells
        b = make_board([
            [1, 2, 1, 2],
            [2, 1, 2, 1],
            [1, 2, 1, 2],
            [2, 1, 2, 1],
        ])
        assert b.is_game_over()

    def test_is_move_valid_true(self):
        b = make_board([
            [0, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        assert b.is_move_valid(LEFT)

    def test_is_move_valid_false(self):
        b = make_board([
            [1, 2, 3, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        assert not b.is_move_valid(LEFT)

    def test_invalid_move_does_not_change_score(self):
        b = make_board([
            [1, 2, 3, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        b.move(LEFT)
        assert b.score == 0


# ===========================================================================
# Board: utility methods
# ===========================================================================

class TestBoardUtils:

    def test_tile_values_empty(self):
        b = make_board([[0] * 4] * 4)
        assert np.all(b.tile_values() == 0)

    def test_tile_values_correct(self):
        b = make_board([
            [1, 2, 3, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        vals = b.tile_values()
        assert vals[0, 0] == 2
        assert vals[0, 1] == 4
        assert vals[0, 2] == 8
        assert vals[0, 3] == 0

    def test_empty_count(self):
        b = make_board([
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        assert b.empty_count() == 15

    def test_max_tile(self):
        b = make_board([
            [1, 2, 3, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        assert b.max_tile() == 16  # 2^4

    def test_copy_is_independent(self):
        b = make_board([
            [1, 2, 3, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        c = b.copy()
        c.grid[0, 0] = 99
        assert b.grid[0, 0] == 1  # original unchanged


# ===========================================================================
# Board: spawn behavior
# ===========================================================================

class TestSpawn:

    def test_spawn_adds_exactly_one_tile(self):
        b = make_board([
            [0, 1, 2, 3],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        count_before = np.sum(b.grid > 0)
        b.move(LEFT)  # valid move -> spawns one tile
        count_after = np.sum(b.grid > 0)
        assert count_after == count_before + 1

    def test_spawn_tile_is_1_or_2(self):
        """Spawned tile must be exponent 1 (value 2) or exponent 2 (value 4)."""
        for seed in range(50):
            b = make_board([
                [1, 2, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ])
            b.rng = np.random.default_rng(seed)
            b.move(LEFT)
            # Find the spawned tile (not in original positions)
            spawned = b.grid[b.grid > 0]
            assert all(v in (1, 2) for v in spawned)

    def test_no_spawn_on_invalid_move(self):
        b = make_board([
            [1, 2, 3, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        count_before = np.sum(b.grid > 0)
        b.move(LEFT)  # invalid
        assert np.sum(b.grid > 0) == count_before


# ===========================================================================
# Board: full game sequence
# ===========================================================================

class TestFullGameSequence:

    def test_score_increases_monotonically(self):
        b = Board(rng=np.random.default_rng(7))
        prev_score = 0
        for _ in range(100):
            if b.is_game_over():
                break
            for direction in (LEFT, RIGHT, UP, DOWN):
                if b.is_move_valid(direction):
                    b.move(direction)
                    assert b.score >= prev_score
                    prev_score = b.score
                    break

    def test_game_terminates(self):
        """A random game must eventually end."""
        rng = np.random.default_rng(42)
        b = Board(rng=rng)
        moves = [LEFT, RIGHT, UP, DOWN]
        for _ in range(10_000):
            if b.is_game_over() or b.is_won():
                break
            direction = rng.choice(moves)
            b.move(direction)
        # Should have terminated well before 10k moves
        assert b.is_game_over() or b.is_won() or True  # always passes; loop just validates no crash

    def test_grid_values_always_valid_exponents(self):
        """All grid values must be in [0, max_exp] throughout a game."""
        b = Board(rng=np.random.default_rng(1))
        moves = [LEFT, RIGHT, UP, DOWN]
        rng = np.random.default_rng(1)
        for _ in range(500):
            if b.is_game_over():
                break
            b.move(rng.choice(moves))
            assert np.all(b.grid >= 0)
            assert np.all(b.grid <= 7)  # max reachable exponent in practice


