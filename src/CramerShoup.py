#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains the CramerShoup class
"""

from random import randint

class CramerShoup(object):
    """ CramerShoup implementation
    """
    def __init__(self):
        self.p = 67
        self.a1 = 34
        self.a2 = 41
        self.X = 0
        self.Y = 0
        self.W = 0

    def key_generation(self):
        """ Generate the public key (p, a1, a2, X, Y, W)
        """
        # pick randomly 5 integers in range [0:P]
        x1 = randint(0, self.p)
        x2 = randint(0, self.p)
        y1 = randint(0, self.p)
        y2 = randint(0, self.p)
        w = randint(0, self.p)
        # calculate X, Y and W
        self.X = self.a1**x1 + self.a2**x2
        self.Y = self.a1**y1 + self.a2**y2
        self.W = self.a1**w
