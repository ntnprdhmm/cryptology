#!/usr/bin/env python3

""" This module contains functions to simplify the cli building
"""

import curses
from src.utils import (read_file)

SCREEN = curses.initscr()

def wait_to_continu(leave=False, next_step=None):
    """ Print a message and wait for the user to press any key to continu

        Args:
            leave -- boolean -- if True, inform the user that the program will leave
            next_step -- function -- if not None, call this function after
    """
    destination = "leave" if leave else "continu"

    SCREEN.addstr("\n\n")
    SCREEN.addstr("Press any key to " + destination + ".\n")
    SCREEN.getch()

    if next_step:
        next_step()

def print_option_header(title):
    """ Clear the console and print the option's title

        Args:
            title -- string -- the choosen option's title
    """
    SCREEN.clear()
    SCREEN.addstr(title.upper())
    SCREEN.addstr("\n\n")

def load_data(data_name=None, to_string=False):
    """ Ask the data to the user. He has to choose between:
            - paste his text in the console
            - paste the name of his file in the console

        Args:
            to_string -- boolean -- if True, the data as string, else bytes

        return the data
    """
    if data_name:
        SCREEN.addstr("TO LOAD: " + data_name + "\n")

    SCREEN.addstr("How do you want to load it ?\n")
    SCREEN.addstr("- press 't' to type (or paste) your it directly in the console\n")
    SCREEN.addstr("- press 'f' if you want to choose a file\n")
    choice = -1
    while choice != 102 and choice != 116:
        choice = SCREEN.getch()
    if choice == 116:
        SCREEN.addstr("You choose to type directly in the console.\n")
        SCREEN.addstr("Enter your data now:\n")
        data = SCREEN.getstr()
        SCREEN.addstr(str(data)[2:-1] + "\n\n")
    else:
        SCREEN.addstr("You choose to load it by file.\n")
        SCREEN.addstr("Your file must be in the '/assets' directory.\n")
        SCREEN.addstr("Enter the name of your file:\n")
        filename = str(SCREEN.getstr())[2:-1]
        data = read_file(filename, read_bytes=True)

    return str(data)[2:-1] if to_string else data

def print_data(data, message=None, done=False):
    """ Print some data at the screen

        Args:
            data -- string -- the data to display
            message -- string -- if not None, add the message before the data
            done -- boolean -- if set to True, show diplay "done" to inform that
                the user that this is the final output
    """
    if done:
        SCREEN.addstr("DONE !!!\n")
    if message:
        SCREEN.addstr(message + "\n")
    SCREEN.addstr(data + "\n\n")
