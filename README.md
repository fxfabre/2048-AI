# 2048-AI
Play game 2048 with an "artificial intelligence"

IA created :
- Random move. Average score : ~200 pts
- Maximize score at next move. Average score : ~500 pts
- Monte carlo simulations, with parallel simulations. 1000 simulation, 6 nodes deep : 32748 pts
- Minimax

Next steps :
- Use C++ / Cython to accelelerate MC simulations
- Add Alpha–beta pruning to minimax algo
- Use bandit algorithms for MC simulations : UCB, UCT
- Machine learning
- Reinforcement learning : temporal differences learning
http://www.cse.unsw.edu.au/~cs9417ml/RL1/tdlearning.html

