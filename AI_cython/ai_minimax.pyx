#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

import GameGrids.GameGridLight as GGL

AVAILABLE_MOVES = ['down', 'left', 'right', 'up']
DEEP = 2


class ai_minimax:

    def __init__(self):
        print("Initialize AI minimax")

    def move_next(self, gameBoard, gridHistory, scoreHistory):
        if gameBoard.grid.isGameOver:
            return ''

#        print("\n\n_______________________________________________\n\n" )

        gridMatrix = gameBoard.grid.to_int_matrix()
#        print(gridMatrix)
        grid = GGL.GameGridLight(matrix=gridMatrix)

        direction, _ = evalMoveTo(grid, DEEP)
        print("Moving to " + direction)
        return direction


def evalMoveTo(par_grid: GGL.GameGridLight, deep: int):
    if deep == 0:
        return '', par_grid.getScore()
#    print("evalMoveTo Deep " + str(deep))

    scores = []
    for direction in AVAILABLE_MOVES:
        loc_grid = par_grid.clone()
        score, have_moved = loc_grid.moveTo(direction)
#        print("{0} => {1} pts".format(direction, score))
#        print(loc_grid.matrix)

        if have_moved:
            score = evalAddTile(loc_grid, deep -1)
            scores.append((direction, score))
        else:
            scores.append((direction, -1))

    # return argmax( scores )
    best_direction = ''
    best_score = -1
    for direction, score in scores:
        if score > best_score:
            best_direction = direction
            best_score = score

#    print("Best direction : " + str(best_direction))
    return best_direction, best_score

def evalAddTile(par_grid: GGL.GameGridLight, deep: int):
    if deep == 0:
        return par_grid.getScore()
#    print("evalAddTile Deep " + str(deep))

    scores = np.zeros(2 * par_grid.rows * par_grid.columns) + 1000000000  # + inf
    for x in range(par_grid.columns):
        for y in range(par_grid.rows):
            if not par_grid.canAddTile(x,y):
                continue
            for tileToAdd in [2,4]:
#                print("Add tile {0} at ({1}, {2})".format(tileToAdd, x, y))
                loc_grid = par_grid.clone()
                loc_grid.add_tile(x, y, tileToAdd)
#                print("Matrix")
                _, score = evalMoveTo(loc_grid, deep) # Yes, keep same deep here.
#                print("Add tile {0} at ({1}, {2}) => {3} pts".format(tileToAdd, x, y, score))

                index = coord_to_index(loc_grid, x, y, tileToAdd)
                scores[index] = score

    # min score : suppose the added tile is at the worst position
#    print( scores )
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


