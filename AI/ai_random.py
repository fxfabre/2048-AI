#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import sys
from time import sleep


class ai_random:

    def __init__(self):
        self._available_moves = ['left', 'right', 'up', 'down']
        file = open("LogPython.log", 'w')
        self.logFile = file

    def move_next(self, gameBoard, gridHistory, scoreHistory):
        grid = gameBoard.grid
        if grid.isGameOver:
            return ''

        direction = random.choice( self._available_moves )

        sleep(0.01)
        return direction

    def __del__(self):
        self.logFile.close()
        self.logFile = sys.stdout

