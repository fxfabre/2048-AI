#!/usr/bin/python3
# -*- coding: utf-8 -*-

from math import sqrt
import pandas
import numpy as np
from sklearn.decomposition.pca import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold

from constants import FILE_RECORD_MOVES


def add_features(df):
    nb_tiles = int(sqrt(len(df.columns)))
    df.columns = range(nb_tiles)


def dim_redux():
    df = pandas.read_csv(FILE_RECORD_MOVES, sep='|', header=None)
    # df = df.iloc[:10, :]
    columns = df.columns.tolist()
    index_direction = columns[-1]
    x = df[columns[:len(columns) // 2]]

    for direction in ['left', 'right', 'up', 'down']:
        print('\n' + direction)
        x_dir = x[df[index_direction] == direction]
        # y = df[df[index_direction] == direction][index_direction]
        # y = y.map(lambda s: s and 1 or 0)
        pca = PCA()
        pca.fit(x_dir)
        eigenval = pca.explained_variance_ratio_
        for i in range(len(eigenval)):
            val = eigenval[i]
            vect = pca.components_[i]
            print(val, vect)
        yield direction, pca


def classification():
    directions = ['left', 'right', 'up', 'down']

    df = pandas.read_csv(FILE_RECORD_MOVES, sep='|', header=None)
    df = df.iloc[:20, :]
    columns = df.columns.tolist()

    col_train = columns[:len(columns) // 2]
    index_direction = columns[-1]
    x = df[col_train]

    # Set 1 column for each direction {0, 1}
    for direction in directions:
        df[direction] = df[index_direction].map(lambda s: s == direction and 1 or 0)

    for direction in ['left', 'right', 'up', 'down']:
        kf = KFold(n_splits=4)
        x['target'] = df[direction]
        for train, test in kf.split(x):
            x_train = train[col_train]
            y_train = train['target']
            x_test = test[col_train]
            y_test = test['target']

            reglog = LogisticRegression()
            reglog.fit(x_train, y_train)
            score = reglog.score(x_test, y_test)
            print(direction, score)


def get_features(row, nb_tile):
    """ Features to add
    - position of the highest value (x, y)
    - entropy
    - barycentre (x, y)
    """
    matrix = np.array(row[1])

    # position of the highest value (x, y)
    idx_max_val = matrix.argmax()

    # reshape array to matrix
    matrix = matrix.reshape([nb_tile, nb_tile])

    # Entropy
    entropy = 0
    for x in range(nb_tile - 1):
        for y in range(nb_tile):
            entropy += abs(matrix[x, y] - matrix[x + 1, y])
            entropy += abs(matrix[y, x] - matrix[y, x + 1])

    # Barycentre
    sum_val_x = 0
    sum_val_y = 0
    total_coeff = 0
    for x in range(nb_tile):
        for y in range(nb_tile):
            sum_val_x += x * matrix[x, y]
            sum_val_y += y * matrix[x, y]
            total_coeff += matrix[x, y]

    return {
        'idx_max_val_x' : idx_max_val // nb_tile,
        'idx_max_val_y' : idx_max_val % nb_tile,
        'entropy'       : entropy,
        'barycentre_x'  : sum_val_x / total_coeff,
        'barycentre_Y'  : sum_val_y / total_coeff
    }





def main():
    df = pandas.read_csv(FILE_RECORD_MOVES, sep='|', header=None)
    nb_tile = df.shape[1] / 2
    columns = df.columns.tolist()
    col_x = columns[:nb_tile]
    col_y = columns[nb_tile:]

    df_matrix_x = df[col_x]
    add_features(df_matrix_x)

    df_matrix_y = df[col_y]
    add_features(df_matrix_y)


if __name__ == '__main__':
    main()

