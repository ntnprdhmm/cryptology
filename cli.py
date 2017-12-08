#!usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
from src.cli_functions import show_main_menu
from src.CramerShoup import CramerShoup

if __name__ == '__main__':
    try:
        #show_main_menu()
        c = CramerShoup()
        c.cipher()
        c.decipher()
    finally:
        # Todo if an error happened or end correctly
        # else, the terminal is broken
        curses.endwin()
