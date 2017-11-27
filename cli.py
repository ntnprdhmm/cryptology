#!usr/bin/env python3
# -*- coding: utf-8 -*-

from src.CramerShoup import CramerShoup

c = CramerShoup()
c.key_generation()
print(c.p)
print(c.g1)
print(c.g2)
print(c.X)
print(c.Y)
print(c.W)
