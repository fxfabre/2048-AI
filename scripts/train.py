"""
Training entry point for 2048-RL.

Usage
-----
    # Basic (uses config/default.yaml)
    python scripts/train.py

    # Custom run
    python scripts/train.py --episodes 50000 --alpha 0.05 --run-id my_run

    # Resume from checkpoint
    python scripts/train.py --checkpoint experiments/runs/my_run/checkpoint_10000.npz

Options
-------
    --run-id        Name for this run. Default: timestamp-based.
    --episodes      Number of training episodes. Default: 100 000.
    --alpha         Learning rate. Default: 0.1.
    --init-value    Initial weight value (0=pessimistic, >0=optimistic). Default: 0.
    --eval-interval Eval every N episodes. Default: 1 000.
    --eval-games    Games per evaluation. Default: 100.
    --checkpoint    Path to a .npz file to resume from.
    --seed          Master random seed. Default: 42.
"""

from __future__ import annotations

import argparse
import datetime
import pathlib
import sys

import numpy as np

# Allow running from project root: `python scripts/train.py`
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

from agent.td_ntuple import TDNTupleAgent
from training.evaluator import evaluate
from training.trainer import Trainer


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Train a TD N-tuple agent on 2048.")
    p.add_argument("--run-id", default=None,
                   help="Run identifier (used as output folder name).")
    p.add_argument("--episodes", type=int, default=100_000,
                   help="Total number of training episodes.")
    p.add_argument("--alpha", type=float, default=0.1,
                   help="TD learning rate.")
    p.add_argument("--init-value", type=float, default=0.0,
                   help="Initial weight value (0=pessimistic, >0=optimistic).")
    p.add_argument("--eval-interval", type=int, default=1_000,
                   help="Evaluate every N episodes.")
    p.add_argument("--eval-games", type=int, default=100,
                   help="Number of games per evaluation.")
    p.add_argument("--checkpoint-interval", type=int, default=10_000,
                   help="Save a checkpoint every N episodes.")
    p.add_argument("--checkpoint", default=None,
                   help="Path to a .npz checkpoint to resume training from.")
    p.add_argument("--seed", type=int, default=42,
                   help="Master random seed.")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    # ------------------------------------------------------------------ #
    # Output directory                                                     #
    # ------------------------------------------------------------------ #
    run_id = args.run_id or datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = pathlib.Path("experiments/runs") / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"Run directory : {run_dir}")

    # ------------------------------------------------------------------ #
    # Agent                                                                #
    # ------------------------------------------------------------------ #
    if args.checkpoint:
        ckpt_path = pathlib.Path(args.checkpoint)
        print(f"Resuming from checkpoint: {ckpt_path}")
        agent = TDNTupleAgent.load(ckpt_path, alpha=args.alpha)
    else:
        agent = TDNTupleAgent(alpha=args.alpha, init_value=args.init_value)

    print(agent)
    print()

    # ------------------------------------------------------------------ #
    # Training loop (manual to add checkpoint saving)                     #
    # ------------------------------------------------------------------ #
    rng = np.random.default_rng(args.seed)
    trainer = Trainer(agent, rng=rng)

    all_scores: list[int] = []
    eval_rng = np.random.default_rng(0)   # fixed seed for reproducible evals

    print(f"{'Episode':>10}  {'Train avg':>10}  {'Eval avg':>10}  {'Win rate':>9}  {'Max tile':>9}")
    print("-" * 57)

    for ep in range(args.episodes):
        ep_rng = np.random.default_rng(rng.integers(2**31))
        result = trainer.run_episode(rng=ep_rng)
        all_scores.append(result.score)

        # Periodic evaluation
        if (ep + 1) % args.eval_interval == 0:
            eval_result = evaluate(
                agent,
                n_games=args.eval_games,
                rng=np.random.default_rng(ep),
                learn=False,
            )
            recent = all_scores[-args.eval_interval:]
            train_avg = sum(recent) / len(recent)
            print(
                f"{ep + 1:>10d}  "
                f"{train_avg:>10.0f}  "
                f"{eval_result.mean_score:>10.0f}  "
                f"{eval_result.win_rate:>8.1%}  "
                f"{eval_result.max_tile_ever:>9d}"
            )

        # Periodic checkpoint
        if (ep + 1) % args.checkpoint_interval == 0:
            ckpt_path = run_dir / f"checkpoint_{ep + 1}.npz"
            agent.save(ckpt_path)

    # ------------------------------------------------------------------ #
    # Final save                                                           #
    # ------------------------------------------------------------------ #
    final_path = run_dir / "weights_final.npz"
    agent.save(final_path)
    print()
    print(f"Training complete. Final weights saved to: {final_path}")

    # Final evaluation
    print("\nFinal evaluation over 500 games:")
    final_eval = evaluate(agent, n_games=500, rng=np.random.default_rng(999), learn=False)
    print(final_eval)


if __name__ == "__main__":
    main()
