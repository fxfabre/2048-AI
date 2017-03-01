#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import sklearn
import pandas


FILE_NAME = 'moves_history.csv'


def main():
    df = pandas.read_csv(FILE_NAME, sep='|')
    nb_tile = df.shape[1] / 2
    for row in df.iterrows():
        print(row[0])
        print()
        print(row[1])
        return


# def process_line():


if __name__ == '__main__':
    main()

