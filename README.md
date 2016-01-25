# 2048-AI
Play game 2048 with an "artificial intelligence"

IA created :
- Random move. Average score : ~200 pts
- Maximize score at next move. Average score : ~500 pts
- Monte carlo simulations, with parallel simulations. 5000 simulation, 6 nodes deep : up to 70.000 pts
- Minimax : max > 120.000 pts

Next steps :
- Use C++ / Cython to accelelerate MC simulations
- Add Alpha–beta pruning to minimax algo
- Use bandit algorithms for MC simulations : UCB, UCT
- Machine learning
- Reinforcement learning : temporal differences learning
http://www.cse.unsw.edu.au/~cs9417ml/RL1/tdlearning.html

