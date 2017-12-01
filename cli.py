#!usr/bin/env python3
# -*- coding: utf-8 -*-

from src.cli_functions import (curses, show_main_menu)

if __name__ == '__main__':
    try:
        show_main_menu()
    finally:
        # Todo if an error happened or end correctly
        # else, the terminal is broken
        curses.endwin()
