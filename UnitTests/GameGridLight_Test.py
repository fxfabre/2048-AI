#!/usr/bin/python3
# -*- coding: utf-8 -*-


import unittest
import numpy as np
import AI.GameGridLight as GGL


class testConstructor(unittest.TestCase):

    def test_Initialisation(self):
        tab = np.array(
            [[0,0,0,0],
             [0,0,0,0],
             [0,0,0,0],
             [0,0,0,0]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertEqual(4, grid.rows)
        self.assertEqual(4, grid.columns)

        grid = GGL.gameGridLight(3, 4)
        self.assertEqual(3, grid.rows)
        self.assertEqual(4, grid.columns)
        self.assertTrue(GGL.array2DEquals(grid.matrix, np.zeros([3,4])))


class TestMoves(unittest.TestCase):

    def test_MoveLeft(self):
        tab = np.array(
            [[2,2,0,0],
             [2,0,2,0],
             [2,0,0,2],
             [0,2,0,2]]
        )
        target = np.array(
            [[4,0,0,0],
             [4,0,0,0],
             [4,0,0,0],
             [4,0,0,0]]
        )
        grid = GGL.gameGridLight(0,0,tab)
        grid.moveLeft()
        self.assertTrue(GGL.array2DEquals(grid.matrix, target), str(grid.matrix) + "\n" + str(target))

        tab = np.array(
            [[2,2,0,2],
             [2,0,4,2],
             [0,2,0,4],
             [4,0,2,2],
             [2,0,2,4]]
        )
        target = np.array(
            [[4,2,0,0],
             [2,4,2,0],
             [2,4,0,0],
             [4,4,0,0],
             [4,4,0,0]]
        )
        grid = GGL.gameGridLight(0,0,tab)
        grid.moveLeft()
        self.assertTrue(GGL.array2DEquals(grid.matrix, target), str(grid.matrix) + "\n" + str(target))

    def test_MoveRight(self):
        tab = np.array(
            [[2,2,0,0],
             [2,0,2,0],
             [2,0,0,2],
             [0,2,0,2]]
        )
        target = np.array(
            [[0,0,0,4],
             [0,0,0,4],
             [0,0,0,4],
             [0,0,0,4]]
        )
        grid = GGL.gameGridLight(0,0,tab)
        grid.moveRight()
        self.assertTrue(GGL.array2DEquals(grid.matrix, target), str(grid.matrix) + "\n" + str(target))

        tab = np.array(
            [[2,2,0,2],
             [2,0,4,2],
             [0,2,0,4],
             [4,0,2,2]]
        )
        target = np.array(
            [[0,0,2,4],
             [0,2,4,2],
             [0,0,2,4],
             [0,0,4,4]]
        )
        grid = GGL.gameGridLight(0,0,tab)
        grid.moveRight()
        self.assertTrue(GGL.array2DEquals(grid.matrix, target), str(grid.matrix) + "\n" + str(target))

    def test_MoveUp(self):
        tab = np.array(
            [[2,2,2,0,0,0],
             [2,0,0,2,2,0],
             [0,2,0,2,0,2],
             [0,0,2,0,2,2]]
        )
        target = np.array(
            [[4,4,4,4,4,4],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0]]
        )
        grid = GGL.gameGridLight(0,0,tab)
        grid.moveUp()
        self.assertTrue(GGL.array2DEquals(grid.matrix, target), "\n" + str(grid.matrix) + "\n" + str(target))

        tab = np.array(
            [[2,2,2,4,0,0],
             [2,4,0,2,2,4],
             [4,2,4,2,4,2],
             [0,4,2,4,2,2]]
        )
        target = np.array(
            [[4,2,2,4,2,4],
             [4,4,4,4,4,4],
             [0,2,2,4,2,0],
             [0,4,0,0,0,0]]
        )
        grid = GGL.gameGridLight(0,0,tab)
        grid.moveUp()
        self.assertTrue(GGL.array2DEquals(grid.matrix, target), "\n" + str(grid.matrix) + "\n" + str(target))

        tab = np.array(
            [[2,2,0,4],
             [2,0,2,0],
             [0,4,0,2],
             [2,2,4,2]]
        )
        target = np.array(
            [[4,2,2,4],
             [2,4,4,4],
             [0,2,0,0],
             [0,0,0,0]]
        )

        grid = GGL.gameGridLight(0,0,tab)
        grid.moveUp()
        self.assertTrue(GGL.array2DEquals(grid.matrix, target), "\n" + str(grid.matrix) + "\n" + str(target))

    def test_MoveDown(self):
        tab = np.array(
            [[2,2,2,0,0,0],
             [2,0,0,2,2,0],
             [0,2,0,2,0,2],
             [0,0,2,0,2,2]]
        )
        target = np.array(
            [[0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [4,4,4,4,4,4]]
        )
        grid = GGL.gameGridLight(0,0,tab)
        grid.moveDown()
        self.assertTrue(GGL.array2DEquals(grid.matrix, target), "\n" + str(grid.matrix) + "\n" + str(target))

        tab = np.array(
            [[2,2,2,4,0,0],
             [2,4,0,2,2,4],
             [4,2,4,2,4,2],
             [0,4,2,4,2,2]]
        )
        target = np.array(
            [[0,2,0,0,0,0],
             [0,4,2,4,2,0],
             [4,2,4,4,4,4],
             [4,4,2,4,2,4]]
        )
        grid = GGL.gameGridLight(0,0,tab)
        grid.moveDown()
        self.assertTrue(GGL.array2DEquals(grid.matrix, target), "\n" + str(grid.matrix) + "\n" + str(target))

        tab = np.array(
            [[2,2,0,4],
             [2,0,2,0],
             [0,4,0,2],
             [2,2,4,2]]
        )
        target = np.array(
            [[0,0,0,0],
             [0,2,0,0],
             [2,4,2,4],
             [4,2,4,4]]
        )
        grid = GGL.gameGridLight(0,0,tab)
        grid.moveDown()
        self.assertTrue(GGL.array2DEquals(grid.matrix, target), "\n" + str(grid.matrix) + "\n" + str(target))


class TestCanMove(unittest.TestCase):

    def test_canMergeUpDown(self):
        # Only one value, assert can't merge
        tab = np.array(
            [[0,0,0,0],
             [0,0,0,0],
             [0,0,0,0],
             [0,0,0,0]]
        )
        for row in range(4):
            for column in range(4):
                grid = GGL.gameGridLight(matrix=tab)
                grid.matrix[row, column] = 2
                self.assertFalse(grid.canMergeUpDown(), "Can merge : \n" + str(grid.matrix))

        tab = np.array(
            [[2,0,0,0],
             [2,0,0,0],
             [0,0,0,0],
             [0,0,0,0]]
        )
        grid = GGL.gameGridLight(matrix=tab)
        self.assertTrue(grid.canMergeUpDown())

        tab = np.array(
            [[0,2,0,0],
             [0,2,0,0],
             [0,0,0,0],
             [0,0,0,0]]
        )
        grid = GGL.gameGridLight(matrix=tab)
        self.assertTrue(grid.canMergeUpDown())

        tab = np.array(
            [[0,0,0,2],
             [0,0,0,2],
             [0,0,0,0],
             [0,0,0,0]]
        )
        grid = GGL.gameGridLight(matrix=tab)
        self.assertTrue(grid.canMergeUpDown())

        tab = np.array(
            [[0,0,0,0],
             [0,0,0,0],
             [0,0,0,2],
             [0,0,0,2]]
        )
        grid = GGL.gameGridLight(matrix=tab)
        self.assertTrue(grid.canMergeUpDown())

        tab = np.array(
            [[3,0,0,0],
             [2,0,0,0],
             [0,0,0,0],
             [0,0,0,0]]
        )
        grid = GGL.gameGridLight(matrix=tab)
        self.assertFalse(grid.canMergeUpDown())

        tab = np.array(
            [[0,0,0,3],
             [2,3,0,0],
             [0,0,0,3],
             [0,0,0,4]]
        )
        grid = GGL.gameGridLight(matrix=tab)
        self.assertFalse(grid.canMergeUpDown())

    def test_canMoveUp(self):
        # Set a number at the top of each column => can't move up
        tab = np.zeros([4,4])
        for column in range(4):
            grid = GGL.gameGridLight(matrix=tab)
            grid.matrix[0, column] = 2
            self.assertFalse(grid.canMoveUp(), "Can move up ! \n" + str(grid.matrix))

        # Set a number everywhere but at the top of each column => can move up
        tab = np.zeros([4,4])
        for row in range(1, 4):
            for column in range(4):
                grid = GGL.gameGridLight(matrix=tab)
                grid.matrix[row, column] = 2
                self.assertTrue(grid.canMoveUp())

        # Set an empty tile everywhere but at the bottom of each column => can move up
        tab = np.array(
            [[1,2,3,4],
             [5,6,7,8],
             [1,2,3,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(matrix=tab)
        self.assertFalse(grid.canMoveDown())
        for row in range(0, 3):
            for column in range(4):
                grid = GGL.gameGridLight(matrix=tab)
                grid.matrix[row, column] = 0
                self.assertTrue(grid.canMoveUp())

        tab = np.array(
            [[1,2,3,4],
             [5,6,7,8],
             [1,2,3,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(matrix=tab)
        self.assertFalse(grid.canMoveUp())
        for row in range(1, 4):
            for column in range(4):
                grid = GGL.gameGridLight(matrix=tab)
                grid.matrix[row, column] = grid.matrix[row -1, column] # copy cell from the one above
                self.assertTrue(grid.canMoveUp())       # merge cells

    def test_canMoveDown(self):
        # Set a number at the bottom of each column => can't move down
        tab = np.zeros([4,4])
        for column in range(4):
            grid = GGL.gameGridLight(matrix=tab)
            grid.matrix[3,column] = 2
            self.assertFalse(grid.canMoveDown(), "Can move down \n" + str(grid.matrix))

        # Set a number everywhere but at the bottom of each column => can move down
        tab = np.zeros([4,4])
        for row in range(0, 3):
            for column in range(4):
                grid = GGL.gameGridLight(matrix=tab)
                grid.matrix[row, column] = 2
                self.assertTrue(grid.canMoveDown())

        # Set an empty tile everywhere but at the top of each column => can move down
        tab = np.array(
            [[1,2,3,4],
             [5,6,7,8],
             [1,2,3,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(matrix=tab)
        self.assertFalse(grid.canMoveDown())
        for row in range(1, 4):
            for column in range(4):
                grid = GGL.gameGridLight(matrix=tab)
                grid.matrix[row, column] = 0
                self.assertTrue(grid.canMoveDown())

        # Set 2 identical consecutive tile in a column => merge cells
        tab = np.array(
            [[1,2,3,4],
             [5,6,7,8],
             [1,2,3,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(matrix=tab)
        self.assertFalse(grid.canMoveDown())
        for row in range(1, 4):
            for column in range(4):
                grid = GGL.gameGridLight(matrix=tab)
                grid.matrix[row, column] = grid.matrix[row -1, column] # copy cell from the one above
                self.assertTrue(grid.canMoveDown())       # merge cells

    def test_canMoveLeft(self):
        # Set a number at the left of each column => can't move left
        tab = np.zeros([4,4])
        for row in range(4):
            grid = GGL.gameGridLight(matrix=tab)
            grid.matrix[row, 0] = 2
            self.assertFalse(grid.canMoveLeft(), "Can move left ! \n" + str(grid.matrix))

        # Set a number everywhere but at the left of each column => can move left
        tab = np.zeros([4,4])
        for row in range(4):
            for column in range(1, 4):
                grid = GGL.gameGridLight(matrix=tab)
                grid.matrix[row, column] = 2
                self.assertTrue(grid.canMoveLeft())

        # Set an empty tile everywhere but at the right of each column => can move left
        tab = np.array(
            [[1,2,3,4],
             [5,6,7,8],
             [1,2,3,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(matrix=tab)
        self.assertFalse(grid.canMoveLeft())
        for row in range(4):
            for column in range(0, 3):
                grid = GGL.gameGridLight(matrix=tab)
                grid.matrix[row, column] = 0
                self.assertTrue(grid.canMoveLeft())

        tab = np.array(
            [[1,2,3,4],
             [5,6,7,8],
             [1,2,3,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(matrix=tab)
        self.assertFalse(grid.canMoveLeft())
        for row in range(4):
            for column in range(1, 4):
                grid = GGL.gameGridLight(matrix=tab)
                grid.matrix[row, column] = grid.matrix[row, column-1] # copy cell from the one above
                self.assertTrue(grid.canMoveLeft(), "should move left\n" + str(grid.matrix))       # merge cells


class TestPrivateFunctions(unittest.TestCase):

    def test_is_full(self):
        tab = np.array(
            [[0,0,0,0],
             [0,0,0,0],
             [0,0,0,0],
             [0,0,0,0]]
        )
        grid = GGL.gameGridLight(0,0,tab)
        self.assertFalse(grid.is_full())

        tab = np.array(
            [[2,2,2,2],
             [2,2,2,2],
             [2,2,2,2],
             [2,2,2,2]]
        )
        grid = GGL.gameGridLight(0,0,tab)
        self.assertTrue(grid.is_full())

        tab = np.array(
            [[2,4,2,4],
             [2,4,2,4],
             [2,4,2,4],
             [2,4,2,4]]
        )
        grid = GGL.gameGridLight(0,0,tab)
        self.assertTrue(grid.is_full())

        tab = np.array(
            [[1,1,3,4],
             [5,6,7,8],
             [1,2,3,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertTrue(grid.is_full())

        for row in range(4):
            for col in range(4):
                loc_tab = np.array(tab)
                loc_tab[row, col] = 0
                grid = GGL.gameGridLight(0, 0, loc_tab)
                self.assertFalse(grid.is_full(), "Error at ({0}, {1})\n{2}".format(row, col, grid.matrix))

    def test_is_game_over_lines(self):
        tab = np.array(
            [[0,0,0,0],
             [0,0,0,0],
             [0,0,0,0],
             [0,0,0,0]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[2,2,2,2],
             [2,2,2,2],
             [2,2,2,2],
             [2,2,2,2]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,2,1,2],
             [3,4,3,4],
             [1,2,1,2],
             [3,4,3,4]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertTrue(grid.is_game_over())

        tab = np.array(
            [[1,1,3,4],
             [5,6,7,8],
             [1,2,3,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,2,2,4],
             [5,6,7,8],
             [1,2,3,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,2,3,3],
             [5,6,7,8],
             [1,2,3,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,2,3,4],
             [5,5,7,8],
             [1,2,3,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,2,3,4],
             [5,6,6,8],
             [1,2,3,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,2,3,4],
             [5,6,7,7],
             [1,2,3,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,2,3,4],
             [5,6,7,8],
             [1,1,3,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,2,3,4],
             [5,6,7,8],
             [1,2,2,4],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,2,3,4],
             [5,6,7,8],
             [1,2,3,3],
             [5,6,7,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,2,3,4],
             [5,6,7,8],
             [1,2,3,4],
             [5,5,7,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,2,3,4],
             [5,6,7,8],
             [1,2,3,4],
             [5,6,6,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,2,3,4],
             [5,6,7,8],
             [1,2,3,4],
             [5,6,7,7]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

    def test_is_game_over_column(self):

        tab = np.array(
            [[1,5,1,5],
             [1,6,2,6],
             [3,7,3,7],
             [4,8,4,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,5,1,5],
             [2,6,2,6],
             [2,7,3,7],
             [4,8,4,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,5,1,5],
             [2,6,2,6],
             [3,7,3,7],
             [3,8,4,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,5,1,5],
             [2,5,2,6],
             [3,7,3,7],
             [4,8,4,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,5,1,5],
             [2,6,2,6],
             [3,6,3,7],
             [4,8,4,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,5,1,5],
             [2,6,2,6],
             [3,7,3,7],
             [4,7,4,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,5,1,5],
             [2,6,1,6],
             [3,7,3,7],
             [4,8,4,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,5,1,5],
             [2,6,2,6],
             [3,7,2,7],
             [4,8,4,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,5,1,5],
             [2,6,2,6],
             [3,7,3,7],
             [4,8,3,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,5,1,5],
             [2,6,2,5],
             [3,7,3,7],
             [4,8,4,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,5,1,5],
             [2,6,2,6],
             [3,7,3,6],
             [4,8,4,8]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

        tab = np.array(
            [[1,5,1,5],
             [2,6,2,6],
             [3,7,3,7],
             [4,8,4,7]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertFalse(grid.is_game_over())

    def test_add_random_tile(self):

        tab = np.array(
            [[0,0,0,0],
             [0,0,0,0],
             [0,0,0,0],
             [0,0,0,0]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        grid.add_random_tile()
        self.assertTrue(grid.matrix.sum() > 0)

        tab = np.array(
            [[2,2,2,2],
             [2,2,2,2],
             [2,2,2,2],
             [2,2,2,2]]
        )
        grid = GGL.gameGridLight(0, 0, tab)
        self.assertRaises(grid.add_random_tile())

        tab = np.array(
            [[1,1,1,1],
             [1,1,1,1],
             [1,1,1,1],
             [1,1,1,1]]
        )
        for row in range(4):
            for column in range(4):
                grid = GGL.gameGridLight(0, 0, tab)
                grid.matrix[row, column] = 0
                grid.add_random_tile()
                self.assertTrue(grid.matrix.sum() > 16)


class TestTools(unittest.TestCase):

    def test_ArrayDEquals(self):
        a = np.array(
            [[0,0,0],
             [0,0,0]]
        )
        b = np.array(
            [[0,0],
             [0,0]]
        )
        self.assertFalse(GGL.array2DEquals(a, b))

        b = np.array(
            [[0,0,0],
             [0,0,0],
             [0,0,0]]
        )
        self.assertFalse(GGL.array2DEquals(a, b))

        b = np.array(
            [[0,0,0],
             [0,0,0]]
        )
        self.assertTrue(GGL.array2DEquals(a, b))

        a = np.array(
            [[1,3,0],
             [0,4,0]]
        )
        b = np.array(
            [[1,3,0],
             [1,4,0]]
        )
        self.assertFalse(GGL.array2DEquals(a, b))

        a = np.array(
            [[4,3,0],
             [0,4,0]]
        )
        b = np.array(
            [[1,3,0],
             [0,4,0]]
        )
        self.assertFalse(GGL.array2DEquals(a, b))

        a = np.array(
            [[1,3,0],
             [0,4,9]]
        )
        b = np.array(
            [[1,3,0],
             [0,4,0]]
        )
        self.assertFalse(GGL.array2DEquals(a, b))

        a = np.array(
            [[1,3,0],
             [0,4,0]]
        )
        b = np.array(
            [[1,3,0],
             [0,4,0]]
        )
        self.assertTrue(GGL.array2DEquals(a, b))


if __name__ == '__main__':
    unittest.main()

