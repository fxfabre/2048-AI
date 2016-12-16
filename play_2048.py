#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import logging
import traceback

from AI.ai_q_learning import Qlearning
from GameGrids.LogGameGrid import GameGrid2048
import constants


class PlayGame:

    def __init__(self):
        self.init_logger()
        self._logger = logging.getLogger(__name__)

        self._history = []
        self._ai = Qlearning()

        self._ai.init(constants.NB_ROWS, constants.NB_COLS, constants.GRID_MAX_VAL)
        print(self._ai.q_values.shape)

    def Simulate(self):
        file_pattern = os.path.join(constants.SAVE_DIR, '{0}_{1}'.format(constants.NB_ROWS, constants.NB_COLS))
        self._ai.LoadStates(file_pattern)

        try:
            nb_iter = 0
            while True:
                nb_iter += 1
                self.playGame(nb_iter)

                if nb_iter % 500000 == 0:
                    self._ai.SaveStates(file_pattern)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
        self._ai.SaveStates(file_pattern)

    def playGame(self, play_number=0):
        current_grid = GameGrid2048(nbRows=constants.NB_ROWS, nbColumns=constants.NB_COLS)

        nb_iter = 0
        total_score = 0
        has_moved = True

        while has_moved:
            nb_iter += 1

            self._logger.debug('')
            self._logger.debug("=" * 30)
            self._logger.debug("New loop")
            self._logger.debug("=" * 30)
            self._logger.debug('\n{0}'.format(current_grid))

            old_state = self._ai.GetState(current_grid)
            self._logger.debug("current state :" + str(old_state))

            next_move = self._ai.GetMove(current_grid, self._history)
            score, has_moved = current_grid.moveTo(next_move)
            self._logger.debug("Moving to {0}, score : {1}, has moved : {2}".format(next_move, score, has_moved))
            # self._history.append({'grid': current_grid.clone(), 'score': score, 'action': next_move})

            total_score += score
            self._logger.debug('\n{0}'.format(current_grid))

            current_grid.add_random_tile()
            self._logger.debug("Random tile added \n" + str(current_grid))

            if current_grid.matrix.max() >= constants.GRID_MAX_VAL:
                self._logger.info("Stop iterations, values too big for the model")
                has_moved = False
            else:
                self._ai.RecordState(old_state, current_grid, next_move, score, total_score, has_moved)

        self._logger.info("{2:>3} Game over in {0} iterations, score = {1}".format(
            nb_iter, total_score, play_number))

    def init_logger(self):
        log_filename = os.path.join('/tmp', "2048_" + str(int(time.time())) + ".log")
        log_format = '%(asctime)-15s %(message)s'
        logging.basicConfig(format=log_format, level=logging.INFO)


if __name__ == '__main__':
    game = PlayGame()
    game.Simulate()
