#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np


def perp_vector(ref, u):
    if not isinstance(ref, np.ndarray):
        ref = np.array(ref)
    if not isinstance(u, np.ndarray):
        u = np.array(u)
    return u - (ref.dot(u) / ref.dot(ref)) * ref


def reduce_space_to_base(list_vectors):
    vectors_to_keep = []
    for vector in list_vectors:
        # print("Processing", vector)
        vector = np.array(vector)

        for base in vectors_to_keep:
            vector = perp_vector(base, vector)
            # print("Base reduce to", vector)

        if vector.dot(vector) > 1e-6:
            # print("Keep vector")
            vectors_to_keep.append(vector)

    return vectors_to_keep


if __name__ == '__main__':
    l_vect = ([1, 0, 0], [0, 1, 0], [0, 0, 1], [2, 1, 4])
    print(reduce_space_to_base(l_vect))
