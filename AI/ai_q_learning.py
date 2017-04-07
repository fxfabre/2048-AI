#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import logging
import constants

from GameGrids.LogGameGrid import GameGrid2048
from AI.Models.qvalue_container import QvaluesContainer

ALPHA = 0.5
GAMMA = 1.0
EPSILON = 0.2       # 1 means move at random
REWARD_MOVE = 0.25
REWARD_END_GAME = -10.0


class Qlearning:

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info("Init Q learning")
        self._moves_list = ['left', 'right', 'up', 'down']
        self.file_history = None

        # Force epsilon-greedy if record moves
        self.epsilon = (constants.RECORD_MOVES and 0) or EPSILON
        self.alpha = ALPHA
        self.gamma = GAMMA
        self.reward_move = REWARD_MOVE
        self.reward_end_game = REWARD_END_GAME

        self.qval_container = QvaluesContainer(self._moves_list)
        self.init_end_states()

        # if constants.RECORD_MOVES:
        #     self.file_history = open(os.path.join(constants.SAVE_DIR, constants.FILE_RECORD_MOVES), 'a+')

    def init_end_states(self):
        self._logger.debug("Start init end states")
        for grid in GameGrid2048.get_final_states():
            grid.to_min_state()
            state = self.qval_container.get_state(grid.matrix)
            self.qval_container.set_qvals(state, [REWARD_END_GAME] * 4)
        self._logger.debug("Init end states done")

        # TODO : bugfix Attention aux final state. Bien initialise ?
        # # Set bad Q value for impossible moves
        # current_state = current_grid.GetState()
        # for index, move in enumerate(self._moves_list):
        #     if move not in available_moves:
        #         self.q_values.iloc[current_state, index] = REWARD_END_GAME

    def GetMove(self, current_grid : GameGrid2048):
        available_moves = [move for move in self._moves_list if current_grid.canMove(move)]

        self._logger.debug('Available moves : %s', available_moves)
        if len(available_moves) == 1:
            return available_moves[0]       # Don't waste time running AI
        if len(available_moves) == 0:
            return self._moves_list[0]      # whatever, it wont't move !

        if (self.epsilon > 0) and (random.uniform(0, 1) < self.epsilon):
            # self._logger.debug("Randomly choose move")
            return random.choice(available_moves)

        current_state = self.qval_container.get_state(current_grid.matrix)
        current_q_val = self.qval_container.get_qvals(current_state)[available_moves]

        max_val = current_q_val.max()
        optimal_moves = current_q_val[current_q_val == max_val].index.tolist()

        # if not(self.file_history is None):
        #     nb_cell = current_grid.matrix.shape[0] * current_grid.matrix.shape[1]
        #     line = '|'.join(map(str, current_grid.matrix.reshape(nb_cell)))
        #     for move in optimal_moves:
        #         self.file_history.write(line + '|' + move + '\n')

        if len(optimal_moves) == 0:     # shouldn't happen
            raise Exception("No optimal move in Get move function")
        elif len(optimal_moves) == 1:
            return optimal_moves[0]
        else:
            return random.choice(optimal_moves)

    def RecordState(self, s, s_prime, move_dir):
        if move_dir == '':
            move_dir = random.choice(self._moves_list)

        a = self._moves_list.index(move_dir)
        q_value_s = self.qval_container.get_qval(s, a)
        v_value_s_prime = self.qval_container.get_qvals(s_prime).max()

        self._logger.debug("Update q values from state %s, move %s to state %s", s, move_dir, s_prime)
        self._logger.debug("\n%s", self.qval_container.get_qvals(s))

        value_to_add = self.alpha * (self.reward_move + self.gamma * v_value_s_prime - q_value_s)
        self.qval_container.add_value(s, a, value_to_add)

        self._logger.debug("Diff : %s => new value %s : %s", value_to_add, s, self.qval_container.get_qval(s, a))
        self._logger.debug("\n%s", self.qval_container.get_qvals(s_prime))
        return abs(value_to_add)

    def SaveStates(self, nb_iter):
        self.qval_container.save_states(nb_iter)

    # def __del__(self):
    #     if self.file_history:
    #         self.file_history.close()
    #         self.file_history = None
