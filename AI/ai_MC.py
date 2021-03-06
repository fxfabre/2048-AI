#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random

import GameGrids.GameGridLight as GGL
from AI.Models.simulationNode import SimulationNode

available_moves = ['down', 'left', 'right', 'up']

class ai_MCsimulation:

    def __init__(self):
        pass

    def move_next(self, gameBoard, gridHistory, scoreHistory):
        if gameBoard.grid.isGameOver:
            return ''

        nbSimulation = 1000
        deepSimulation = 6

        simuationScores = SimulationNode()
        gridMatrix = gameBoard.grid.to_int_matrix()

        for i in range(nbSimulation):
            grid = GGL.GameGridLight(matrix=gridMatrix)

            deep = 0
            score = 0
            directions = []
            while deep < deepSimulation:
                direction = random.choice( available_moves )
#                print("{0} Moving {1}".format('  ' * deep, direction))

                directions.append(direction)
                current_score, have_moved = grid.moveTo(direction)
                score += current_score

                if have_moved:
                    deep += 1
                    grid.add_random_tile()
                else:
                    deep = deepSimulation + 1 # end

            simuationScores.addScore(directions[0], score)

#            print("Action {0:<5} => {1} pts".format(directions[0], score))

        best_move = simuationScores.getBestMove()
#        print("Best move : " + str(best_move))
#        print("")
        return best_move

