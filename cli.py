#!usr/bin/env python3
# -*- coding: utf-8 -*-

from src.CramerShoup import CramerShoup
from src.SHA1 import SHA1

m = 33

cs = CramerShoup()
cs.key_generation()
print("m  -- %d" % m)
b1, b2, c, v = cs.cipher(m)
print("b1 -- %d" % b1)
print("b2 -- %d" % b2)
print("c  -- %d" % c)
print("v  -- %d" % v)
m_rec = cs.decipher(b1, b2, c, v)
print("m_rec -- %d" % m_rec)
