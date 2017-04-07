#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import pandas
import logging
import constants
import numpy as np
from GameGrids.LogGameGrid import GameGrid2048


class QvaluesContainer:

    def __init__(self, moves_list):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._moves_list = moves_list

        self.nb_row = constants.NB_ROWS
        self.nb_col = constants.NB_COLS
        self.max_value = constants.GRID_MAX_VAL
        self.nb_states = self.max_value ** (self.nb_row * self.nb_col)

        self.q_values = None
        self.file_pattern = os.path.join(constants.SAVE_DIR, '{0}_{1}_qValues.csv'.format(self.nb_row, self.nb_col))

        self.load_states()
        if self.q_values is None:
            self.state_to_min_state = self.state_number_to_tab_index()
            self.nb_states = len(self.state_to_min_state)
            self.q_values = pandas.DataFrame(index=range(self.nb_states), columns=self._moves_list)
            self.q_values.fillna(0, inplace=True)

        self.logger.info('Init Q learning success : %s', self.q_values.shape)

    def save_states(self, nb_iter):
        file_pattern = self.file_pattern + '_' + str(nb_iter)
        self.logger.info("Saving file to %s", file_pattern)
        self.q_values['state'] = np.zeros(self.nb_states)
        for min_state, index_id in self.state_to_min_state.items():
            self.q_values.loc[index_id, 'state'] = int(min_state)
        self.q_values.to_csv(self.file_pattern, sep='|')

    def load_states(self):
        if not os.path.exists(self.file_pattern):
            return

        self.logger.info("Read Q values file from %s", self.file_pattern)
        self.q_values = pandas.read_csv(self.file_pattern, sep='|', index_col=0)
        self.nb_states = self.q_values.shape[0]
        self.state_to_min_state = {
            int(min_state): int(index_id) for min_state, index_id
            in zip(self.q_values['state'], range(self.nb_states))
        }
        self.q_values = self.q_values[self._moves_list]

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

    # region Compute min state
    def state_number_to_tab_index(self):
        """
        define : min state = in all equivalent states, the state with the min value
        find the min states : ex {2, 8, 1, 12} among all states
        and compute the translation dictionnary, to save only these states.
        ex translation dict = {1 : 2, 2 : 8, 3 : 1, 4 : 12}
        :return: translation dict
        """
        # for each state, save the min state in state_mapping
        state_mapping = self.get_state_to_min_state()
        distinct_states = set(state_mapping)
        return {
            int(min_state) : int(index_id) for min_state, index_id
            in zip(distinct_states, range(len(distinct_states)))
        }

    def get_state_to_min_state(self):
        state_mapping = np.zeros(self.nb_states) - 1
        for grid in GameGrid2048.get_all_states():
            current_state = self.get_state(grid.matrix)
            if state_mapping[current_state] >= 0:
                continue

            eq_states = self.get_state_equivalence(grid, current_state)
            min_state = min(eq_states)
            for s in eq_states:
                state_mapping[s] = min_state
        return state_mapping

    def get_state_equivalence(self, grid, current_state):
        equivalent_states = [current_state]
        for tx in ['symetry_axis_x', None]:
            for ty in ['symetry_axis_y', None]:
                for rotate in ['rotate_90', 'rotate_180', 'rotate_270', None]:
                    nb_transfo = 0
                    loc_grid = grid.clone()
                    if not(tx is None):
                        loc_grid.run_transfo(tx)
                        nb_transfo += 1
                    if not(ty is None):
                        loc_grid.run_transfo(ty)
                        nb_transfo += 1
                    if not(rotate is None):
                        loc_grid.run_transfo(rotate)
                        nb_transfo += 1

                    if nb_transfo > 0:
                        state = loc_grid.GetState()
                        equivalent_states.append(state)
        return set(equivalent_states)
    # endregion
