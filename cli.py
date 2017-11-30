#!usr/bin/env python3
# -*- coding: utf-8 -*-

from src.CramerShoup import CramerShoup

m = 33

cs = CramerShoup()
cs.key_generation()
cs.cipher()
cs.decipher()
