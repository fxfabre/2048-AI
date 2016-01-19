#!/usr/bin/python3
# -*- coding: utf-8 -*-


from AI.Models.simulationNode import SimulationNode
import random
import AI.GameGridLight as GGL
import multiprocessing
import time
import numpy as np


AVAILABLE_MOVES = ['down', 'left', 'right', 'up']
DEEP = 2

class ai_minimax:

    def __init__(self):
        print("Initialize AI minimax")
        pass

    def move_next(self, gameBoard, gridHistory, scoreHistory):
        if gameBoard.grid.isGameOver:
            return ''

        direction, _ = evalMoveTo(gameBoard, DEEP)
        return direction


def evalMoveTo(par_grid:GGL.gameGridLight, deep:int):
    if deep == 0:
        return par_grid.getScore()

    scores = []
    for direction in AVAILABLE_MOVES:
        loc_grid = par_grid.clone()
        loc_grid.moveTo(direction)
        score = evalAddTile(loc_grid, deep -1)
        scores.append((direction, score))

    # return argmax( scores )
    best_direction = ''
    best_score = -1
    for direction, score in scores:
        if score > best_score:
            best_direction = direction
            best_score = score

    return best_direction, best_score

def evalAddTile(par_grid:GGL.gameGridLight, deep:int):
    if deep == 0:
        return par_grid.getScore()

    scores = np.zeros(2 * par_grid.rows * par_grid.columns)
    for x in range(par_grid.columns):
        for y in range(par_grid.rows):
            if not par_grid.canAddTile(x,y):
                continue
            for tileToAdd in [2,4]:
                loc_grid = par_grid.clone()
                loc_grid.add_tile(x, y, tileToAdd)
                _, score = evalMoveTo(loc_grid, deep -1) # should be deep, not deep -1, but it doesn't matter

                index = coord_to_index(loc_grid, x, y, tileToAdd)
                scores[index] = score

    # min score : suppose the added tile is at the worst position
    return scores.min()

def coord_to_index(grid, x, y, tileToAdd):
    # X,  Y,  tile  => index
    # 0,  0,  2     => 0
    # 0,  3,  2     => 3
    # 3,  0,  2     => 12
    # 3,  3,  2     => 15
    # 0,  0,  4     => 16
    return (x * grid.rows + y) + ( (-1 + tileToAdd/2) * 16 )

def index_to_coord(grid, index):
    x = (index % 16) // grid.rows
    y = index % grid.rows
    valeur = (index > 15) and 4 or 2
    return x, y, valeur


