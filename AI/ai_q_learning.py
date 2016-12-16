#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import random
import pandas
import logging
import itertools

from AI.ai_base import BaseAi
from GameGrids.LogGameGrid import GameGrid2048
import constants

ALPHA = 0.5
GAMMA = 1.0
EPSILON = 0.8       # 1 means move at random
REWARD_END_GAME = -1000000000.0


class Qlearning(BaseAi):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        print("Init Q learning")
        self._moves_list = ['left', 'right', 'up', 'down']

        self.q_values = pandas.DataFrame()
        self.state_history = None
        self.epsilon = EPSILON

    def init(self, nb_row, nb_col, max_value):
        nb_box      = nb_row * nb_col
        nb_states   = max_value ** nb_box
        # nb_actions  = 4
        # self.q_values = pandas.DataFrame(np.zeros([nb_states, nb_actions]), columns=self._moves_list)
        self.q_values = pandas.DataFrame(index=range(nb_states), columns=self._moves_list)
        self.q_values.fillna(0, inplace=True)
        print('Init Q learning success :', self.q_values.shape)

    def GetMove(self, current_grid : GameGrid2048, history):
        available_moves = [move for move in self._moves_list if current_grid.canMove(move)]
        self._logger.debug('Available moves : {0}'.format(available_moves))
        if len(available_moves) == 1:
            self._logger.debug("One move available : " + available_moves[0])
            return available_moves[0]       # Don't waste time running AI
        if len(available_moves) == 0:
            self._logger.debug("No move available.")
            return self._moves_list[0]      # whatever, it wont't move !

        if random.uniform(0, 1) < self.epsilon:
            self._logger.debug("Randomly choose move")
            return random.choice(available_moves)

        current_state = self.GetState(current_grid)
        current_q_val = self.q_values.iloc[current_state, :][available_moves]
        self._logger.debug("Q values for current state :\n{0}".format(current_q_val))

        max_val = current_q_val.max()
        optimal_moves = current_q_val[current_q_val == max_val].index.tolist()
        self._logger.debug("Optimal moves :\n{0}".format(optimal_moves))

        if len(optimal_moves) == 0:     # shouldn't happen
            raise Exception("No optimal move in Get move function")
            # idx_move = np.argmax(self.q_values.iloc[current_state, :])
        elif len(optimal_moves) == 1:
            return optimal_moves[0]
        else:
            return random.choice(optimal_moves)

    def RecordState(self, old_state, current_grid, next_move, score, total_score, has_moved):
        if next_move == '':
            next_move = random.choice(self._moves_list)

        s = old_state
        a = self._moves_list.index(next_move)
        s_prime = self.GetState(current_grid)
        q_value_s = self.q_values.iloc[s, a]
        q_value_s_prime = self.q_values.iloc[s_prime, :].max()

        if has_moved:
            reward = 0
        else:
            reward = REWARD_END_GAME

        self._logger.debug("Update q values from {0}".format(self.q_values.iloc[s, a]))
        self.q_values.iloc[s, a] += ALPHA * (reward + GAMMA * q_value_s_prime - q_value_s)
        self._logger.debug("To {0}".format(self.q_values.iloc[s, a]))

    def GetState(self, grid):
        total = 0
        for i in range(grid.columns):
            for j in range(grid.rows):
                total = total * grid.max_value + grid.matrix[i, j]

        return total

    def SaveStates(self, name):
        file_name = name + '_qValues.csv'
        self._logger.info("Saving file to " + file_name)
        self.q_values.to_csv(file_name, sep='|')

    def LoadStates(self, name):
        file_name = name + '_qValues.csv'
        current_shape = self.q_values.shape
        if os.path.exists(file_name):
            self._logger.info("Read Q values file from " + file_name)
            self.q_values = pandas.read_csv(file_name, sep='|', index_col=0)
        assert current_shape == self.q_values.shape

    def set_end_states_in_q_values(self):
        for grid in GameGrid2048.getFinalStates():
            state = self.GetState(grid)
            print(grid)

            # self.q_values.iloc[state, :] = [REWARD_END_GAME, REWARD_END_GAME, REWARD_END_GAME, REWARD_END_GAME]
        # self.SaveStates("end_states")

