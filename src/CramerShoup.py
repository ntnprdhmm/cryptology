#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains the CramerShoup class
"""

from random import randint
from src.functions import random_prime, find_group_generators

class CramerShoup(object):
    """ CramerShoup implementation
    """
    def __init__(self):
        self.min_prime = 100
        self.max_prime = 500
        self.p, self.a1, self.a2, self.X, self.Y, self.W = self.key_generation()

    def key_generation(self):
        """ Generate the public key (p, a1, a2, X, Y, W)
        """
        # start by generate randomly a prime number p
        p = random_prime(self.min_prime, self.max_prime)
        # get the generators of p
        generators = find_group_generators(p)
        # pick 2 distinct generators randomly
        a1 = generators[randint(0, len(generators)-1)]
        a2 = a1
        while a2 == a1:
            a2 = generators[randint(0, len(generators)-1)]
        # pick randomly 5 integers in range [0:P]
        x1 = randint(0, p)
        x2 = randint(0, p)
        y1 = randint(0, p)
        y2 = randint(0, p)
        w = randint(0, p)
        # calculate X, Y and W
        X = a1**x1 + a2**x2
        Y = a1**y1 + a2**y2
        W = a1**w

        return p, a1, a2, X, Y, W
