#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import random
import pandas
import matplotlib
from AI.ai_base import BaseAi
from GameGrids.LogGameGrid import GameGrid2048

ALPHA = 0.5
GAMMA = 1.0

class Qlearning(BaseAi):

    def __init__(self):
        print("Init Q learning")
        self._available_moves = ['left', 'right', 'up', 'down']

        self.q_values = pandas.DataFrame()
        self.state_history = None
        self.epsilon = 0.1

    def init(self, grid : GameGrid2048):
        nb_box = grid.rows * grid.columns
        nb_states  = grid.max_value ** nb_box
        nb_actions = 4
        print('Q learning : nb_states', nb_states)
        self.q_values = pandas.DataFrame(np.zeros([nb_states, nb_actions]), columns=self._available_moves)

    def GetMove(self, current_grid, history):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self._available_moves)

        current_state = self.GetState(current_grid)
        max_val = max(self.q_values.iloc[current_state, :])
        idx_moves = []
        for i in range(4):
            if self.q_values.iloc[current_state, i] == max_val:
                idx_moves.append(i)

        if len(idx_moves) == 0:     # shouldn't happen
            idx_move = np.argmax(self.q_values.iloc[current_state, :])
        elif len(idx_moves) == 1:
            idx_move = idx_moves[0]
        else:
            idx_move = random.choice(idx_moves)
        return self._available_moves[idx_move]

    def RecordState(self, old_state, current_grid, next_move, score, total_score, has_moved):
        s = old_state
        a = self._available_moves.index(next_move)

        if not has_moved:
            self.q_values.iloc[s, a] = -1000000000.0

        s_prime = self.GetState(current_grid)
        q_value_a = self.q_values.iloc[s, a]
        q_value_a_prime = self.q_values.iloc[s_prime, :].max()
        print('Update q values from', self.q_values.iloc[s, a], end=' ')
        self.q_values.iloc[s, a] += ALPHA * (0 + GAMMA * q_value_a_prime - q_value_a)
        print('to', self.q_values.iloc[s, a])

    def GetState(self, grid):
        total = 0
        for i in range(grid.columns):
            for j in range(grid.rows):
                total = total * grid.max_value + grid.matrix[i, j]
        return total

    def SaveStates(self, name):
        file_name = name + '_qValues.csv'
        print("Saving file to", file_name)
        self.q_values.to_csv(file_name, sep='|')
        # with open(file_name, 'w+') as f:
        #     for state in range(self.q_values.shape[0]):
        #         f.write(','.join(map(str, self.q_values[state, :])) + '\n')

    def LoadStates(self, name):
        file_name = name + '_qValues.csv'
        if os.path.exists(file_name):
            self.q_values = pandas.read_csv(file_name, sep='|', index_col=0)
        # with open(file_name, 'w+') as f:
        #     for state in range(len(self.q_values)):
        #         f.write(','.join(map(str, self.q_values[state, :])) + '\n')



