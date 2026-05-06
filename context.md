# 2048-RL — Project Context

## Goal
Implement a 2048-playing agent using Temporal Difference Learning with N-tuple networks.
This is a learning project focused on understanding RL, not just getting results.

## Game variant
- Standard 4x4 board
- Winning tile: **64** (to speed up training in early experiments)
- Tile spawning: original rules — tile 2 (90%) or tile 4 (10%) on a random empty cell
- Invalid moves: silently ignored (no penalty, no error)
- Tile values stored as **exponents of 2** (int8): 0=empty, 1=tile2, 2=tile4, ..., 6=tile64

## Architecture decisions

### Tile representation
Exponents of 2 in a numpy int8 array. Merging = exponent + 1. Compact and fast.

### Move lookup table (naive version first)
Row moves precomputed at startup into a dict:
  key   : tuple of 4 exponents
  value : {"left": RowResult, "right": RowResult}
  RowResult = (new_row_tuple, score_gained)
UP/DOWN handled by transposing the board and reusing LEFT/RIGHT.
LUT covers exponents 0–7 (8^4 = 4096 entries).

### RL algorithm: TD-Learning + N-tuple networks
State of the art for 2048 (see: arxiv 2212.11087).
- No neural network needed
- N-tuples = groups of N board cells (e.g. rows, columns, 2x2 squares)
- Each tuple has its own weight table, indexed by tile exponent combinations
- Value of a state = sum of weights across all tuples
- TD update: weights adjusted after each move based on reward + discounted next value

### Symmetries
The 2048 board has 8 symmetries (D4 group: 4 rotations x 2 reflections).
Can reduce effective state space by up to 8x.
To implement after baseline is working.

### Language
Python with numpy. No deep learning framework needed for N-tuple TD.
Potential future optimization: port hot loop (move application) to C extension.

## Project structure
```
2048-rl/
├── core/
│   ├── __init__.py
│   ├── board.py          # Board class, moves, game state
│   └── moves_lut.py      # Naive row-move lookup table
├── agent/
│   ├── __init__.py
│   ├── base.py           # Abstract Agent interface
│   ├── random.py         # Random baseline agent
│   └── td_ntuple.py      # TD-Learning + N-tuple agent (to build)
├── training/
│   ├── __init__.py
│   ├── trainer.py        # Training loop
│   └── evaluator.py      # Periodic evaluation
├── config/
│   └── default.yaml      # Hyperparameters
├── experiments/
│   └── runs/             # Checkpoints, metrics
├── tests/
│   ├── __init__.py
│   └── test_board.py     # Exhaustive board/LUT tests (pytest)
├── CONTEXT.md            # This file
└── pyproject.toml
```

## Files already implemented
- `core/moves_lut.py` — complete, tested
- `core/board.py` — complete, tested
- `tests/test_board.py` — 40+ tests, all passing

## Next steps
1. `agent/base.py` — abstract Agent interface
2. `agent/random.py` — random baseline (sanity check)
3. `agent/td_ntuple.py` — TD-Learning + N-tuple networks
4. `training/trainer.py` — training loop
5. `training/evaluator.py` — metrics (avg score, % reaching tile 64)

## Key references
- arxiv 2212.11087 — "On Reinforcement Learning for the Game of 2048" (Hung Guei)
  → Optimistic TD learning + N-tuple networks = current SOTA for learning-based agents

## Developer profile
- 10 years Python / data engineering (Airflow, Databricks, Delta Lake, Azure)
- Strong math background
- Learning RL — explain concepts when introducing new ones
- Write all code comments in English
- Ask clarifying questions before implementing anything non-trivial
```
