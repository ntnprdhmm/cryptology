#!usr/bin/env python3
# -*- coding: utf-8 -*-

from src.CramerShoup import CramerShoup
from src.functions import find_group_generators

"""
c = CramerShoup()
c.key_generation()
print(c.X)
print(c.Y)
print(c.W)
"""

print(find_group_generators(509))
