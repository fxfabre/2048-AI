#!/usr/bin/python3
# -*- coding: utf-8 -*-

import GUI.game2048_score as GS
import GUI.game2048_grid as GG

from AI.ai_random import ai_random
from AI.ai_bestScoreNextMove import ai_bestScoreNextMove
from AI.ai_MC import ai_MCsimulation
from AI.ai_parallelMC import ai_parallelMC


class gameBoard2048:

    def __init__(self, game, **kw):
        # Game2048 object, UI
        self.game2048 = game

        # get 2048's grid
        self.grid = GG.Game2048Grid(game, **kw)

        # score subcomponents
        self.score = GS.Game2048Score(game, **kw)
        self.highscore = GS.Game2048Score(game, label="Highest:", **kw)

        # set score callback method
        self.grid.set_score_callback(self.update_score)

        # Init AI
        self._ai = ai_parallelMC()
        self._scoreHistory = []
        self._gridHistory = []

    def reset(self):
        # reset grid
        self.grid.reset_grid()

        # reset score
        self.score.reset_score()

    def update_score (self, value, mode="add"):
        """
            updates score along @value and @mode;
        """
        # relative mode
        if str(mode).lower() in ("add", "inc", "+"):
            # increment score value
            self.score.add_score(value)

        # absolute mode
        else:
            # set new value
            self.score.set_score(value)

        # update high score
        self.highscore.high_score(self.score.get_score())

    def slot_keypressed(self, tk_event=None, *args, **kw):
        if tk_event:
            self.move_tile(tk_event.keysym)

    def move_tiles_left(self):
        return self.move_tile('left')

    def move_tiles_right(self):
        return self.move_tile('right')

    def move_tiles_up(self):
        return self.move_tile('up')

    def move_tiles_down(self):
        return self.move_tile('down')

    def move_tile(self, direction):
        """
            keyboard input events manager;
        """
        # action slot multiplexer
        _slot = {
            "left" : self.grid.move_tiles_left,
            "right": self.grid.move_tiles_right,
            "up"   : self.grid.move_tiles_up,
            "down" : self.grid.move_tiles_down
        }.get(direction.lower())

        # got some redirection?
        if callable(_slot):
            _slot()

        # Update user interface
#        self.grid.update()

    def play_ia(self, *args, **kw):
        self.grid.isGameOver = False

        i = 0
        nextMove = 'up'
        while len(nextMove) > 0:
            i += 1

            # Add history (grid and score) data
            self._scoreHistory.append( self.score.get_score() )
            self._gridHistory.append( self.grid.toIntMatrix() )

            # Get next move : 'left', 'right', 'up' or 'down'
            nextMove = self._ai.move_next(self, self._gridHistory, self._scoreHistory)

            # Simulate keyboard event
            self.move_tile(nextMove)
            self.grid.update()

#            if i > 3:
#                nextMove = ''
        print("Game over in {0} iterations, score = {1}".format(i+1, self.score.get_score()))

    def __str__(self):
        returnString = ['']

        returnString.append("### Game Board ###")

        # HighScore :
        returnString.append("# HighScore : {0}".format(self.highscore.get_score()))

        # Score :
        returnString.append("# Score : {0}".format(self.score.get_score()))

        # Grid :
        for line in str(self.grid.toIntMatrix()).split('\n'):
            returnString.append("# {0}".format(line))

        returnString.append('')

        return '\n'.join(returnString)
