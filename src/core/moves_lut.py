"""
Naive lookup table for all possible row moves in 2048.

Each row is represented as a tuple of 4 integers (tile exponents).
Tile values are stored as exponents of 2:
  0  -> empty cell
  1  -> tile 2
  2  -> tile 4
  ...
  6  -> tile 64 (winning tile)

The table maps each row tuple to (result_row_tuple, score_gained).
Score gained = sum of merged tile values (in actual tile values, not exponents).

The table is built once at import time and reused for all moves.
"""

from typing import NamedTuple


class RowResult(NamedTuple):
    row: tuple  # resulting row as exponent tuple, length 4
    score: int  # score gained by merges in this move


def _slide_left(row: tuple) -> RowResult:
    """
    Slide and merge a single row to the left.
    Input/output: tuple of 4 tile exponents (0 = empty).
    Returns RowResult with the new row and the score gained.
    """
    # Step 1: remove empty cells (compact non-zero tiles to the left)
    tiles = [t for t in row if t != 0]

    score = 0

    # Step 2: merge adjacent equal tiles left to right
    merged = []
    skip = False
    for i in range(len(tiles)):
        if skip:
            skip = False
            continue
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            # Merge: exponent + 1, score += actual tile value after merge
            new_exp = tiles[i] + 1
            merged.append(new_exp)
            score += 2 ** new_exp
            skip = True
        else:
            merged.append(tiles[i])

    # Step 3: pad with zeros on the right to restore length 4
    merged += [0] * (4 - len(merged))

    return RowResult(row=tuple(merged), score=score)


def _reverse(row: tuple) -> tuple:
    """Reverse a row tuple."""
    return row[::-1]


def build_lut() -> dict:
    """
    Build the full lookup table for all possible rows.

    Keys: tuple of 4 tile exponents, each in range [0, 6] (0=empty, 6=tile 64)
    Values: dict with keys 'left', 'right', each a RowResult

    We only build left/right here; up/down are handled by transposing the board
    and reusing left/right.
    """
    lut = {}

    # All possible exponent values: 0 (empty) + exponents 1..6 (tiles 2..64)
    # We allow up to exponent 7 in the table to handle intermediate merge states
    # (e.g. two 64-tiles merging into 128), even if 128 is beyond the win condition.
    max_exp = 7
    values = range(max_exp + 1)

    for a in values:
        for b in values:
            for c in values:
                for d in values:
                    row = (a, b, c, d)
                    left = _slide_left(row)
                    right_input = _reverse(row)
                    right_slid = _slide_left(right_input)
                    right = RowResult(
                        row=_reverse(right_slid.row),
                        score=right_slid.score,
                    )
                    lut[row] = {"left": left, "right": right}

    return lut


# Build once at import time
LUT: dict = build_lut()

