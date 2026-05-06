# 2048-RL

2048-playing agent using Temporal Difference Learning with N-tuple networks.

## Installation

```bash
pip install -e .
```

Requires Python 3.13. Uses numpy only — no deep learning framework needed.

## Project structure

```
2048-rl/
├── src/
│   ├── core/
│   │   ├── board.py          # Board class, moves, game state
│   │   └── moves_lut.py      # Row-move lookup table
│   ├── agent/
│   │   ├── base.py           # Abstract Agent interface
│   │   ├── random.py         # Random baseline agent
│   │   └── td_ntuple.py      # TD-Learning + N-tuple agent
│   └── training/
│       ├── trainer.py        # Training loop
│       └── evaluator.py      # Evaluation metrics
├── scripts/
│   ├── train.py              # Training entry point
│   └── play.py               # Play / evaluate entry point
├── config/
│   └── default.yaml          # Hyperparameters
├── experiments/
│   └── runs/                 # Checkpoints and metrics
└── tests/
    └── test_board.py
```

## Training

```bash
# Basic run (100 000 episodes, default hyperparameters)
python scripts/train.py

# Custom run
python scripts/train.py --episodes 50000 --alpha 0.05 --run-id my_run

# Resume from a checkpoint
python scripts/train.py --checkpoint experiments/runs/my_run/checkpoint_10000.npz
```

**Key options:**

| Option | Default | Description |
|---|---|---|
| `--run-id` | timestamp | Name of the output folder |
| `--episodes` | 100 000 | Number of training episodes |
| `--alpha` | 0.1 | TD learning rate |
| `--init-value` | 0.0 | Initial weight (0 = pessimistic, >0 = optimistic) |
| `--eval-interval` | 1 000 | Print stats every N episodes |
| `--checkpoint-interval` | 10 000 | Save weights every N episodes |
| `--seed` | 42 | Master random seed |

During training, a progress table is printed to the console:

```
   Episode   Train avg    Eval avg   Win rate   Max tile
---------------------------------------------------------
      1000         442         499     98.0%         64
      2000         516         535     96.0%         64
      3000         549         539     94.0%         64
```

## Saved strategy

Learned weights are saved as `.npz` files (numpy format, ~256 KB each) in `experiments/runs/<run-id>/`:

```
experiments/runs/my_run/
├── checkpoint_10000.npz    # intermediate checkpoint
├── checkpoint_20000.npz
└── weights_final.npz       # final weights after training
```

Each file contains the weight tables of the 8 N-tuples (4 rows + 4 columns of the board).

## Playing with a trained strategy

```bash
# Watch one game step by step (ASCII board)
python scripts/play.py --weights experiments/runs/my_run/weights_final.npz

# Slow down the display (seconds between moves)
python scripts/play.py --weights experiments/runs/my_run/weights_final.npz --delay 0.2

# Run 200 games silently, then print statistics
python scripts/play.py --weights experiments/runs/my_run/weights_final.npz --games 200

# Compare with the random baseline
python scripts/play.py --random --games 200
```

The statistics output looks like:

```
EvalResult over 200 games
  score  : 550 ± 110  (max 916)
  win rate (≥64) : 91.8%
  max tile ever : 64
  avg moves     : 70.4
  tile dist : 32: 8.2%  64: 91.8%
```

## Running tests

```bash
pytest
```

## How it works

The agent uses **N-tuple networks** — a lightweight alternative to neural networks well-suited to 2048 (Szubert & Jaskowski 2014; Guei et al. 2022, arxiv:2212.11087).

The board is divided into 8 groups of 4 cells (the 4 rows and 4 columns). Each group has its own weight lookup table indexed by the tile exponents of its cells. The state value is the sum of all active table entries.

Training uses **TD(0) with after-states**: after each move (before tile spawning), the agent updates its value estimate using the best achievable value from the resulting state as the TD target.
