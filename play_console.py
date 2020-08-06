#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
from pandas import DataFrame

from AI.ai_parallelMC import ai_parallelMC
from GameGrids.LogGameGrid import GameGrid2048


class consoleAutoPlay:

    def __init__(self):
        self._scoreHistory = []
        self._gridHistory  = []
        self.totalScore = 0
        self._ai = ai_parallelMC()
        self.grid = None
        pass

    def playGame(self):
        self.grid = GameGrid2048(nbRows=3, nbColumns=3)
        self.grid.add_random_tile()
        self.grid.add_random_tile()

        i = 0
        nextMove = 'up'
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
            print("Move {0:<5}, add score {1:>5}, total score {2:>5}".format(nextMove, score, self.totalScore))

            if not has_moved:
                print("did not moved")
                nb_iter_without_moving += 1
            print(self.grid)

        print("Game over in {0} iterations, score = {1}".format(i+1, self.totalScore))

    def saveScores(self):
        N = len( self._scoreHistory )
        datasToStore = DataFrame( np.array([N, 17]) )

        datasToStore[:][0] = self._scoreHistory


if __name__ == '__main__':
    game = consoleAutoPlay()
    game.playGame()
