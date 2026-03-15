# 2048-AI

Implémentations d'intelligences artificielles pour jouer au jeu 2048, avec plusieurs approches allant du hasard pur à l'apprentissage par renforcement.

---

## Architecture

```
2048-AI/
├── GameGrids/            # Logique du jeu
│   ├── baseGrid2048.py   # Classe de base (mouvements, fusions, symétries)
│   ├── GameGridLight.py  # Grille légère pour les simulations (valeurs 2, 4, 8...)
│   └── LogGameGrid.py    # Représentation log₂ pour le Q-learning (valeurs 1, 2, 3...)
├── AI/                   # Algorithmes d'IA
│   ├── ai_random.py
│   ├── ai_bestScoreNextMove.py
│   ├── ai_MC.py
│   ├── ai_parallelMC.py
│   ├── ai_minimax.py
│   ├── ai_expectimax.py
│   ├── ai_q_learning.py
│   ├── ai_TDlearning.py  # Incomplet
│   └── Models/
│       ├── qvalue_container.py   # Stockage des Q-values avec réduction par symétrie
│       └── simulationNode.py     # Nœuds pour les simulations Monte Carlo
├── GUI/                  # Interface graphique Tkinter
├── UnitTests/            # Tests unitaires
├── game.py               # Lancement de l'interface graphique
├── play_2048.py          # Script d'entraînement Q-learning
├── play_console.py       # Jeu en mode console (Parallel MC)
├── features_selection.py # Analyse ML post-jeu (PCA, SVM, régression logistique)
└── constants.py          # Configuration (taille grille, valeur max)
```

---

## Algorithmes d'IA

### Résultats comparatifs

| Algorithme | Fichier | Score moyen | Statut |
|---|---|---|---|
| Random | `ai_random.py` | ~200 pts | Fonctionnel |
| Best Next Move (greedy 1 coup) | `ai_bestScoreNextMove.py` | ~500 pts | Fonctionnel |
| Monte Carlo (1000 sims, profondeur 6) | `ai_MC.py` | ~70 000 pts | Fonctionnel |
| Parallel Monte Carlo (4 processus) | `ai_parallelMC.py` | ~70 000 pts | Fonctionnel |
| Minimax (adversarial, depth=2) | `ai_minimax.py` | > 120 000 pts | Fonctionnel |
| Expectimax (probabiliste, depth=3) | `ai_expectimax.py` | > 120 000 pts | Fonctionnel |
| Q-Learning | `ai_q_learning.py` | En cours | Partiellement fonctionnel |
| TD-Learning | `ai_TDlearning.py` | — | **Non fonctionnel** |

### Description des approches

**Heuristiques simples**
- **Random** : sélection aléatoire parmi les 4 directions. Sert de référence basse.
- **Best Next Move** : évalue le score immédiat de chaque coup et choisit le meilleur. Greedy sur 1 coup.

**Recherche arborescente**
- **Monte Carlo** : simule N parties aléatoires depuis l'état courant pour chaque direction, et choisit celle avec le meilleur score moyen. Version parallélisée avec `multiprocessing`.
- **Minimax** : modélise la pose de tuiles adversariale (pire cas). Complexité exponentielle, limité à depth=2.
- **Expectimax** : variante probabiliste du Minimax — moyenne les placements de tuiles au lieu de les minimiser. Mieux adapté au caractère stochastique du jeu.

**Apprentissage par renforcement**
- **Q-Learning** : table de Q-values entraînée par épisodes (α=0.5, γ=1.0, ε=0.2). L'espace d'états est compressé via 8 symétries (rotations + retournements). Les Q-values sont sauvegardées/rechargées en CSV.
- **TD-Learning** : non finalisé, voir section "Bugs connus".

---

## Optimisation : symétries

Le moteur de jeu implémente 8 transformations géométriques (retournements selon x et y, rotations à 90°/180°/270°) qui permettent de mapper tout état vers un état canonique "minimal". Cela réduit l'espace d'états d'un facteur 8, ce qui est particulièrement utile pour le Q-learning.

---

## Analyse ML (`features_selection.py`)

Après enregistrement des parties (`RECORD_MOVES = True` dans `constants.py`), ce module permet :
- **PCA** : réduction de dimensionnalité sur les états de jeu
- **SVM / Régression logistique** : classification des meilleurs coups selon les features extraites (position, entropie, barycentre)
- Validation croisée K-Fold

---

## Lancement

```bash
# Interface graphique avec IA
python game.py

# Entraînement Q-learning
python play_2048.py

# Mode console (Parallel MC)
python play_console.py
```

### Configuration (`constants.py`)

```python
NB_ROWS = 2          # Hauteur de la grille (4 pour le vrai 2048)
NB_COLS = 2          # Largeur de la grille (4 pour le vrai 2048)
GRID_MAX_VAL = 5     # Valeur max en log₂ : 2^5 = 32 (11 pour le vrai 2048)
RECORD_MOVES = False # Enregistrer les coups dans moves_history.csv
```

> **Note** : la configuration par défaut est en grille 2×2 pour les tests et l'entraînement rapide du Q-learning. Pour le vrai jeu 4×4, modifier `NB_ROWS=4`, `NB_COLS=4`, `GRID_MAX_VAL=11`.

---

## Tests

```bash
python -m unittest discover UnitTests/
```

- `UnitTests/GameGrid/GameGridLight_Test.py` — tests complets des mécaniques de jeu (825 lignes, ~30 scénarios)
- `UnitTests/AI/q_learning_Test.py` — tests de la mise à jour des Q-values
- `UnitTests/simulationNode_Test.py` — tests des nœuds Monte Carlo

---

## Bugs connus à corriger

1. **`AI/ai_TDlearning.py` (lignes 68–92)** — Implémentation abandonnée. Erreurs : appel à `self.GetState()` inexistant, variables mal nommées (`s_prime`). À réécrire ou supprimer.

2. **`AI/Models/simulationNode.py` (~ligne 101)** — Bug dans `getMaxMove()` : le `best_score` n'est pas mis à jour pour la direction `"down"`, seul `best_move` l'est.

3. **`play_console.py`** — La méthode `saveScores()` est incomplète. `DataFrame(np.array([N, 17]))` a une syntaxe incorrecte (manque le paramètre `columns`).

4. **`GameGrids/GameGridLight.py`** — Code inaccessible après un `return` dans la propriété `max_value` (double définition).

---

## Améliorations possibles

- Implémenter Alpha-Beta pruning pour Minimax
- Utiliser UCB/UCT (bandit algorithms) pour les simulations Monte Carlo
- Réécrire les parties critiques en C++ ou Cython pour accélérer les simulations MC
- Finaliser le TD-Learning
- Entraîner le Q-learning sur grille 4×4 (nécessite une compression d'état plus agressive, ex. n-tuple networks)
