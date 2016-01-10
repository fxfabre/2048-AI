#!/usr/bin/python3
# -*- coding: utf-8 -*-

from GUI.gameBoard2048 import gameBoard2048
from AI.GameGridLight import gameGridLight

from AI.ai_random import ai_random
from AI.ai_bestScoreNextMove import ai_bestScoreNextMove
from AI.ai_MC import ai_MCsimulation
from AI.ai_parallelMC import ai_parallelMC


class consoleAutoPlay:

    def __init__(self):
        self._scoreHistory = []
        self._gridHistory  = []
        self.totalScore = 0
        self._ai = ai_parallelMC()
        self.grid = None
        pass

    def playGame(self):
        self.grid = gameGridLight(nbRows=4, nbColumns=4)
        self.grid.add_random_tile()
        self.grid.add_random_tile()

        i = 0
        nextMove = 'up'
        nb_itera_without_moving = 0
        while nb_itera_without_moving < 5:
            i += 1

            # Add history (grid and score) data
#            self._scoreHistory.append( self.totalScore )
#            self._gridHistory.append( grid.matrix )

            # Get next move : 'left', 'right', 'up' or 'down'
            nextMove = self._ai.move_next(self, self._gridHistory, self._scoreHistory)

            if len(nextMove) == 0:
                print("null direction")
                print(self.grid.matrix)
                nb_itera_without_moving += 1
                continue

            score, has_moved = self.grid.moveTo(nextMove)
            self.grid.add_random_tile()
            self.totalScore += score
            print("Move {0:<5}, add score {1:>5}, total score {2:>5}".format(nextMove, score, self.totalScore))

            if not has_moved:
                print("did not moved")
                print(self.grid.matrix)
                nb_itera_without_moving += 1
            print(self.grid)

        print("Game over in {0} iterations, score = {1}".format(i+1, self.totalScore))


if __name__ == '__main__':
    game = consoleAutoPlay()
    game.playGame()
