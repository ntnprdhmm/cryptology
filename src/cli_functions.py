#!usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains all function uses in cli.py
"""

import curses
from src.SHA1 import SHA1
from src.utils import read_file

SCREEN = curses.initscr()

def sha1_hash_message():
    """ Ask the user to enter the text he wants to hash,
        hash it, and print the result
    """
    # clear the main menu
    SCREEN.clear()

    # header
    SCREEN.addstr("HASH A MESSAGE WITH SHA-1\n")
    SCREEN.addstr("\n")

    SCREEN.addstr("Please enter the message you want to hash:\n")
    # read the text to hash
    s = SCREEN.getstr()
    # print the text to hash
    SCREEN.addstr("text: " + str(s)[2:-1] + "\n")
    SCREEN.addstr("\n")
    # hash the text
    SCREEN.addstr("Hashing your text...\n")
    h = SHA1().hash(s)
    # print the hash
    SCREEN.addstr("\n")
    SCREEN.addstr("Here's your hash: \n")
    SCREEN.addstr(h)
    # wait before redirect to main menu
    wait_to_continu(main_menu=True)

def sha1_hash_file():
    """ Ask the user to enter the name of the file he wants to hash,
        read the content of the file, hash it, and print the result
    """
    # clear the main menu
    SCREEN.clear()

    # header
    SCREEN.addstr("HASH A FILE WITH SHA-1\n")
    SCREEN.addstr("\n")

    SCREEN.addstr("Please put your file in the 'assets' directory\n")
    SCREEN.addstr("and enter the complete file name (with the extension):\n")
    # read the file name
    filename = str(SCREEN.getstr())[2:-1]
    # print the filename
    SCREEN.addstr("filename: " + filename + "\n")
    SCREEN.addstr("\n")
    # read the content of the file to hash
    content = read_file(filename, read_bytes=True)
    # hash the file
    SCREEN.addstr("Hashing your file...\n")
    h = SHA1().hash(content)
    # print the hash
    SCREEN.addstr("\n")
    SCREEN.addstr("Here's your hash: \n")
    SCREEN.addstr(h)
    # wait before redirect to main menu
    wait_to_continu(main_menu=True)

def cramer_shoup_cipher():
    pass

MENU_ITEMS = [
    ("Hash a message with SHA-1", sha1_hash_message),
    ("Hash a file with SHA-1", sha1_hash_file),
    ("Cipher a file with Cramer-Shoup", cramer_shoup_cipher),
    ("Quit", lambda: None)
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
            SCREEN.addstr(str(i+1) + ". " + item[0] + "\n")

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
