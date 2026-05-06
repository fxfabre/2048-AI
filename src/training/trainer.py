"""
Training loop for 2048 RL agents.

Episode structure and TD update timing
---------------------------------------
The key subtlety is *when* to apply the TD update.  We use after-state TD,
which means V is defined over board states *before* tile spawning.

At each step t:
  1. Compute best_value(s_t) — this becomes the TD target for step t-1.
  2. Update V(as_{t-1}) with that target.
  3. Select and apply action a_t (including tile spawn → s_{t+1}).
  4. Store as_t (the state after the move, before the spawn).

At game end:
  5. Update V(as_last) with target = 0.0 (terminal has no future reward).

Step 1 happens at the *start* of iteration t, which is why the update is
"one step delayed" — we need to observe the best value from the *next* state
before we can update the *current* after-state.  This is the standard
after-state TD(0) scheme.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

import numpy as np

from agent.base import Agent
from core.board import Board


@dataclass
class EpisodeResult:
    """Summary statistics for a single episode."""

    score: int
    max_tile: int
    n_moves: int


@dataclass
class TrainingStats:
    """Aggregated statistics collected during training."""

    scores: list[int] = field(default_factory=list)
    max_tiles: list[int] = field(default_factory=list)
    n_moves: list[int] = field(default_factory=list)
    eval_scores: list[float] = field(default_factory=list)  # mean score at each eval
    eval_episodes: list[int] = field(default_factory=list)  # episode index of each eval


class Trainer:
    """
    Runs training episodes for a given agent.

    Parameters
    ----------
    agent : Agent
        The agent to train.  Must implement select_action, best_value, update.
    rng : np.random.Generator, optional
        Master RNG.  Each episode gets its own derived seed for reproducibility.
    """

    def __init__(
        self,
        agent: Agent,
        rng: np.random.Generator | None = None,
    ) -> None:
        self.agent = agent
        self.rng: np.random.Generator = rng if rng is not None else np.random.default_rng()

    # ------------------------------------------------------------------
    # Single episode
    # ------------------------------------------------------------------

    def run_episode(self, rng: np.random.Generator | None = None) -> EpisodeResult:
        """
        Play one complete game and apply TD updates after every move.

        Parameters
        ----------
        rng : np.random.Generator, optional
            RNG for this episode (tile spawning).  Defaults to self.rng.

        Returns
        -------
        EpisodeResult
            Score, max tile, and number of moves for the finished game.
        """
        board = Board(rng=rng if rng is not None else self.rng)

        # prev_after_state: the board state produced by the last move,
        # *before* the tile was spawned.  We need it to apply the TD update.
        prev_after_state: Board | None = None
        n_moves = 0

        while not board.is_game_over() and not board.is_won():
            # Step 1: compute TD target for the *previous* after-state.
            # best_value(board) = max_a [r(a) + V(after_state(board, a))]
            # This represents the best achievable value from the current state,
            # which is exactly what the previous after-state should have predicted.
            target = self.agent.best_value(board)

            # Step 2: update previous after-state's value.
            if prev_after_state is not None:
                self.agent.update(prev_after_state, target)

            # Step 3: select action and capture the after-state (no spawn yet).
            action = self.agent.select_action(board)
            after_state = board.copy()
            after_state._apply_move(action, spawn=False)  # deterministic after-state

            # Step 4: apply the move for real (spawns a new tile → next state).
            board.move(action)
            n_moves += 1

            prev_after_state = after_state

        # Terminal update: the last after-state has no future reward.
        if prev_after_state is not None:
            self.agent.update(prev_after_state, 0.0)

        return EpisodeResult(
            score=board.score,
            max_tile=board.max_tile(),
            n_moves=n_moves,
        )

    # ------------------------------------------------------------------
    # Training loop
    # ------------------------------------------------------------------

    def train(
        self,
        n_episodes: int,
        eval_interval: int = 1000,
        eval_games: int = 100,
        verbose: bool = True,
    ) -> TrainingStats:
        """
        Run `n_episodes` training episodes with periodic evaluation.

        Parameters
        ----------
        n_episodes : int
            Total number of training episodes.
        eval_interval : int
            Every `eval_interval` episodes, evaluate the agent on `eval_games`
            games without learning updates and print a summary.
        eval_games : int
            Number of games per evaluation window.
        verbose : bool
            Print progress to stdout.

        Returns
        -------
        TrainingStats
            All episode scores / max-tiles / move counts and eval snapshots.
        """
        from training.evaluator import evaluate  # local import to avoid circular

        stats = TrainingStats()
        t0 = time.perf_counter()

        for ep in range(n_episodes):
            # Use a fresh seeded RNG per episode for reproducibility.
            ep_rng = np.random.default_rng(self.rng.integers(2**31))
            result = self.run_episode(rng=ep_rng)

            stats.scores.append(result.score)
            stats.max_tiles.append(result.max_tile)
            stats.n_moves.append(result.n_moves)

            # Periodic evaluation
            if (ep + 1) % eval_interval == 0:
                eval_result = evaluate(
                    self.agent,
                    n_games=eval_games,
                    rng=np.random.default_rng(ep),  # fixed seed for comparability
                    learn=False,
                )
                stats.eval_scores.append(eval_result.mean_score)
                stats.eval_episodes.append(ep + 1)

                if verbose:
                    elapsed = time.perf_counter() - t0
                    recent_scores = stats.scores[-eval_interval:]
                    print(
                        f"[ep {ep + 1:>7d}/{n_episodes}] "
                        f"train_avg={sum(recent_scores)/len(recent_scores):>8.0f}  "
                        f"eval_avg={eval_result.mean_score:>8.0f}  "
                        f"win_rate={eval_result.win_rate:>5.1%}  "
                        f"max_tile={eval_result.max_tile_ever:>4d}  "
                        f"t={elapsed:>6.1f}s"
                    )

        return stats
