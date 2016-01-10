#!/usr/bin/python3
# -*- coding: utf-8 -*-

import AI.GameGridLight as GGL


class ai_bestScoreNextMove:

    Available_moves = ['down', 'left', 'right', 'up']

    def __init__(self):
        pass

    def move_next(self, gameBoard, gridHistory, scoreHistory):
        if gameBoard.grid.isGameOver:
            return ''

        gridMatrix = gameBoard.grid.toIntMatrix()

        best_score = -1
        best_move  = ''
        for direction in ai_bestScoreNextMove.Available_moves:
            gameGrid = GGL.gameGridLight(matrix=gridMatrix)
            current_score, have_moved = gameGrid.moveTo(direction)

            if (have_moved) and (current_score > best_score):
                best_score = current_score
                best_move = direction

        print("{0:<5} with score {1}".format(best_move, best_score))
        return best_move
