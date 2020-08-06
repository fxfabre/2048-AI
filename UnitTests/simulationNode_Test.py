#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
import numpy as np
import AI.Models.simulationNode as sn

class testConstructor(unittest.TestCase):

    def test_Initialisation(self):

        rootNode = sn.SimulationNode()
        rootNode.addScore('left' , 12)
        rootNode.addScore('right', 5)
        rootNode.addScore('up'   , 21)
        rootNode.addScore('up'   , 14)

        self.assertEqual(12, sum(rootNode.scoreLeft))
        self.assertEqual(5 , sum(rootNode.scoreRight))
        self.assertEqual(35, sum(rootNode.scoreUp))
        self.assertEqual(0 , sum(rootNode.scoreDown))

        self.assertRaises(Exception, lambda : rootNode.addScore('somewhere', 42))

