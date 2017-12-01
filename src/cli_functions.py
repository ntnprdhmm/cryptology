#!usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains all function uses in cli.py
"""

import curses

SCREEN = curses.initscr()

MENU_ITEMS = [
    "1. Hash a message with SHA-1",
    "2. Cipher a file with Cramer-Shoup",
    "3. Quit"
]

def wait_to_continu(leave=False):
    """ Print a message and wait for the user to press any key to continu

        Args:
            leave -- boolean -- if True, inform the user that the program will leave
    """
    SCREEN.addstr("\n")
    SCREEN.addstr("Press any key to " + ("leave" if leave else "continu") + ".\n")
    SCREEN.getch()

def handle_user_choice(choice):
    """
    """
    # clear the screen
    SCREEN.clear()
    # print the choice
    SCREEN.addstr(MENU_ITEMS[choice] + "\n")

    wait_to_continu(True)

def show_main_menu():
    """ Display the main function, where the user can choose the function he want
        to use
    """
    key = None
    current_pos = 0

    # loop until the user chooses an option
    while not (key == curses.KEY_ENTER or key == 10 or key == 13):
        # remove the menu of the previous loop to draw a new one
        SCREEN.clear()
        # settings
        curses.noecho()
        curses.curs_set(0)
        SCREEN.keypad(1)
        # Draw the menu heading
        SCREEN.addstr("Hello World !\n")
        SCREEN.addstr("\n")
        SCREEN.addstr("Choose what you want to do:\n")
        SCREEN.addstr("(use your arrow keys, and press 'enter' to select):\n")
        SCREEN.addstr("\n")
        # Draw the menu items
        for i, item in enumerate(MENU_ITEMS):
            if i == current_pos:
                SCREEN.addstr(">> ")
            SCREEN.addstr(item + "\n")

        # listen user's input
        key = SCREEN.getch()
        # handle user's input
        if key == curses.KEY_UP:
            # update pos only if not already at the top of the menu
            if current_pos > 0:
                current_pos -= 1
        elif key == curses.KEY_DOWN:
            # update pos only if not already at the bottom of the menu
            if current_pos < (len(MENU_ITEMS) - 1):
                current_pos += 1

    # handle the user's choice
    handle_user_choice(current_pos)
