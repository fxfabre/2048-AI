#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import random
import constants
import itertools

from GameGrids.baseGrid2048 import BaseGrid2048, array2DEquals


class GameGrid2048(BaseGrid2048):

    ###############
    # Moves
    ###############
    def moveTo(self, direction=""):
        if self.matrix.max() >= constants.GRID_MAX_VAL:
            return 0, False

        direction = direction.lower()
        if direction == 'left':
            return self.moveLeft()
        elif direction == 'right':
            return self.moveRight()
        elif direction == 'up':
            return self.moveUp()
        elif direction == 'down':
            return self.moveDown()
        return 0, False

    def moveLeft(self):
        _at = self.matrix
        score = 0
        have_moved = False

        # Step 1 : fusion of equal tiles
        for _row in range(self.rows):
            for _column in range(self.columns - 1):

                # find same tile
                for _column_next in range(_column + 1, self.columns):
                    if _at[_row, _column_next] == 0:
                        continue
                    if _at[_row, _column] == _at[_row, _column_next]:
                        self.matrix[_row, _column] += 1
                        self.matrix[_row, _column_next] = 0
                        score += 1 << _at[_row, _column]
                        have_moved = True
                    break

        # Step 2 : Move tiles
        for _row in range(self.rows):

            # Skip columns with > 0 tile
            _first_empty_column = self.columns # après la dernière colonne
            for _column in range(self.columns - 1):
                if _at[_row, _column] == 0:
                    _first_empty_column = _column
                    break

            # Move tiles
            for _column in range(_first_empty_column + 1, self.columns):
                if _at[_row, _column] > 0:
                    self.matrix[_row, _first_empty_column] = _at[_row, _column]
                    _at[_row, _column] = 0
                    _first_empty_column += 1
                    have_moved = True

        return score, have_moved

    def moveRight(self):
        _at = self.matrix
        score = 0
        have_moved = False

        # Step 1 : fusion of equal tiles
        for _row in range(self.rows):
            for _column in range(self.columns - 1, 0, -1):

                # find same tile
                for _column_next in range(_column - 1, -1, -1):
                    if _at[_row, _column_next] == 0:
                        continue
                    if _at[_row, _column] == _at[_row, _column_next]:
                        self.matrix[_row, _column] += 1
                        self.matrix[_row, _column_next] = 0
                        score += 1 << _at[_row, _column]
                        have_moved = True
                    break

        # Step 2 : Move tiles
        for _row in range(self.rows):

            # Skip columns with > 0 tile
            _first_empty_column = -1 # avant la premiere colonne
            for _column in range(self.columns - 1, -1, -1):
                if _at[_row, _column] == 0:
                    _first_empty_column = _column
                    break

            # Move tiles
            for _column in range(_first_empty_column-1, -1, -1):
                if _at[_row, _column] > 0:
                    self.matrix[_row, _first_empty_column] = _at[_row, _column]
                    _at[_row, _column] = 0
                    _first_empty_column -= 1
                    have_moved = True

        return score, have_moved

    def moveUp(self):
        _at = self.matrix
        score = 0
        have_moved = False

        # Step 1 : fusion of equal tiles
        for _column in range(self.columns):
            for _row in range(self.rows - 1):

                # find same tile
                for _row_next in range(_row + 1, self.rows):

                    if _at[_row_next, _column] == 0:
                        continue
                    if _at[_row, _column] == _at[_row_next, _column]:
                        self.matrix[_row, _column] += 1
                        self.matrix[_row_next, _column] = 0
                        score += 1 << _at[_row, _column]
                        have_moved = True
                    break

        # Step 2 : Move tiles
        for _column in range(self.columns):

            # Skip columns with > 0 tile
            _first_empty_row = self.rows # après la dernière colonne
            for _row in range(self.rows - 1):
                if _at[_row, _column] == 0:
                    _first_empty_row = _row
                    break

            # Move tiles
            for _row in range(_first_empty_row+1, self.rows):
                if _at[_row, _column] > 0:
                    self.matrix[_first_empty_row, _column] = _at[_row, _column]
                    _at[_row, _column] = 0
                    _first_empty_row += 1
                    have_moved = True

        return score, have_moved

    def moveDown(self):
        _at = self.matrix
        score = 0
        have_moved = False

        # Step 1 : fusion of equal tiles
        for _column in range(self.columns):
            for _row in range(self.rows - 1, 0, -1):

                # find same tile
                for _row_next in range(_row - 1, -1, -1):

                    if _at[_row_next, _column] == 0:
                        continue
                    if _at[_row, _column] == _at[_row_next, _column]:
                        self.matrix[_row, _column] += 1
                        self.matrix[_row_next, _column] = 0
                        score += 1 << _at[_row, _column]
                        have_moved = True
                    break

        # Step 2 : Move tiles
        for _column in range(self.columns):

            # Skip columns with > 0 tile
            _first_empty_row = -1 # avant la premiere ligne
            for _row in range(self.rows - 1, -1, -1):
                if _at[_row, _column] == 0:
                    _first_empty_row = _row
                    break

            # Move tiles
            for _row in range(_first_empty_row-1, -1, -1):
                if _at[_row, _column] > 0:
                    self.matrix[_first_empty_row, _column] = _at[_row, _column]
                    _at[_row, _column] = 0
                    _first_empty_row -= 1
                    have_moved = True

        return score, have_moved

    ################
    def add_random_tile(self):
        """
            pops up a random tile
        """
        # ensure we yet have room in grids
        if self.is_full():
            return

        _value = random.choice([1, 1, 1, 2, 1, 1, 1, 1, 1, 1])
        _row, _column = self.get_available_box()
        self.set_tile(_row, _column, _value)

    @staticmethod
    def get_all_states(min_val=0):
        grid_size = constants.NB_ROWS * constants.NB_COLS
        for grid_values in itertools.product(range(min_val, constants.GRID_MAX_VAL), repeat=grid_size):
            matrix = np.array(grid_values).reshape(constants.NB_ROWS, constants.NB_COLS)
            grid = GameGrid2048(matrix=matrix)
            yield grid

    @staticmethod
    def get_final_states():
        i = 0
        for grid in GameGrid2048.get_all_states(1):
            i += 1
            if i % 100 == 0:
                print("Get final state number", i)

            if grid.canMergeUpDown():
                continue
            if grid.canMergeLeftRight():
                continue

            yield grid

    def print(self, log_level):
        if self.logger.isEnabledFor(log_level):
            print(self)

    def __str__(self):
        state_val = 0
        for i in range(self.columns):
            for j in range(self.rows):
                state_val = state_val * self.max_value + self.matrix[i, j]

        realValues = np.zeros([self.rows, self.columns], dtype=int)
        for i in range(self.rows):
            for j in range(self.columns):
                realValues[i, j] = 1 << self.matrix[i, j]
        return str(realValues).replace('[1 ', '[. ').replace(' 1 ', ' . ').replace(' 1]', ' .]') + '  ' + str(state_val)

    def __eq__(self, other):
        return array2DEquals(self.matrix, other.matrix)

