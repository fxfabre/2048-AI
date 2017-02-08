#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import random
import pandas
import logging

from AI.ai_base import BaseAi
from GameGrids.LogGameGrid import GameGrid2048

ALPHA = 0.5
GAMMA = 1.0
EPSILON = 0.2       # 1 means move at random
REWARD_MOVE = 1.0
REWARD_END_GAME = -10.0


class Qlearning(BaseAi):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info("Init Q learning")
        self._moves_list = ['left', 'right', 'up', 'down']

        self.q_values = pandas.DataFrame()
        self.state_history = None

        self.epsilon = EPSILON
        self.alpha = ALPHA
        self.gamma = GAMMA
        self.reward_move = REWARD_MOVE
        self.reward_end_game = REWARD_END_GAME

    def init(self, nb_row, nb_col, max_value, file_pattern):
        nb_box      = nb_row * nb_col
        nb_states   = max_value ** nb_box
        self.q_values = pandas.DataFrame(index=range(nb_states), columns=self._moves_list)
        if not self.LoadStates(file_pattern):
            self.q_values.fillna(0, inplace=True)
            self.init_end_states()
        self._logger.info('Init Q learning success : %s', self.q_values.shape)

    def init_end_states(self):
        self._logger.debug("Start init end states")
        for grid in GameGrid2048.get_final_states():
            state = self.GetState(grid)
            self.q_values.iloc[state, :] = [REWARD_END_GAME] * 4
        self._logger.debug("Init end states done")

    def GetMove(self, current_grid : GameGrid2048, history):
        available_moves = [move for move in self._moves_list if current_grid.canMove(move)]

        # Set bad Q value for impossible moves
        # TODO : move in init
        current_state = self.GetState(current_grid)
        for index, move in enumerate(self._moves_list):
            if move not in available_moves:
                self.q_values.iloc[current_state, index] = REWARD_END_GAME

        # self._logger.debug('Available moves : %s', available_moves)
        if len(available_moves) == 1:
            # self._logger.debug("One move available : %s", available_moves[0])
            return available_moves[0]       # Don't waste time running AI
        if len(available_moves) == 0:
            # self._logger.debug("No move available.")
            return self._moves_list[0]      # whatever, it wont't move !

        if (self.epsilon > 0) and (random.uniform(0, 1) < self.epsilon):
            # self._logger.debug("Randomly choose move")
            return random.choice(available_moves)

        current_q_val = self.q_values.iloc[current_state, :][available_moves]

        max_val = current_q_val.max()
        optimal_moves = current_q_val[current_q_val == max_val].index.tolist()
        # self._logger.debug("Optimal moves : %s", optimal_moves)

        if len(optimal_moves) == 0:     # shouldn't happen
            raise Exception("No optimal move in Get move function")
            # idx_move = np.argmax(self.q_values.iloc[current_state, :])
        elif len(optimal_moves) == 1:
            return optimal_moves[0]
        else:
            return random.choice(optimal_moves)

    def RecordState(self, s, s_prime, move_dir):
        if move_dir == '':
            move_dir = random.choice(self._moves_list)

        a = self._moves_list.index(move_dir)
        q_value_s = self.q_values.iloc[s, a]
        q_value_s_prime = self.q_values.iloc[s_prime, :].max()

        self._logger.debug("Update q values from state %s, move %s to state %s", s, move_dir, s_prime)
        self._logger.debug("\n%s", self.q_values.iloc[s, :])

        value_to_add = self.alpha * (self.reward_move + self.gamma * q_value_s_prime - q_value_s)
        self.q_values.iloc[s, a] += value_to_add

        self._logger.debug("Diff : %s => new value %s : %s", value_to_add, s, self.q_values.iloc[s, a])
        self._logger.debug("\n%s", self.q_values.iloc[s_prime, :])
        return abs(value_to_add)

    def SaveStates(self, name):
        file_name = name + '_qValues.csv'
        self._logger.info("Saving file to %s", file_name)
        self.q_values.to_csv(file_name, sep='|')

    def LoadStates(self, name):
        file_name = name + '_qValues.csv'
        current_shape = self.q_values.shape
        if os.path.exists(file_name):
            self._logger.info("Read Q values file from %s", file_name)
            self.q_values = pandas.read_csv(file_name, sep='|', index_col=0)
            self._moves_list = self.q_values.columns.tolist()
            assert current_shape == self.q_values.shape
            return True
        return False

    def GetState(self, grid):
        total = 0
        for i in range(grid.columns):
            for j in range(grid.rows):
                total = total * grid.max_value + grid.matrix[i, j]
        return total

    def get_symetric_states_for_grid(self, grid : GameGrid2048):
        equivalent_states = {}
        current_state = self.GetState(grid)
        equivalent_states[current_state] = 0

        for tx in ['symetry_axis_x', None]:
            for ty in ['symetry_axis_y', None]:
                for rotate in ['rotate_90', 'rotate_180', 'rotate_270', None]:
                    transformations = []
                    loc_grid = grid.clone()
                    if not(tx is None):
                        loc_grid.run_transfo(tx)
                        transformations.append(tx)
                    if not(ty is None):
                        loc_grid.run_transfo(ty)
                        transformations.append(ty)
                    if not(rotate is None):
                        loc_grid.run_transfo(rotate)
                        transformations.append(rotate)

                    state = self.GetState(loc_grid)
                    equivalent_states[state] = min(len(transformations), equivalent_states.get(state, '999'))
        return equivalent_states

    def get_symetric_states(self):
        states = {}
        for grid in GameGrid2048.get_all_states():
            state = self.GetState(grid)
            equivalent_states = self.get_symetric_states_for_grid(grid)
            min_state = min(equivalent_states.keys())
            states[state] = {min_state : equivalent_states[min_state]}
        keys = states.keys()
        keys = list(keys)
        keys.sort()
        for key in keys:
            val = states[key]
            print(key, val)

