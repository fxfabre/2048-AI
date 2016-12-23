#!/usr/bin/python3
# -*- coding: utf-8 -*-


import unittest

import pandas
from AI.ai_q_learning import Qlearning

MOVE_LEFT = 0
MOVE_RIGHT = 1
MOVE_UP = 2
MOVE_DOWN = 3


class testQLearning(unittest.TestCase):

    def test_record_state(self):
        ai = Qlearning_wrapper()

        ai.RecordState(0, 1, 'right', 0, True)
        self.assertEqual(-0.02, ai.q_values.iloc[0, MOVE_RIGHT])
        print(ai.q_values)

        ai.RecordState(1, 2, 'right', 0, True)
        self.assertEqual(-0.02, ai.q_values.iloc[1, MOVE_RIGHT])
        print(ai.q_values)

        ai.RecordState(2, 2, 'right', 0, False)
        self.assertEqual(0.5, ai.q_values.iloc[2, MOVE_RIGHT])
        print(ai.q_values)

        ai.RecordState(0, 1, 'right', 0, True)
        self.assertEqual(-0.03, ai.q_values.iloc[0, MOVE_RIGHT])
        print(ai.q_values)

        ai.RecordState(1, 2, 'right', 0, True)
        # self.assertEqual(0.22, ai.q_values.iloc[1, MOVE_RIGHT])
        self.assertAlmostEqual(0.22, ai.q_values.iloc[1, MOVE_RIGHT])
        print(ai.q_values)

        ai.RecordState(2, 2, 'right', 0, False)
        self.assertEqual(0.75, ai.q_values.iloc[2, MOVE_RIGHT])
        print(ai.q_values)


class Qlearning_wrapper(Qlearning):

    def __init__(self):
        super(Qlearning_wrapper, self).__init__()

        self.q_values = pandas.DataFrame(index=range(3), columns=self._moves_list)
        self.q_values.fillna(0, inplace=True)
        print('Init Q learning success :', self.q_values.shape)

        self.alpha = 0.5
        self.gamma = 1
        self.reward_move = -0.04
        self.reward_end_game = 1

    def GetState(self, state):
        return state


