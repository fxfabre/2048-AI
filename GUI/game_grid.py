#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    tkGAME - all-in-one Game library for Tkinter

    Generic Game Grid and subcomponents

    Copyright (c) 2014+ Raphaël Seban <motus@laposte.net>

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see http://www.gnu.org/licenses/
"""


import tkinter as TK
import numpy as np

# module utility function
def normalize (value, minimum=1):
    r"""
        normalizes value along constraints;

        returns UINT of @value or at least @minimum;
    """
    return max(abs(int(minimum)), abs(int(value)))


class GameGrid (TK.Canvas):
    r"""
        Generic Game Grid component;
    """
    # background color
    BGCOLOR = "white"

    # foreground color
    FGCOLOR = "grey"

    # nb of rows and columns in grid
    ROWS = 3
    COLUMNS = 3

    # thickness of a line stroke
    THICKNESS = 8   # pixels

    # default global config values
    CONFIG = {
        "background": BGCOLOR,
        "highlightthickness": 0,
        "width" : 500,  # pixels
        "height": 500,  # pixels
    }

    def __init__ (self, master, **kw):
        # member inits
        self.CONFIG = self.CONFIG.copy()
        self.CONFIG.update(kw)

        # super class inits
        TK.Canvas.__init__(self, master)
        self.configure(**self._only_tk(self.CONFIG))

        # public members
        self.rows    = kw.get("rows"   , self.ROWS   )
        self.columns = kw.get("columns", self.COLUMNS)
        self.bgcolor = kw.get("bgcolor", self.BGCOLOR)
        self.fgcolor = kw.get("fgcolor", self.FGCOLOR)
        self.thickness = kw.get("thickness", self.THICKNESS)

        # private member inits
        self.__tk_owner = master
        self.__tiles = dict()
        self.__matrix = GridMatrix(self.rows, self.columns)
        self.__cell_size = GridCellSize(self)

        # widget inits
        self.init_widget(**self.CONFIG)

    ####################
    # My functions
    ####################
    def toIntMatrix(self):
        N = len(self.matrix.matrix)
        matrix = np.zeros([N, N])
        for i in range(N):
            for j in range(N):
                tile = self.matrix.get_object_at(i,j)
                if tile:
                    matrix[i,j] = tile.value
        return matrix

    #####################
    # Private functions
    #####################
    def _only_tk (self, kw):
        r"""
            private method def;

            filters external keywords to suit tkinter init options;

            returns filtered dict() of keywords;
        """
        # inits
        _dict = dict()

        # $ 2014-03-24 RS $
        # Caution:
        # TK widget *MUST* be init'ed before calling _only_tk() /!\
        # self.configure() needs self.tk to work well
        if hasattr(self, "tk") and hasattr(self, "configure"):
            _attrs = set(self.configure().keys()) & set(kw.keys())
            for _key in _attrs:
                _dict[_key] = kw.get(_key)
        return _dict

    ###################
    # Clear functions
    ###################
    def clear_all (self, tk_event=None, *args, **kw):
        r"""
            clears up all critical members;
        """
        # clear grid
        self.clear_grid()

        # clear tiles collection
        self.clear_tiles()

        # clear matrix
        self.matrix.reset_matrix()

    def clear_grid (self, tk_event=None, *args, **kw):
        r"""
            clears up grid canvas entirely;
        """
        # clear grid
        self.delete(TK.ALL)

    def clear_tiles (self, tk_event=None, *args, **kw):
        r"""
            clears up tiles collection entirely;
        """
        # clear tiles
        self.tiles.clear()

    def remove_tile (self, tile_id):
        r"""
            removes silently if exists;
        """
        self.tiles.pop(tile_id, None)

    def reset_grid (self, tk_event=None, *args, **kw):
        r"""
            clears up and redraws grid entirely;
        """
        # clear all
        self.clear_all()

        # canvas dims
        _grid_width, _grid_height = self.grid_size

        # point of origin
        _x0, _y0 = self.xy_origin

        # thickness
        _thickness = self.thickness

        # foreground color
        _fg = self.fgcolor

        # draw rectangle
        self.create_rectangle(
            _x0, _y0, _grid_width, _grid_height,
            outline=_fg, width=_thickness,
        )

        # draw vertical lines
        for _column in range(1, self.columns):
            _x = _x0 + _column * (self.cell_size.width + _thickness)
            self.create_line(
                _x, 0, _x, _grid_height,
                fill=_fg, width=_thickness,
            )

        # draw horizontal lines
        for _row in range(1, self.rows):
            _y = _y0 + _row * (self.cell_size.height + _thickness)
            self.create_line(
                0, _y, _grid_width, _y,
                fill=_fg, width=_thickness,
            )

    ###################
    def get_coords (self, row, column, centered=False):
        r"""
            calculates canvas (x, y) coordinates from grid matrix
            (row, column) pair;
        """
        # get (left, top) coordinates
        _x, _y = self.cell_size.xy_left_top(row, column)

        # center coords?
        if centered:
            _x += self.cell_size.width // 2
            _y += self.cell_size.height // 2
        return (_x, _y)

    def init_widget (self, **kw):
        r"""
            widget's main inits;
        """
        # put your own code in subclass
        pass

    def is_full (self):
        r"""
            evaluates available room in grid;
        """
        return len(self.tiles) >= self.max_tiles

    def is_tile (self, row, column):
        r"""
            determines whether canvas item at (row, column) is of
            tile type or not;
        """
        # inits coordinates
        _x, _y = self.get_coords(row, column, centered=True)

        # get canvas item id
        _item_id = self.find_overlapping(_x, _y, _x, _y)

        # is a tile?
        return bool(_item_id in self.tiles)

    def register_tile (self, tile_id, tile_object, raise_error=False):
        r"""
            registers new tile in tiles dict();
        """
        # new tile id?
        if tile_id not in self.tiles:
            # register tile object
            self.tiles[tile_id] = tile_object
        elif raise_error:
            # should *NOT* override already existing tile
            raise KeyError(
                "tile id '{tid}' is already registered."
                .format(tid=tile_id)
            )

    ################
    # Properties
    ################
    @property
    def columns (self):
        r"""
            returns grid's current nb of columns;
        """
        return self.__columns

    @columns.setter
    def columns (self, value):
        self.__columns = normalize(value)

    @columns.deleter
    def columns (self):
        del self.__columns

    @property
    def grid_height (self):
        r"""
            returns grid's height;
        """
        return self.winfo_reqheight()

    @property
    def grid_size (self):
        r"""
            returns (real_width, real_height) pair;
        """
        # must adjust along thickness
        return (
            (self.grid_width - self.half_high),
            (self.grid_height - self.half_high)
        )

    @property
    def grid_width (self):
        r"""
            returns grid's width;
        """
        return self.winfo_reqwidth()

    @property
    def cell_size (self):
        r"""
            returns internal GridCellSize object instance;
        """
        return self.__cell_size

    @property
    def half_high (self):
        r"""
            returns half thickness, high value;
        """
        return round(0.1 + self.thickness / 2)

    @property
    def half_low (self):
        r"""
            returns half thickness, low value;
        """
        return self.thickness // 2

    @property
    def matrix (self):
        r"""
            returns internal matrix object;
        """
        return self.__matrix

    @matrix.setter
    def matrix(self, value):
        self.__matrix = value

    @property
    def max_tiles (self):
        r"""
            returns maximum number of tiles currently admitted;
        """
        return self.rows * self.columns

    @property
    def owner (self):
        r"""
            returns ref to private tk_owner;
        """
        return self.__tk_owner

    @property
    def rows (self):
        r"""
            returns grid's current nb of rows;
        """
        return self.__rows

    @rows.setter
    def rows (self, value):
        self.__rows = normalize(value)

    @rows.deleter
    def rows (self):
        del self.__rows

    @property
    def thickness (self):
        r"""
            returns grid's line stroke thickness;
        """
        return self.__thickness

    @thickness.setter
    def thickness (self, value):
        self.__thickness = normalize(value, minimum=0)

    @thickness.deleter
    def thickness (self):
        del self.__thickness

    @property
    def tiles (self):
        r"""
            returns internal tiles collection;
        """
        return self.__tiles

    @property
    def xy_origin (self):
        r"""
            returns (x0, y0) point of origin of grid drawings;
        """
        # must adjust along thickness
        _x0 = _y0 = self.half_low
        return (_x0, _y0)

    @property
    def xy_center (self):
        r"""
            returns (x, y) coordinates of canvas' center point;
        """
        return (self.grid_width // 2, self.grid_height // 2)


class GridAnimation (TK.Frame):
    r"""
        GridAnimation - GameGrid subcomponent;
    """

    def __init__ (self, master=None):
        # super class inits
        TK.Frame.__init__(self, master)

        # public member inits
        self.owner = master

        # private member inits
        self.__pid = 0
        self.__animation_kw = dict()
        self.__callback = None
        self.__callback_args = tuple()
        self.__callback_kw = dict()

    @property
    def keywords (self):
        r"""
            returns internal animation's keywords;
        """
        return self.__animation_kw

    def register (self, callback, *args, **kw):
        r"""
            registers callback function/method with its own
            arguments and keywords;

            returns True on success, False otherwise;
        """
        if callable(callback):
            # init callback
            self.__callback = callback

            # init args and kw
            self.__callback_args = args
            self.__callback_kw = kw

            # success
            return True

        raise TypeError( "callback object *MUST* be a callable one." )
        return False

    def resume (self):
        r"""
            resumes animation with current param values;

            returns newly created process id (pid) on success,
            integer zero (0 - no pid) otherwise;
        """
        return self.run_sequencer()

    def run_sequencer (self, animation_kw=None):
        r"""
            runs animation loop itself with some cool features;

            returns newly created process id (pid) on success,
            integer zero (0 - no pid) otherwise;
        """
        # stops previous pending process, if any;
        # resets self.__pid = 0 whatever happens;
        self.stop()

        # first of all
        if callable(self.__callback):
            # param controls
            if isinstance(animation_kw, dict):
                # set new keywords
                self.__animation_kw = _anim_kw = animation_kw
            else:
                # get previously stored keywords
                _anim_kw = self.__animation_kw
            # param inits
            _sequence = _anim_kw.get("sequence")

            # indexed and iterable sequence?
            if isinstance(_sequence, (list, tuple)):
                # get other inits
                _interval = int(_anim_kw.get("interval", 100))
                _step = int(_anim_kw.get("step", 0))

                # should we run a new step?
                if _step < len(_sequence):
                    # update values in callback keywords
                    self.__callback_kw.update( value=_sequence[_step] )

                    # call callback with args and kw
                    self.__callback( *self.__callback_args, **self.__callback_kw )

                    # schedule next step
                    self.__animation_kw["step"] = _step + 1

                    # go further
                    self.__pid = self.after( _interval, self.run_sequencer )

        # current process id (pid) or 0 on failure
        return self.__pid

    def start (self, interval=100, step=0, sequence=None):
        r"""
            starts animation loop along params;

            returns newly created process id (pid) on success,
            integer zero (0 - no pid) otherwise;
        """
        return self.run_sequencer( dict(interval=interval, step=step, sequence=sequence) )

    def start_after (self, delay=500, interval=100, step=0, sequence=None):
        r"""
            runs deferred animation after @delay (in milliseconds);

            returns newly created process id (pid) of deferred call;
        """
        self.__pid = self.after( delay, self.start, interval, step, sequence )
        return self.__pid

    def stop (self, pid=None):
        r"""
            stops a deferred process along @pid or along internal
            pid if omitted;

            no return value (void);
        """
        # specific pid to cancel?
        if pid:
            self.after_cancel(pid)
        # internal pid
        else:
            self.after_cancel(self.__pid)
            self.__pid = 0


class GridCellSize:
    r"""
        GridCellSize - GameGrid subcomponent;
    """
    def __init__ (self, grid_owner):
        self.__tk_owner = grid_owner
        self.__width = None
        self.__height = None

    def _real_size (self, size, count, thickness):
        r"""
            adjusts calculations to meet real GridCellSize size;
        """
        # adjust to correct size
        _size = size - (count + 1) * thickness

        # return real size
        return round(abs(_size // count))

    @property
    def height (self):
        r"""
            gets GridCellSize's real height;
        """
        # missing pre-computed dimension?
        if not self.__height:
            # get cell's real height dimension
            self.__height = self._real_size(
                size=self.owner.grid_height,
                count=self.owner.rows,
                thickness=self.owner.thickness,
            )
        return self.__height

    @property
    def owner (self):
        r"""
            returns ref to private tk_owner;
        """
        return self.__tk_owner

    @property
    def size (self):
        r"""
            returns a (width, height) pair;
        """
        return (self.width, self.height)

    @property
    def size_hxw (self):
        r"""
            returns a (height, width) pair;
        """
        return (self.height, self.width)

    @property
    def size_wxh (self):
        r"""
            returns a (width, height) pair;
        """
        return (self.width, self.height)

    @property
    def width (self):
        r"""
            gets GridCellSize's real width;
        """
        # missing pre-computed dimension?
        if not self.__width:
            # get cell's real width dimension
            self.__width = self._real_size(
                size=self.owner.grid_width,
                count=self.owner.columns,
                thickness=self.owner.thickness,
            )
        return self.__width

    def x_center (self, column):
        r"""
            returns only centered x coordinate;
        """
        return self.x_left(column) + self.width // 2

    def x_left (self, column):
        r"""
            returns only x_left coordinate;
        """
        # rebind location
        _column = min(abs(int(column)), self.owner.columns)
        _thickness = self.owner.thickness

        # make calculations
        _x = _thickness + _column * (self.width + _thickness)

        # new coordinate
        return _x

    def xy_center (self, row, column):
        r"""
            returns (x, y) centered coordinates;
        """
        return (self.x_center(column), self.y_center(row))

    def xy_left_top (self, row, column):
        r"""
            returns (x_left, y_top) coordinates;
        """
        return (self.x_left(column), self.y_top(row))

    def y_center (self, row):
        r"""
            returns only centered y coordinate;
        """
        return self.y_top(row) + self.height // 2

    def y_top (self, row):
        r"""
            returns only y_top coordinate;
        """
        # rebind location
        _row = min(abs(int(row)), self.owner.rows)
        _thickness = self.owner.thickness

        # make calculations
        _y = _thickness + _row * (self.height + _thickness)

        # new coordinate
        return _y


class GridError (Exception):
    r"""
        Exception handler for convenience;
    """
    pass


class GridMatrix:
    r"""
        GridMatrix - GameGrid subcomponent;
    """
    def __init__ (self, rows, columns):
        self.rows = rows
        self.columns = columns

        # first time: reset matrix
        self.reset_matrix()

    def display(self):
        matrix = np.zeros([self.rows, self.columns])

        for i in range(self.rows):
            for j in range(self.columns):
                if self.__matrix[i][j] is None:
                    matrix[i][j] = 0
                else:
                    matrix[i][j] = self.__matrix[i][j].value

    def add(self, object_, row, column, raise_error=False):
        r"""
            adds an object at (row, column) in matrix;

            raises error if @raise_error and busy location;

            returns True on success, False otherwise;
        """
        # all is OK?
        if self.matrix[row][column] is None:
            # add object to matrix
            self.matrix[row][column] = object_

            # succeeded
            return True
        elif raise_error:
            raise GridError(
                "cannot add object at (row, column) = ({row}, {col}): busy location."
                .format(row=row, col=column)
            )
        # failed
        return False

    def duplicate_object(self, from_row_column, to_row_column):
        r"""
            duplicates the object located at @from_row_column into
            @to_row_column if exists;

            raises errors otherwise;
        """
        # get object if exists
        _object = self.get_object_at(*from_row_column, raise_error=True)

        # add copy to new location
        self.add(_object, *to_row_column, raise_error=True)

    def get_object_at(self, row, column, raise_error=False):
        r"""
            returns the object located at (row, column) in the
            matrix or None on failure;

            raises an error if @raise_error and empty location;
        """
        try:
            _object = self.matrix[row][column]
        except:
            _object = None

        # no object found?
        if raise_error and _object is None:
            raise GridError(
                "no object found at (row, column) = ({row}, {col}): empty location."
                .format(row=row, col=column)
            )
        return _object

    def move_object(self, from_row_column, to_row_column):
        r"""
            moves the object located at @from_row_column to
            @to_row_column if exists;

            raises errors otherwise;
        """
        # get object if exists
        _object = self.get_object_at(*from_row_column, raise_error=True)

        # add it to new location
        self.add(_object, *to_row_column, raise_error=True)

        # and then remove it from old location
        self.remove_object_at(*from_row_column)

    def remove_object_at(self, row, column):
        r"""
            removes the object located at (row, column) from the
            matrix, if any;
        """
        # remove object
        self.matrix[row][column] = None

    def reset_matrix(self):
        r"""
            resets matrix to current rows and columns;
        """
        # caution:
        # do *NOT* use [[None]*cols]*rows: *NOT* shallow copies!
        self.__matrix = [
            [None] * self.columns for i in range(self.rows)
        ]

    def swap_objects(self, row_column1, row_column2):
        r"""
            swaps two objects located at @row_column1 and
            @row_column2 if they do exist;

            raises errors otherwise;
        """
        # get objects if exist
        _object1 = self.get_object_at(*row_column1, raise_error=True)
        _object2 = self.get_object_at(*row_column2, raise_error=True)

        # clear locations
        self.remove_object_at(*row_column1)
        self.remove_object_at(*row_column2)

        # swap locations
        self.add(_object1, *row_column2, raise_error=True)
        self.add(_object2, *row_column1, raise_error=True)

    ################
    # Properties
    ################
    @property
    def columns (self):
        r"""
            returns number of columns in matrix;
        """
        return self.__columns

    @columns.setter
    def columns (self, value):
        self.__columns = normalize(value)

    @columns.deleter
    def columns (self):
        del self.__columns

    @property
    def matrix (self):
        r"""
            returns internal matrix object;
        """
        return self.__matrix

    @matrix.setter
    def matrix(self, matrixToSet):
        # Copy content
        for i in range(self.rows):
            for j in range(self.columns):
                if matrixToSet[i][j] is None:
#                    print("{0}, {1} => {2}".format(i, j, 0))
                    self.__matrix[i][j] = None
                else:
#                    print("{0}, {1} => {2}".format(i, j, self.__matrix[i][j].value))
                    self.__matrix[i][j] = GridTile(
                        matrixToSet[i][j].owner,
                        matrixToSet[i][j].value,
                        matrixToSet[i][j].row,
                        matrixToSet[i][j].column
                    )

    @property
    def rows (self):
        r"""
            returns number of rows in matrix;
        """
        return self.__rows

    @rows.setter
    def rows (self, value):
        self.__rows = normalize(value)

    @rows.deleter
    def rows (self):
        del self.__rows


class GridTile:
    r"""
        GridTile - GameGrid subcomponent;
    """
    def __init__ (self, grid_owner, value, row, column):
        # private member inits
        self.__tk_owner = grid_owner
        self.__cell_size = grid_owner.cell_size

        # unique tag id for canvas tags management
        self.tag = "GridTile{}".format(id(self))

        self.id = None
        self.value = value
        self.row = row
        self.column = column

    @property
    def cell_size (self):
        r"""
            returns object's GridCellSize structure;
        """
        return self.__cell_size

    @property
    def column (self):
        r"""
            returns object's normalized column;
        """
        return self.__column

    @column.setter
    def column (self, value):
        self.__column = normalize(value, minimum=0)

    @column.deleter
    def column (self):
        del self.__column

    @property
    def row_column (self):
        r"""
            returns a (row, column) pair;
        """
        return (self.row, self.column)

    @property
    def owner (self):
        r"""
            returns ref to private tk_owner;
        """
        return self.__tk_owner

    @property
    def row (self):
        r"""
            returns object's normalized row;
        """
        return self.__row

    @row.setter
    def row (self, value):
        self.__row = normalize(value, minimum=0)

    @row.deleter
    def row (self):
        del self.__row

    @property
    def size (self):
        r"""
            returns object's (width, height) cell size;
        """
        return self.cell_size.size_wxh

    @property
    def value (self):
        r"""
            returns object's value;
        """
        return self.__value

    @value.setter
    def value (self, new_value):
        self.__value = new_value

    @value.deleter
    def value (self):
        del self.__value

    @property
    def xy_center (self):
        r"""
            returns tile's (x, y) center point on canvas;
        """
        return self.cell_size.xy_center(self.row, self.column)

    @property
    def xy_origin (self):
        r"""
            returns tile's (x_left, y_top) point of origin on canvas;
        """
        return self.cell_size.xy_left_top(self.row, self.column)

