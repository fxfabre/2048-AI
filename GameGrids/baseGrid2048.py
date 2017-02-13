#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import logging
import constants
import random


class BaseGrid2048:

    def __init__(self, nb_rows=0, nb_columns=0, matrix=None):
        self.logger = logging.getLogger(__name__)
        self.isGameOver = False

        if matrix is not None:
            self.matrix = np.array(matrix, dtype=int)
        else:
            self.matrix = np.zeros([nb_rows, nb_columns], dtype=int)
            self.add_random_tile()
            self.add_random_tile()

    def clone(self):
        return type(self)(matrix=self.matrix.copy())

    def add_random_tile(self):
        raise NotImplementedError()

    def GetState(self):
        total = 0
        for i in range(self.columns):
            for j in range(self.rows):
                total = total * self.max_value + self.matrix[i, j]
        return total

    # region Transformations / symmetry
    def run_transfo(self, transfo_name):
        if transfo_name is None:
            return self

        transformations = {
            'symetry_axis_x': self.symetry_axis_x,
            'symetry_axis_y': self.symetry_axis_y,
            'rotate_90'     : self.rotate_90,
            'rotate_180'    : self.rotate_180,
            'rotate_270'    : self.rotate_270,
        }
        return transformations[transfo_name]()

    def symetry_axis_x(self):
        for col in range(self.columns):
            for i in range(self.rows // 2):
                j = self.rows - i - 1
                self.matrix[i, col], self.matrix[j, col] = self.matrix[j, col], self.matrix[i, col]
        return self

    def symetry_axis_y(self):
        for row in range(self.rows):
            for i in range(self.columns // 2):
                j = self.columns - i - 1
                self.matrix[row, i], self.matrix[row, j] = self.matrix[row, j], self.matrix[row, i]
        return self

    def rotate_90(self):
        assert self.rows == self.columns
        self.matrix = np.rot90(self.matrix)
        return self

    def rotate_180(self):
        row = self.rows
        col = self.columns
        assert self.rows == self.columns
        self.matrix = self.matrix.reshape(row * col)[::-1].reshape([row, col])
        return self

    def rotate_270(self):
        assert self.rows == self.columns
        new_matrix = np.zeros([self.columns, self.rows])
        for x in range(self.rows):
            for y in range(self.columns):
                new_matrix[y, self.columns - x - 1] = self.matrix[x, y]
        self.matrix = new_matrix
        return self

    def identity(self):
        return self
    # endregion

    # region Can move
    def canMergeLeftRight(self):
        for row in range(self.rows):
            for column in range(self.columns - 1):
                if self.matrix[row, column] == 0:
                    pass
                elif self.matrix[row, column] == self.matrix[row, column + 1]:
                    return True
        return False

    def canMergeUpDown(self):
        for column in range(self.columns):
            for row in range(self.rows -1):
                if self.matrix[row, column] == 0:
                    pass
                elif self.matrix[row, column] == self.matrix[row +1, column]:
                    return True
        return False

    def canMove(self, direction):
        if direction == 'left':
            return self.canMoveLeft()
        if direction == 'right':
            return self.canMoveRight()
        if direction == 'up':
            return self.canMoveUp()
        if direction == 'down':
            return self.canMoveDown()

        raise Exception("Unknown direction " + str(direction))

    def canMoveLeft(self):
        # Find a tile with an empty box at its left
        for row in range(self.rows):
            for column in range(self.columns -1):
                if (self.matrix[row, column] == 0) and (self.matrix[row, column +1] > 0):
                    return True
        return self.canMergeLeftRight()

    def canMoveUp(self):
        # Find a tile with an empty box above
        for column in range(self.columns):
            for row in range(1, self.rows):
                if (self.matrix[row, column] > 0) and (self.matrix[row - 1, column] == 0):
                    return True
        return self.canMergeUpDown()

    def canMoveDown(self):
        # Find a tile with an empty box below
        for column in range(self.columns):
            for row in range(self.rows -1):
                if (self.matrix[row, column] > 0) and (self.matrix[row +1, column] == 0):
                    return True
        return self.canMergeUpDown()

    def canMoveRight(self):
        # Find a tile with an empty box at its right
        for row in range(self.rows):
            for column in range(1, self.columns):
                if (self.matrix[row, column] == 0) and (self.matrix[row, column -1] > 0):
                    return True
        return self.canMergeLeftRight()
    # endregion

    def is_full(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.matrix[i,j] == 0:
                    return False
        return True

    def is_game_over(self):
        if not self.is_full():
            return False

        # Find 2 consecutive and identical tile
        for _row in range(self.rows - 1):
            for _col in range(self.columns - 1):
                if self.matrix[_row, _col] == self.matrix[_row, _col + 1]:
                    return False
                if self.matrix[_row, _col] == self.matrix[_row + 1, _col]:
                    return False
            if self.matrix[_row, self.columns-1] == self.matrix[_row + 1, self.columns-1]:
                return False
        for _col in range(self.columns - 1):
            if self.matrix[self.rows-1, _col] == self.matrix[self.rows -1, _col +1]:
                return False
        return True

    def can_add_tile(self, x, y):
        return self.matrix[x, y] == 0

    def add_tile(self, row, col, tile_to_add):
        if self.can_add_tile(row, col):
            self.matrix[row, col] = tile_to_add
        else:
            print("Unable to add tile at ({0}, {1})".format(row, col))

    def set_tile(self, row, col, value):
        if self.matrix[row, col] != 0:
            raise Exception("Tile not empty at ({0}, {1}). can't add tile {2}".format(row, col, value))
        self.matrix[row, col] = value

    def get_available_box(self):
        """
            looks for an empty box location;
        """
        available_boxes = []
        for _row in range(self.rows):
            for _column in range(self.columns):
                if self.matrix[_row, _column] == 0:
                    # TODO : replace by .append( (_row, _column) )
                    available_boxes.append(_row * self.columns + _column)

        if len(available_boxes) == 0:
            raise Exception("no more room in grid")

        random_pos = random.choice(available_boxes)
        return random_pos // self.columns, random_pos % self.columns

    def get_empty_tiles(self):
        for col in self.columns:
            for row in self.rows:
                if self.matrix[row, col] == 0:
                    yield row, col

    def toIntMatrix(self):
        return self.matrix

    @property
    def max_value(self):
        return constants.GRID_MAX_VAL or (self.rows + self.columns + 1)

    @property
    def totalScore(self):
        return self.matrix.sum()

    @property
    def rows(self):
        if self.matrix is None:
            return 0
        return self.matrix.shape[0]

    @property
    def columns(self):
        if self.matrix is None:
            return 0
        return self.matrix.shape[1]


def array2DEquals(matrix_a, matrix_b):
    if matrix_a.shape != matrix_b.shape:
        return False
    for i in range(matrix_a.shape[0]):
        for j in range(matrix_a.shape[1]):
            if matrix_a[i,j] != matrix_b[i,j]:
                return False
    return True
