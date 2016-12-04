#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np


class BaseGrid2048:
    def __init__(self, nbRows=0, nbColumns=0, matrix=None, score=0):
        self.rows = nbRows
        self.columns = nbColumns
        self.isGameOver = False
        self.score = score

        if matrix is not None:
            self.rows = matrix.shape[0]
            self.columns = matrix.shape[1]
            self.matrix = np.array(matrix, dtype=int)
        else:
            self.matrix = np.zeros([nbRows, nbColumns], dtype=int)
            self.add_random_tile()
            self.add_random_tile()

    def add_random_tile(self):
        raise NotImplementedError()


def array2DEquals(matrix_a, matrix_b):
    if matrix_a.shape != matrix_b.shape:
        return False
    for i in range(matrix_a.shape[0]):
        for j in range(matrix_a.shape[1]):
            if matrix_a[i,j] != matrix_b[i,j]:
                return False
    return True

