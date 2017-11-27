#!usr/bin/env python3
# -*- coding: utf-8 -*-

from src.CramerShoup import CramerShoup
from src.SHA1 import SHA1

"""
c = CramerShoup()
c.key_generation()
print(c.p)
print(c.g1)
print(c.g2)
print(c.X)
print(c.Y)
print(c.W)
"""

text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
#19afa2a4a37462c7b940a6c4c61363d49c3a35f4

SHA1 = SHA1()
print(SHA1.hash(text))
print(SHA1.final_hash())
