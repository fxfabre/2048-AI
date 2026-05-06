"""
Play 2048 without any UI
Display game grid on the console
"""

import numpy as np
import pandas as pd

from src.AI.ai_parallelMC import ai_parallelMC
from src.GameGrids.LogGameGrid import GameGrid2048


class ConsoleAutoPlay:
    def __init__(self):
        self._scoreHistory = []
        self._gridHistory = []
        self.totalScore = 0
        self._ai = ai_parallelMC()
        self.grid = None

    def playGame(self):
        self.grid = GameGrid2048(nb_rows=3, nb_columns=3)
        self.grid.add_random_tile()
        self.grid.add_random_tile()

        i = 0
        nextMove = "up"
        nb_iter_without_moving = 0
        while nb_iter_without_moving == 0:
            i += 1

            # # Add history (grid and score) data
            # self._scoreHistory.append( self.totalScore )
            # self._gridHistory.append( self.grid.matrix )
            # self._actionHistory ?

            # Get next move : 'left', 'right', 'up' or 'down'
            nextMove = self._ai.move_next(self, self._gridHistory, self._scoreHistory)

            if len(nextMove) == 0:
                print("null direction")
                print(self.grid)
                nb_iter_without_moving += 1
                continue

            score, has_moved = self.grid.moveTo(nextMove)
            self.grid.add_random_tile()
            score -= self.totalScore
            self.totalScore += score
            print(f"Move {nextMove:<5}, add score {score:>5}, total score {self.totalScore:>5}")

            if not has_moved:
                print("did not moved")
                nb_iter_without_moving += 1
            print(self.grid)

        print(f"Game over in {i + 1} iterations, score = {self.totalScore}")

    def saveScores(self):
        N = len(self._scoreHistory)
        datasToStore = pd.DataFrame(np.array([N, 17]))

        datasToStore[:][0] = self._scoreHistory


if __name__ == "__main__":
    game = ConsoleAutoPlay()
    game.playGame()
