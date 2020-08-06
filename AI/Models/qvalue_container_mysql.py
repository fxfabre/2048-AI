#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas
import constants
from Tools.have_logger import IHaveLogger


class QvaluesContainer(IHaveLogger):

    def __init__(self, moves_list):
        super(QvaluesContainer, self).__init__()
        self._moves_list = moves_list

        self.nb_row = constants.NB_ROWS
        self.nb_col = constants.NB_COLS
        self.max_value = constants.GRID_MAX_VAL
        self.nb_states = self.max_value ** (self.nb_row * self.nb_col)

        # self.file_pattern = os.path.join(constants.SAVE_DIR, '{0}_{1}_qValues.csv'.format(self.nb_row, self.nb_col))

    def get_state(self, matrix):
        total = 0
        for val in matrix.reshape(self.nb_row * self.nb_col):
            total = total * self.max_value + val
        return int(total)

    def set_qval(self, state, action, value):
        index = self.state_to_min_state[state]
        self.q_values.iloc[index, action] = value

    def get_qval(self, state, action):
        index = self.state_to_min_state[state]
        return self.q_values.iloc[index, action]

    def set_qvals(self, state, values):
        index = self.state_to_min_state[state]
        self.q_values.iloc[index, :] = values

    def get_qvals(self, state):
        index = self.state_to_min_state[state]
        return self.q_values.iloc[index, :]

    def add_value(self, state, action, value_to_add):
        index = self.state_to_min_state[state]
        self.q_values.iloc[index, action] += value_to_add

    # endregion
