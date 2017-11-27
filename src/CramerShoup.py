#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains the CramerShoup class
"""

from random import randint
from src.functions import random_prime, find_group_generators

class CramerShoup(object):
    """ CramerShoup implementation

        Attributes:
            p -- int -- a prime number
            g1, g2 -- int -- two distinct generators of p
            x1, x2, y1, y2, w -- int -- randomly picked numbers in range [0:p]
            X -- int -- result of g1**x1 + g2**x2
            Y -- int -- result of g1**y1 + g2**y2
            W -- int -- result of g1**w

        public key: (p, g1, g2, X, Y, W)
        private key: (x1, x2, y1, y2, w)
    """
    def __init__(self):
        self.min_prime = 100
        self.max_prime = 500
        self.p, self.g1, self.g2, self.X, self.Y, self.W, self.x1, self.x2, \
            self.y1, self.y2, self.w = self.key_generation()

    def key_generation(self):
        """ Generate the keys
        """
        # start by generate randomly a prime number p
        p = random_prime(self.min_prime, self.max_prime)
        # get the generators of p
        generators = find_group_generators(p)
        # pick 2 distinct generators randomly
        g1 = generators[randint(0, len(generators)-1)]
        g2 = g1
        while g2 == g1:
            g2 = generators[randint(0, len(generators)-1)]
        # pick randomly 5 integers in range [0:P]
        x1 = randint(0, p)
        x2 = randint(0, p)
        y1 = randint(0, p)
        y2 = randint(0, p)
        w = randint(0, p)
        # calculate X, Y and W
        X = g1**x1 + g2**x2
        Y = g1**y1 + g2**y2
        W = g1**w

        return p, g1, g2, X, Y, W, x1, x2, y1, y2, w
