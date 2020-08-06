#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import sys

from AI.ai_base import BaseAi


class ai_random(BaseAi):

    def __init__(self):
        self._available_moves = ['left', 'right', 'up', 'down']
        file = open("LogPython.log", 'w')
        self.logFile = file

    def GetMove(self, grid, history):
        # grid = game_board.grid
        if grid.isGameOver:
            return ''

        direction = random.choice(self._available_moves)

        return direction

    def __del__(self):
        self.logFile.close()
        self.logFile = sys.stdout

