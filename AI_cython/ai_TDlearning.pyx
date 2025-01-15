#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math
import random

import numpy as np

from GameGrids.GameGridLight import GameGridLight

##
# Reinforcement learning algo : Temporal differences learning
# http://www.cse.unsw.edu.au/~cs9417ml/RL1/tdlearning.html
#
# Reward : -1 au dernier mouvement
##

ACTIONS = ['left', 'right', 'up', 'down']
ALPHA   = 0.5       # learning rate
GAMMA   = 0.8       # discount factor
EPSILON = 0.2
INF     = 999 * 1000 * 1000


class ai_TDlearning:

    def __init__(self):
        print("Initialize AI Temporal differences learning")

        self.q_values = np.zeros([384, 4]) # 384 paramètres, 4 actions
        self.state_history = None

        # Train AI
        self.Q_learning(EPSILON)

    def move_next(self, gameBoard, gridHistory, scoreHistory):
        grid = gameBoard.grid
        if grid.isGameOver:
            return ''

        current_state = grid.GetState()
        move_to_do = self.ChooseMove(grid, current_state, 0)

        return move_to_do.direction

    def Q_learning(self, epsilon):

        nb_iter = 2000
        while nb_iter > 0:
            nb_iter -= 1
            grid = GameGridLight(nbRows=4, nbColumns=4)
            grid.add_random_tile()
            grid.add_random_tile()

            self.state_history = []
            have_moved = True
            while have_moved:
                current_state = grid.GetState()

                move_to_do = self.ChooseMove(grid, current_state, epsilon)

                if len(move_to_do.direction) > 0:
                    have_moved, score = grid.moveTo(move_to_do.direction)
                    grid.add_random_tile()
                else:
                    have_moved = False

                if have_moved:
                    score = 1
                else:
                    score = -100

                self.Update_Q_values(grid, move_to_do, current_state, score)

                self.state_history.append(current_state)

            if nb_iter % 100 == 0:
                print("Learning iteration : " + str(nb_iter))
            if nb_iter < 5:
                print("Best score : " + str(grid.score))
                print(grid.matrix)

        self.q_values.tofile('q_values.csv', sep=',', format='%d')

    def ChooseMove(self, grid, current_state, epsilon):
        moves = [
            Move(0, 'left' , self.q_values[current_state, 0], grid.canMoveLeft() ),
            Move(1, 'right', self.q_values[current_state, 1], grid.canMoveRight()),
            Move(2, 'up'   , self.q_values[current_state, 2], grid.canMoveUp()   ),
            Move(3, 'down' , self.q_values[current_state, 3], grid.canMoveDown() )
        ]

        # Save available moves and save best score
        scoreMax = -INF
        available_moves = []
        for i in range(4):
            if moves[i].canMove:
                if moves[i].score > scoreMax:
                    scoreMax = moves[i].score
                available_moves.append( moves[i] )

        # Aucun mouvement possible
        if len(available_moves) == 0:
            return Move(0, '', 0, False)

        # take best move : exploitation
        if random.random() > epsilon:
            best_moves = []
            for move in available_moves:
                if move.score == scoreMax:
                    best_moves.append(move)
            idx = random.randrange(0, len(best_moves))
            move_to_do = best_moves[idx]

        # Move at random : exploration
        else:
            idx_move = random.randrange(0, len(available_moves))
            move_to_do = available_moves[idx_move]

        return move_to_do

    def Update_Q_values(self, grid, move_done, current_state, score):
        s = current_state
        a = move_done.idx_direction
        s_prime = grid.GetState()
        q_value_a = self.q_values[s, a]
        q_value_a_prime = self.q_values[s_prime, :].max()

        self.q_values[s, a] += ALPHA * (score + GAMMA * q_value_a_prime - q_value_a)

    def GetState(self, grid):
        total = 0
        # Sum delta X
        for i in range(3):
            for j in range(4):
                if (grid.matrix[i,j] != 0) and (grid.matrix[i+1,j] != 0):
                    diff = math.log2(grid.matrix[i,j]) - math.log2(grid.matrix[i + 1,j])
                    total += abs(diff)
        for i in range(4):
            for j in range(3):
                if (grid.matrix[i,j] != 0) and (grid.matrix[i,j+1] != 0):
                    diff = math.log2(grid.matrix[i,j]) - math.log2(grid.matrix[i,j + 1])
                    total += abs(diff)
        return total


class Move:
    def __init__(self, idx_dir, direction, score, canMove):
        self.idx_direction = idx_dir
        self.direction = direction
        self.score = score # TD learning score
        self.canMove = canMove