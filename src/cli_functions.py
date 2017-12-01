#!usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains all function uses in cli.py
"""

import curses
from src.SHA1 import SHA1

SCREEN = curses.initscr()

def sha1_hash_message():
    # clear the main menu
    SCREEN.clear()

    SCREEN.addstr("Pleaser enter the message you want to hash:\n")
    # read the text to hash
    s = SCREEN.getstr()
    # hash the text
    SCREEN.addstr("Hashing your text...\n")
    h = SHA1().hash(s)
    # print the hash
    SCREEN.addstr("\n")
    SCREEN.addstr("Here's your hash: \n")
    SCREEN.addstr(h)
    # wait before redirect to main menu
    wait_to_continu(main_menu=True)

def cramer_shoup_cipher():
    pass

MENU_ITEMS = [
    ("1. Hash a message with SHA-1", sha1_hash_message),
    ("2. Cipher a file with Cramer-Shoup", cramer_shoup_cipher),
    ("3. Quit", lambda: None)
]

def wait_to_continu(leave=False, main_menu=False):
    """ Print a message and wait for the user to press any key to continu

        Args:
            leave -- boolean -- if True, inform the user that the program will leave
    """
    destination = "continu"

    if leave:
        destination = "leave"
    elif main_menu:
        destination = "go to the main menu"

    SCREEN.addstr("\n\n")
    SCREEN.addstr("Press any key to " + destination + ".\n")
    SCREEN.getch()

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
            SCREEN.addstr(item[0] + "\n")

        # listen user's input
        key = SCREEN.getch()
        SCREEN.addstr(str(key))
        # handle user's input
        if key == curses.KEY_UP:
            # update pos only if not already at the top of the menu
            if current_pos > 0:
                current_pos -= 1
        elif key == curses.KEY_DOWN:
            # update pos only if not already at the bottom of the menu
            if current_pos < (len(MENU_ITEMS) - 1):
                current_pos += 1
        elif key >= 49 and key <= 57:
            # go directly to the choosen position
            menu_index = key % 49
            if len(MENU_ITEMS) > menu_index:
                current_pos = menu_index

    # handle the user's choice
    MENU_ITEMS[current_pos][1]()
