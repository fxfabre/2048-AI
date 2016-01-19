#!/usr/bin/python3
# -*- coding: utf-8 -*-

from AI.Models.simulationNode import SimulationNode
import random
import AI.GameGridLight as GGL
import multiprocessing
import time

NB_PROCESS = 4
AVAILABLE_MOVES = ['down', 'left', 'right', 'up']
NB_SIMULATIONS_MC = 750 # Number of random simulations
DEEP_SIMULATIONS  = 3    # Deep in the tree for MC simulations


class ai_parallelMC:

    def __init__(self):
        self.pool = multiprocessing.Pool(processes=NB_PROCESS)

    def move_next(self, gameBoard, gridHistory, scoreHistory):

        grid = gameBoard.grid.toIntMatrix()
        params = [ [direction, grid] for direction in AVAILABLE_MOVES]

        scores = self.pool.map(runSimulation, params)
        print("(Scores, nb moves) for {0} : {1}".format(AVAILABLE_MOVES, scores))
#        print("Deeps : " + str(nb_simulations_success))
        return getBestMove(scores)


def runSimulation(params):
    firstDirection = params[0]
    gridMatrix = params[1]

    scores = []
    deeps  = []

    grid = GGL.gameGridLight(matrix=gridMatrix)

    for i in range(NB_SIMULATIONS_MC):
        grid_MC = grid.clone()

        deep = 0
        score = 0
        while deep < DEEP_SIMULATIONS:
            if deep == 0:
                direction = firstDirection
            else:
                direction = random.choice( AVAILABLE_MOVES )
            current_score, have_moved = grid_MC.moveTo(direction)
            score += current_score

            if have_moved:
                deep += 1
                grid_MC.add_random_tile()
            else:
                break

        scores.append(score)
        deeps.append(deep)
    return getScore(scores, deeps)

def getScore(scores, deeps):
    return max(scores), sum(deeps)
    return sum(scores)/(len(scores)-1)

def getBestMove(scores):
    best_score = -1
    best_move  = -1
    best_len   = 0

    for i in range(len(scores)):
#        print(i, scores[i])
        score    = scores[i][0]
        nb_moves = scores[i][1]
        if score > best_score:
            best_score = score
            best_move  = AVAILABLE_MOVES[i]
            best_len   = nb_moves
        elif score == best_score:
            if nb_moves > best_len:
                best_score = score
                best_move  = AVAILABLE_MOVES[i]
                best_len   = nb_moves

    print(best_move, best_score, best_len)
    return best_move

