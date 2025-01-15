#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
import numpy as np
from GameGrids.baseGrid2048 import BaseGrid2048, array2DEquals


class testConstructor(unittest.TestCase):

    def test_Initialisation(self):
        tab = np.array(
            [[0,0,0,0],
             [0,0,0,0],
             [0,0,0,0],
             [0,0,0,0]]
        )
        grid = BaseGrid2048(0, 0, tab)
        self.assertEqual(4, grid.rows)
        self.assertEqual(4, grid.columns)
        #
        # grid = BaseGrid2048(3, 4)
        # self.assertEqual(3, grid.rows)
        # self.assertEqual(4, grid.columns)


class TestSymetryX(unittest.TestCase):

    def test_axis_x_2by2(self):
        tab = np.array(
            [[1, 2],
             [3, 4]]
        )
        target = np.array(
            [[3, 4],
             [1, 2]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.symetry_axis_x()
        self.assertTrue(array2DEquals(grid.matrix, target), "Sx, matrix 2x2\n" + str(grid.matrix))

    def test_axis_x_3by3(self):
        tab = np.array(
            [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]]
        )
        target = np.array(
            [[7, 8, 9],
             [4, 5, 6],
             [1, 2, 3]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.symetry_axis_x()
        self.assertTrue(array2DEquals(grid.matrix, target), "Sx, matrix 3x3\n" + str(grid.matrix))

    def test_axis_x_4by4(self):
        tab = np.array(
            [[ 1,  2,  3,  4],
             [ 5,  6,  7,  8],
             [ 9, 10, 11, 12],
             [13, 14, 15, 16]]
        )
        target = np.array(
            [[13, 14, 15, 16],
             [ 9, 10, 11, 12],
             [ 5,  6,  7,  8],
             [ 1,  2,  3,  4]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.symetry_axis_x()
        self.assertTrue(array2DEquals(grid.matrix, target), "Sx, matrix 4x4\n" + str(grid.matrix))


class TestSymetryY(unittest.TestCase):
    def test_axis_y_2by2(self):
        tab = np.array(
            [[1, 2],
             [3, 4]]
        )
        target = np.array(
            [[2, 1],
             [4, 3]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.symetry_axis_y()
        self.assertTrue(array2DEquals(grid.matrix, target), "Sy, matrix 2x2\n" + str(grid.matrix))

    def test_axis_y_3by3(self):
        tab = np.array(
            [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]]
        )
        target = np.array(
            [[3, 2, 1],
             [6, 5, 4],
             [9, 8, 7]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.symetry_axis_y()
        self.assertTrue(array2DEquals(grid.matrix, target), "Sy, matrix 3x3\n" + str(grid.matrix))

    def test_axis_y_4by4(self):
        tab = np.array(
            [[ 1,  2,  3,  4],
             [ 5,  6,  7,  8],
             [ 9, 10, 11, 12],
             [13, 14, 15, 16]]
        )
        target = np.array(
            [[ 4,  3,  2,  1],
             [ 8,  7,  6,  5],
             [12, 11, 10,  9],
             [16, 15, 14, 13]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.symetry_axis_y()
        self.assertTrue(array2DEquals(grid.matrix, target), "Sy, matrix 4x4\n" + str(grid.matrix))


class TestRotate90(unittest.TestCase):
    def test_rotate_90_2by2(self):
        tab = np.array(
            [[1, 2],
             [3, 4]]
        )
        target = np.array(
            [[2, 4],
             [1, 3]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.rotate_90()
        self.assertTrue(array2DEquals(grid.matrix, target), "Rotate 90, matrix 2x2\n" + str(grid.matrix))

    def test_rotate_90_3by3(self):
        tab = np.array(
            [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]]
        )
        target = np.array(
            [[3, 6, 9],
             [2, 5, 8],
             [1, 4, 7]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.rotate_90()
        self.assertTrue(array2DEquals(grid.matrix, target), "Rotate 90, matrix 3x3\n" + str(grid.matrix))

    def test_rotate_90_4by4(self):
        tab = np.array(
            [[1, 2, 3, 4],
             [5, 6, 7, 8],
             [9, 10, 11, 12],
             [13, 14, 15, 16]]
        )
        target = np.array(
            [[4, 8, 12, 16],
             [3, 7, 11, 15],
             [2, 6, 10, 14],
             [1, 5,  9, 13]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.rotate_90()
        self.assertTrue(array2DEquals(grid.matrix, target), "Rotate 90, matrix 4x4\n" + str(grid.matrix))


class TestRotate180(unittest.TestCase):
    def test_rotate_180_2by2(self):
        tab = np.array(
            [[1, 2],
             [3, 4]]
        )
        target = np.array(
            [[4, 3],
             [2, 1]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.rotate_180()
        self.assertTrue(array2DEquals(grid.matrix, target), "Rotate 180, matrix 2x2\n" + str(grid.matrix))

    def test_rotate_180_3by3(self):
        tab = np.array(
            [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]]
        )
        target = np.array(
            [[9, 8, 7],
             [6, 5, 4],
             [3, 2, 1]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.rotate_180()
        self.assertTrue(array2DEquals(grid.matrix, target), "Rotate 180, matrix 3x3\n" + str(grid.matrix))

    def test_rotate_180_4by4(self):
        tab = np.array(
            [[ 1,  2,  3,  4],
             [ 5,  6,  7,  8],
             [ 9, 10, 11, 12],
             [13, 14, 15, 16]]
        )
        target = np.array(
            [[16, 15, 14, 13],
             [12, 11, 10,  9],
             [ 8,  7,  6,  5],
             [ 4,  3,  2,  1]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.rotate_180()
        self.assertTrue(array2DEquals(grid.matrix, target), "Rotate 180, matrix 4x4\n" + str(grid.matrix))


class TestRotate270(unittest.TestCase):
    def test_rotate_270_2by2(self):
        tab = np.array(
            [[1, 2],
             [3, 4]]
        )
        target = np.array(
            [[3, 1],
             [4, 2]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.rotate_270()
        self.assertTrue(array2DEquals(grid.matrix, target), "Rotate 270 matrix 2x2\n" + str(grid.matrix))

    def test_rotate_270_3by3(self):
        tab = np.array(
            [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]]
        )
        target = np.array(
            [[7, 4, 1],
             [8, 5, 2],
             [9, 6, 3]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.rotate_270()
        self.assertTrue(array2DEquals(grid.matrix, target), "Rotate 270, matrix 3x3\n" + str(grid.matrix))

    def test_rotate_270_4by4(self):
        tab = np.array(
            [[ 1,  2,  3,  4],
             [ 5,  6,  7,  8],
             [ 9, 10, 11, 12],
             [13, 14, 15, 16]]
        )
        target = np.array(
            [[13, 9, 5, 1],
             [14, 10, 6, 2],
             [15, 11, 7, 3],
             [16, 12, 8, 4]]
        )
        grid = BaseGrid2048(matrix=tab)
        grid.rotate_270()
        self.assertTrue(array2DEquals(grid.matrix, target), "Rotate 270, matrix 4x4\n" + str(grid.matrix))

