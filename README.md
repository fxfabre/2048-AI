# 2048-AI
Play game 2048 with an "artificial intelligence"

IA created :
- Random move. Average score : ~200 pts
- Maximize score at next move. Average score : ~500 pts
- Monte carlo simulations, with parallel simulations. 5000 simulation, 6 nodes deep : up to 70.000 pts
- Minimax : max > 120.000 pts
- Expectimax
- Reinforcement learning : Q-learning

Next steps :
- Use C++ / Cython to accelelerate MC simulations
- Add Alpha–beta pruning to minimax algo
- Use bandit algorithms for MC simulations : UCB, UCT
- Machine learning

