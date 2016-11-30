#!/usr/bin/python3
# -*- coding: utf-8 -*-


from AI.ai_q_learning import Qlearning
from GameGrids.LogGameGrid import GameGrid2048

NB_ROWS = 3
NB_COLS = 3

class PlayGame:

    def __init__(self):
        self._history = []
        self._ai = Qlearning()

    def Simulate(self):
        file_pattern = '{0}_{1}'.format(NB_ROWS, NB_COLS)
        self._ai.LoadStates(file_pattern)
        for i in range(100):
            self.playGame()
        self._ai.SaveStates(file_pattern)

    def playGame(self):
        current_grid = GameGrid2048(nbRows=3, nbColumns=3)
        print("Created grid \n", current_grid)

        current_grid.initNewGame()
        print("init grid \n", current_grid)

        self._ai.init(current_grid)
        print(current_grid)

        nb_iter = 0
        total_score = 0
        has_moved = True

        while has_moved:
            nb_iter += 1

            old_state = self._ai.GetState(current_grid)
            # self._history.append({'grid': current_grid.clone(), 'score': score, 'action': next_move})

            next_move = self._ai.GetMove(current_grid, self._history)
            score, has_moved = current_grid.moveTo(next_move)

            total_score += score
            print("Move {0:<5}, add score {1:>5}, total score {2:>5}".format(next_move, score, total_score))

            current_grid.add_random_tile()

            self._ai.RecordState(old_state, current_grid, next_move, score, total_score, has_moved)

            print(current_grid)

        print("Game over in {0} iterations, score = {1}".format(nb_iter, total_score))


if __name__ == '__main__':
    game = PlayGame()
    game.Simulate()
