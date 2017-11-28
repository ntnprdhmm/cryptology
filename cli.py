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

# a3da7877f94ad4cf58636a395fff77537cb8b919
#text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

# 7c0a529d2e9e40f54944674b0de7e806fba33262
text = "Hello world !"

SHA1 = SHA1()
print(SHA1.hash(text))


#b'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xe0'
