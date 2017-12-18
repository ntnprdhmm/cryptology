#!usr/bin/env python3

""" Display an interactive menu in the console (ncurses)
    with many options: cipher / decipher / hash / check hash / ...
"""

import curses
from src._cli_functions import show_main_menu

if __name__ == '__main__':
    try:
        show_main_menu()
    finally:
        # Todo if an error happened or end correctly
        # else, the terminal is broken
        curses.endwin()
