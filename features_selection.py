#!/usr/bin/python3
# -*- coding: utf-8 -*-

from math import sqrt
import pandas
import numpy as np
from Tools.geometry import reduce_space_to_base

from sklearn.decomposition.pca import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import KFold

from constants import FILE_RECORD_MOVES


def add_features(df):
    nb_tiles = int(sqrt(len(df.columns)))
    df.columns = range(nb_tiles)


def dim_redux():
    directions = ['left', 'right', 'up', 'down']

    df = pandas.read_csv(FILE_RECORD_MOVES, sep='|', header=None)
    df = df.iloc[:20, :]
    columns = df.columns.tolist()
    index_direction = columns[-1]
    # df = df[columns[:len(columns) // 2] + [index_direction]]

    x = df[columns[:len(columns) // 2]]
    y = df[index_direction]

    # Set 1 column for each direction {0, 1}
    for direction in directions:
        df[direction] = df[index_direction].map(lambda s: s == direction and 1 or 0)

    vectors_to_keep = []
    for direction in directions:
        x_train = x[y == direction]

        pca = PCA(n_components=2)
        pca.fit(x_train)

        eigenval = pca.explained_variance_ratio_
        eigenvect = pca.components_

        vectors_to_keep.append(eigenvect[0])
        if eigenval[1] > 0.1:
            vectors_to_keep.append(eigenvect[1])

    vectors_to_keep = reduce_space_to_base(vectors_to_keep)
    print("Base :")
    print(vectors_to_keep)


def dim_redux_tst():
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
    # df = df.iloc[:10, :]
    columns = df.columns.tolist()

    col_train = columns[:len(columns) // 2]
    index_direction = columns[-1]
    x = df[col_train]

    # Set 1 column for each direction {0, 1}
    for direction in directions:
        df[direction] = df[index_direction].map(lambda s: s == direction and 1 or 0)

    for direction in ['left', 'right', 'up', 'down']:
        kf = KFold(n_splits=4)
        # x['target'] = df[direction]
        min_score_reglog = 1
        min_score_svm = 1
        for train_idx, test_idx in kf.split(x):
            x_train = x.iloc[train_idx, :]
            y_train = df[direction].iloc[train_idx]
            x_test = x.iloc[test_idx, :]
            y_test = df[direction].iloc[test_idx]

            reglog = LogisticRegression()
            reglog.fit(x_train, y_train)
            score = reglog.score(x_test, y_test)
            min_score_reglog = min(min_score_reglog, score)

            svm = SVC()
            svm.fit(x_train, y_train)
            score = svm.score(x_test, y_test)
            min_score_svm = min(min_score_svm, score)
        print(direction, min_score_reglog, min_score_svm)


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
    dim_redux()


# array([0.17081063, 0.07524625, 0.22627677, 0.34229269, 0.68748373, 0.44461819, -0.09536208, 0.32199503, -0.11705696]),
# array([-0.07982328, -0.14470174, -0.58007032, -0.49880449, 0.11374474, 0.5977328, -0.0412646, -0.09541662, -0.07982915]),
# array([-0.03289516, -0.06995701, -0.04845927, 0.11186598, -0.15322015, 0.01787916, -0.25065351, 0.08749537, -0.24661663]),
# array([-0.01125051, -0.21717013, 0.0026973, 0.05762126, -0.08556218, 0.06317986, 0.03679571, 0.16021699, 0.16589527]),
# array([-0.18498545, -0.18966956, -0.34019131, -0.03696523, 0.35744632, -0.4686111, 0.15881556, 0.28324479, -0.18841921]),
# array([-0.16202948, 0.05651554, 0.0337192, 0.01448132, -0.02900932, 0.04929434, 0.06637607, 0.0373337, -0.02709643]),
# array([0.14822672, 0.13642155, 0.18322909, -0.3932491, -0.08669006,-0.0314816, -0.01679652, 0.37670263, -0.07055603])

