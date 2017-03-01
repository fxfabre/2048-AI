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
        self._logger = self.init_logger()
        self._ai = Qlearning()

    def Simulate(self):
        try:
            nb_iter = 0
            while nb_iter < 2000:
                nb_iter += 1
                self.playGame(nb_iter)

                if nb_iter % 500000 == 0:
                    self._ai.SaveStates()
                if self._logger.isEnabledFor(logging.DEBUG):
                    raise Exception("end game")
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            print("error :", e)
        self._ai.SaveStates()

    def playGame(self, play_number=0):
        current_grid = GameGrid2048(nb_rows=constants.NB_ROWS, nb_columns=constants.NB_COLS)
        current_grid.to_min_state()
        current_state = current_grid.GetState()

        nb_iter = 0
        is_game_over = False
        diff_update = 0

        while not is_game_over:
            nb_iter += 1
            self._logger.debug('')
            self._logger.debug("=" * 30)
            self._logger.debug("New loop")
            self._logger.debug("=" * 30)
            current_grid.print(logging.DEBUG)

            old_state = current_state

            move_dir = self._ai.GetMove(current_grid, [])
            current_grid.moveTo(move_dir)
            current_state = current_grid.GetState()
            self._logger.debug("Moving %s, from %d to %d", move_dir, old_state, current_state)

            current_grid.print(logging.DEBUG)
            current_grid.add_random_tile()
            current_grid.print(logging.DEBUG)
            current_state = current_grid.to_min_state().GetState()

            if current_grid.matrix.max() >= constants.GRID_MAX_VAL:
                self._logger.info("Stop iterations, values too big for the model")
                is_game_over = True
            else:
                diff_update += self._ai.RecordState(old_state, current_state, move_dir)
                is_game_over = current_grid.is_game_over()

        if play_number % 10 == 0:
            self._logger.info("{0:>3} End in {1:>3} iterations, diff = {2}".format(
                play_number, nb_iter, round(diff_update, 4)))

    def init_logger(self):
        log_format = '%(asctime)-15s %(message)s'
        logging.basicConfig(format=log_format, level=logging.INFO)
        return logging.getLogger(self.__class__.__name__)


if __name__ == '__main__':
    game = PlayGame()
    game.Simulate()
