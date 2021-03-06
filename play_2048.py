#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import math
import logging
import traceback
import numpy as np

from AI.ai_q_learning import Qlearning
from GameGrids.LogGameGrid import GameGrid2048
import constants

COEFF = 100   # 100


class PlayGame:

    def __init__(self):
        self._logger = self.init_logger()
        self._ai = Qlearning()

    def Simulate(self):
        if os.path.exists('scores.txt'):
            os.remove('scores.txt')
        play_number = 0
        try:
            while True:
                play_number += 1
                nb_moves, diff_update = self.playGame()

                if play_number % 100 == 0:
                    self._logger.info("{0:>3} End in {1:>3} iterations, diff = {2}".format(
                        play_number, nb_moves, round(diff_update, 4)))
                if play_number % (500 * COEFF) == 0:
                    self.eval_strat(play_number)
                if play_number % (5000 * COEFF) == 0:
                    self._ai.SaveStates(play_number // 1000)
                if self._logger.isEnabledFor(logging.DEBUG):
                    raise Exception("end game")
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            print("error :", e)
        self._ai.SaveStates(play_number // 1000)

    def eval_strat(self, nb_play_training_done=0):
        self._logger.info("Evaluate strat after %s moves", nb_play_training_done)
        epsilon = self._ai.epsilon
        self._ai.epsilon = 0  # epsilon-greedy

        # Play
        nb_total_play = 1000
        nb_moves_done = np.zeros(100)   # 100 moves max in game before end
        for play_number in range(nb_total_play):
            nb_moves, _ = self.playGame()
            nb_moves_done[nb_moves] += 1

        # Compute mean / var of the number of moves done in each play
        moyenne = 0
        moyenne_square = 0
        for i in range(nb_moves_done.shape[0]):
            nb_moves = nb_moves_done[i]
            if nb_moves > 0:
                moyenne += i * nb_moves
                moyenne_square += i * i * nb_moves
                print(i, nb_moves)
        moyenne /= nb_total_play
        moyenne_square /= nb_total_play
        std = math.sqrt(moyenne_square - moyenne * moyenne)
        print("mean : ", moyenne)
        print("std  : ", std)

        # Save to file
        with open('scores.txt', 'a+') as f:
            f.write('|'.join(map(str, [nb_play_training_done, moyenne, std])) + '\n')

        self._ai.epsilon = epsilon

    def playGame(self):
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

            move_dir = self._ai.GetMove(current_grid)
            current_grid.moveTo(move_dir)
            current_state = current_grid.GetState()
            self._logger.debug("Moving %s, from %d to %d", move_dir, old_state, current_state)

            current_grid.print(logging.DEBUG)
            current_grid.add_random_tile()
            current_grid.print(logging.DEBUG)
            current_state = current_grid.to_min_state().GetState()

            if current_grid.matrix.max() >= constants.GRID_MAX_VAL:
                # self._logger.info("Stop iterations, values too big for the model")
                is_game_over = True
            else:
                diff_update += self._ai.RecordState(old_state, current_state, move_dir)
                is_game_over = current_grid.is_game_over()

        return nb_iter, diff_update

    def init_logger(self):
        log_format = '%(asctime)-15s %(message)s'
        logging.basicConfig(format=log_format, level=logging.INFO)
        return logging.getLogger(self.__class__.__name__)


if __name__ == '__main__':
    game = PlayGame()
    game.Simulate()
    # game.eval_strat()
