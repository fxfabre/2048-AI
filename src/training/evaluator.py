"""
Evaluation utilities for trained 2048 agents.

evaluate() runs a fixed number of games with no weight updates and returns
summary statistics useful for comparing agents and tracking training progress.

Metrics collected
-----------------
mean_score      : average cumulative score across all games
std_score       : standard deviation of scores
max_score       : best single-game score
win_rate        : fraction of games where the winning tile (64) was reached
tile_distribution : histogram of max tiles achieved (e.g. {16: 0.3, 32: 0.5, 64: 0.2})
max_tile_ever   : highest tile seen across all games
mean_moves      : average number of moves per game
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from agent.base import Agent
from core.board import Board, WIN_EXPONENT
from training.trainer import Trainer


@dataclass
class EvalResult:
    """
    Aggregate statistics from an evaluation run.

    Attributes
    ----------
    mean_score : float
    std_score : float
    max_score : int
    win_rate : float
        Fraction of games where max tile >= 2^WIN_EXPONENT (= 64).
    tile_distribution : dict[int, float]
        Keys: max tile values (2, 4, 8, ...).  Values: fraction of games.
    max_tile_ever : int
        Absolute maximum tile seen across all games.
    mean_moves : float
    n_games : int
    """

    mean_score: float
    std_score: float
    max_score: int
    win_rate: float
    tile_distribution: dict[int, float]
    max_tile_ever: int
    mean_moves: float
    n_games: int
    all_scores: list[int] = field(default_factory=list)

    def __str__(self) -> str:
        tile_str = "  ".join(
            f"{tile}: {pct:.1%}"
            for tile, pct in sorted(self.tile_distribution.items())
        )
        return (
            f"EvalResult over {self.n_games} games\n"
            f"  score  : {self.mean_score:.0f} ± {self.std_score:.0f}  (max {self.max_score})\n"
            f"  win rate (≥{2**WIN_EXPONENT}) : {self.win_rate:.1%}\n"
            f"  max tile ever : {self.max_tile_ever}\n"
            f"  avg moves     : {self.mean_moves:.1f}\n"
            f"  tile dist : {tile_str}"
        )


def evaluate(
    agent: Agent,
    n_games: int = 100,
    rng: np.random.Generator | None = None,
    learn: bool = False,
) -> EvalResult:
    """
    Evaluate an agent over `n_games` complete games.

    Parameters
    ----------
    agent : Agent
        The agent to evaluate.  Its weights are NOT modified (learn=False).
    n_games : int
        Number of games to play.
    rng : np.random.Generator, optional
        Master RNG for reproducibility.  A new default generator is used if None.
    learn : bool
        If True, weight updates are applied during evaluation (useful for
        online training metrics).  Defaults to False (pure evaluation).

    Returns
    -------
    EvalResult
        Aggregated statistics across all games.
    """
    master_rng = rng if rng is not None else np.random.default_rng()

    scores: list[int] = []
    max_tiles: list[int] = []
    move_counts: list[int] = []

    if learn:
        # Reuse Trainer logic for consistent update semantics
        trainer = Trainer(agent, rng=master_rng)
        for _ in range(n_games):
            ep_rng = np.random.default_rng(master_rng.integers(2**31))
            result = trainer.run_episode(rng=ep_rng)
            scores.append(result.score)
            max_tiles.append(result.max_tile)
            move_counts.append(result.n_moves)
    else:
        # Pure play-out: no TD updates (agent.update is not called)
        for i in range(n_games):
            board = Board(rng=np.random.default_rng(master_rng.integers(2**31)))
            n_moves = 0
            while not board.is_game_over() and not board.is_won():
                action = agent.select_action(board)
                board.move(action)
                n_moves += 1
            scores.append(board.score)
            max_tiles.append(board.max_tile())
            move_counts.append(n_moves)

    # Aggregate
    scores_arr = np.array(scores, dtype=np.float64)
    max_tiles_arr = np.array(max_tiles)

    # Tile distribution: fraction of games ending with each max-tile value
    unique_tiles, counts = np.unique(max_tiles_arr, return_counts=True)
    tile_distribution = {int(t): int(c) / n_games for t, c in zip(unique_tiles, counts)}

    win_threshold = 2 ** WIN_EXPONENT
    win_rate = float(np.mean(max_tiles_arr >= win_threshold))

    return EvalResult(
        mean_score=float(np.mean(scores_arr)),
        std_score=float(np.std(scores_arr)),
        max_score=int(np.max(scores_arr)),
        win_rate=win_rate,
        tile_distribution=tile_distribution,
        max_tile_ever=int(np.max(max_tiles_arr)),
        mean_moves=float(np.mean(move_counts)),
        n_games=n_games,
        all_scores=scores,
    )
