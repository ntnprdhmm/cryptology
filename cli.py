#!usr/bin/env python3
# -*- coding: utf-8 -*-

from src.CramerShoup import CramerShoup
from src.SHA1 import SHA1

c = CramerShoup()
c.key_generation()
a, b, c, d = c.cipher(150)
print(a)
print('----')
print(b)
print('----')
print(c)
print('----')
print(d)
