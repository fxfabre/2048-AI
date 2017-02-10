#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import logging
import constants


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
