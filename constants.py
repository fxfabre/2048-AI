#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

NB_ROWS = 3
NB_COLS = 3
GRID_MAX_VAL = 6

if sys.platform == 'linux':
    SAVE_DIR = ''
else:
    SAVE_DIR = '.'

RECORD_MOVES = True
FILE_RECORD_MOVES = 'moves_history.csv'
