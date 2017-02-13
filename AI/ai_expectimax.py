#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

import GameGrids.GameGridLight as GGL

AVAILABLE_MOVES = ['down', 'left', 'right', 'up']
DEEP = 3
INF = 1000000000

class ai_expectimax:

    def __init__(self):
        print("Initialize AI expectimax")

    def move_next(self, gameBoard, gridHistory, scoreHistory):
        if gameBoard.grid.isGameOver:
            return ''

        gridMatrix = gameBoard.grid.to_int_matrix()
        grid = GGL.GameGridLight(matrix=gridMatrix)

        direction, _ = evalMoveTo(grid, DEEP)
        return direction


def evalMoveTo(par_grid: GGL.GameGridLight, deep: int):
    if deep == 0:
        return '', par_grid.getScore()

    scores = []
    for direction in AVAILABLE_MOVES:
        loc_grid = par_grid.clone()
        score, have_moved = loc_grid.moveTo(direction)

        if have_moved:
            score = evalAddTile(loc_grid, deep -1)
            scores.append((direction, score))
        else:
            scores.append((direction, -1))

    best_direction = ''
    best_score = -1
    for direction, score in scores:
        if score > best_score:
            best_direction = direction
            best_score = score

    return best_direction, best_score

def evalAddTile(par_grid: GGL.GameGridLight, deep: int):
    if deep == 0:
        return par_grid.getScore()

    scores = []
    for x in range(par_grid.columns):
        for y in range(par_grid.rows):
            if not par_grid.canAddTile(x,y):
                continue
            for tileToAdd in [2,4]:
                loc_grid = par_grid.clone()
                loc_grid.add_tile(x, y, tileToAdd)
                _, score = evalMoveTo(loc_grid, deep) # Yes, keep same deep here.
                scores.append(score)

    arrayScores = np.array( scores )
    avgScore = arrayScores.mean()
    return avgScore

