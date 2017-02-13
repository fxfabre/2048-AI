#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
from GameGrids.baseGrid2048 import BaseGrid2048, array2DEquals
import constants

class GameGridLight(BaseGrid2048):

    def clone(self):
        return GameGridLight(matrix=self.matrix)

    ###############
    # Moves
    ###############
    def moveTo(self, direction=""):
        direction = direction.lower()

        if direction == 'left':
            return self.moveLeft()
        elif direction == 'right':
            return self.moveRight()
        elif direction == 'up':
            return self.moveUp()
        elif direction == 'down':
            return self.moveDown()
        else:
            raise Exception("Unknown direction : " + direction)

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
                        self.matrix[_row, _column] *= 2
                        self.matrix[_row, _column_next] = 0
                        score += _at[_row, _column]
                        have_moved = True
                    break

        # Step 2 : Move tiles
        for _row in range(self.rows):

            # Skip columns with > 0 tile
            _first_empty_column = self.columns  # après la dernière colonne
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
                        self.matrix[_row, _column] *= 2
                        self.matrix[_row, _column_next] = 0
                        score += _at[_row, _column]
                        have_moved = True
                    break

        # Step 2 : Move tiles
        for _row in range(self.rows):

            # Skip columns with > 0 tile
            _first_empty_column = -1  # avant la premiere colonne
            for _column in range(self.columns - 1, -1, -1):
                if _at[_row, _column] == 0:
                    _first_empty_column = _column
                    break

            # Move tiles
            for _column in range(_first_empty_column - 1, -1, -1):
                if _at[_row, _column] > 0:
                    self.matrix[_row, _first_empty_column] = _at[_row, _column]
                    _at[_row, _column] = 0
                    _first_empty_column -= 1
                    have_moved = True

        return score, have_moved

    def moveUp(self):
        score = 0
        have_moved = False

        # Step 1 : fusion of equal tiles
        for _column in range(self.columns):
            for _row in range(self.rows - 1):

                # find same tile
                for _row_next in range(_row + 1, self.rows):

                    if self.matrix[_row_next, _column] == 0:
                        continue
                    if self.matrix[_row, _column] == self.matrix[_row_next, _column]:
                        self.matrix[_row, _column] *= 2
                        self.matrix[_row_next, _column] = 0
                        score += self.matrix[_row, _column]
                        have_moved = True
                    break

        # Step 2 : Move tiles
        for _column in range(self.columns):

            # Skip columns with > 0 tile
            _first_empty_row = self.rows
            for _row in range(self.rows - 1):
                if self.matrix[_row, _column] == 0:
                    _first_empty_row = _row
                    break

            # Move tiles
            for _row in range(_first_empty_row + 1, self.rows):
                if self.matrix[_row, _column] > 0:
                    self.matrix[_first_empty_row, _column] = self.matrix[_row, _column]
                    self.matrix[_row, _column] = 0
                    _first_empty_row += 1
                    have_moved = True

        return score, have_moved

    def moveDown(self):
        score = 0
        have_moved = False

        # Step 1 : fusion of equal tiles
        for _column in range(self.columns):
            for _row in range(self.rows - 1, 0, -1):

                # find same tile
                for _row_next in range(_row - 1, -1, -1):

                    if self.matrix[_row_next, _column] == 0:
                        continue
                    if self.matrix[_row, _column] == self.matrix[_row_next, _column]:
                        self.matrix[_row, _column] *= 2
                        self.matrix[_row_next, _column] = 0
                        score += self.matrix[_row, _column]
                        have_moved = True
                    break

        # Step 2 : Move tiles
        for _column in range(self.columns):

            # Skip columns with > 0 tile
            _first_empty_row = -1  # avant la premiere ligne
            for _row in range(self.rows - 1, -1, -1):
                if self.matrix[_row, _column] == 0:
                    _first_empty_row = _row
                    break

            # Move tiles
            for _row in range(_first_empty_row - 1, -1, -1):
                if self.matrix[_row, _column] > 0:
                    self.matrix[_first_empty_row, _column] = self.matrix[_row, _column]
                    self.matrix[_row, _column] = 0
                    _first_empty_row -= 1
                    have_moved = True

        return score, have_moved

    ################

    def add_random_tile(self):
        """
            pops up a random tile at a given place;
        """
        # ensure we yet have room in grids
        if self.is_full():
            return

        _value = random.choice([2, 2, 2, 4, 2, 2, 2, 2, 2, 2])
        _row, _column = self.get_available_box()
        self.set_tile(_row, _column, _value)

    @property
    def max_value(self):
        return constants.GRID_MAX_VAL
        return self.rows + self.columns + 1

    def __str__(self):
        return str(self.matrix)

    def __eq__(self, other):
        return array2DEquals(self.matrix, other.matrix)

