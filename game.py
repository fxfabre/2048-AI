#!/usr/bin/python3
# -*- coding: utf-8 -*-


import random
import tkinter as TK
import tkinter.messagebox as MB
from tkinter import ttk

from GUI.gameBoard2048 import gameBoard2048


class Game2048(TK.Tk):

    # component disposal padding
    PADDING = 10

    # number of tiles to show at startup
    START_TILES = 2

    def __init__ (self, **kw):
        # super class inits
        TK.Tk.__init__(self)

        # widget inits
        self.init_widget(**kw)

        # prevent from accidental displaying
        self.withdraw()

    def center_window(self, tk_event=None, *args, **kw):
        """
            tries to center window along screen dims;
            no return value (void);
        """

        # ensure dims are correct
        self.update_idletasks()

        # window size inits
        _width = self.winfo_reqwidth()
        _height = self.winfo_reqheight()
        _screen_width = self.winfo_screenwidth()
        _screen_height = self.winfo_screenheight()

        # make calculations
        _left = (_screen_width - _width) // 2
        _top = (_screen_height - _height) // 2

        # update geometry
        self.geometry("+{x}+{y}".format(x=_left, y=_top))

    def init_widget(self, **kw):
        """
            widget's main inits;
        """

        # main window inits
        self.title("2048")
        self.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.resizable(width=False, height=False)

        # look'n'feel
        ttk.Style().configure(".", font="sans 10")

        # inits
        _pad = self.PADDING

        # get 2048's gameBoard = grid, score & highscore
        self.gameBoard = gameBoard2048(self, **kw)

        # layout inits
        self.gameBoard.grid.pack(side=TK.TOP, padx=_pad, pady=_pad)
        self.gameBoard.score.pack(side=TK.LEFT)
        self.gameBoard.highscore.pack(side=TK.LEFT)

        # play button
        ttk.Button(
            self, text="Play !", command=self.gameBoard.play_ia,
        ).pack(side=TK.RIGHT, padx=_pad, pady=_pad)

        # new game button
        ttk.Button(
            self, text="New Game", command=self.new_game,
        ).pack(side=TK.RIGHT)

    def new_game(self, *args, **kw):
        """
            new game inits;
        """

        # no events now
        self.unbind_all("<Key>")

        # reset grid and score
        self.gameBoard.reset()

        # make random tiles to appear
        for n in range(self.START_TILES):
            self.after(
                100 * random.randrange(3, 7), self.gameBoard.grid.pop_tile
            )

        # bind events
        self.bind_all("<Key>", self.gameBoard.slot_keypressed)

    def quit_app (self, **kw):
        """
            quit app dialog;
        """
        self.quit()
        return

        # ask before actually quitting
        if MB.askokcancel("Question", "Quit game?", parent=self):
            self.quit()

    def run (self, **kw):
        """
            actually runs the game;
        """

        # show up window
        self.center_window()
        self.deiconify()

        # init new game
        self.new_game(**kw)

        # enter the loop
        self.mainloop()


# launching the game
if __name__ == "__main__":
    Game2048().run()
