#!/usr/bin/env python3

""" This module contains functions to simplify the cli building
"""

import curses

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

def ask_question(question, to_string=False):
    """ Ask a question to a user, and return his response

        Args:
            question -- string -- the question to ask
            to_string -- boolean -- if True, format the bytes input to string
                before returning it

        return the user's response (in bytes)
    """
    SCREEN.addstr(question + "\n")
    response = SCREEN.getstr()

    SCREEN.addstr(str(response)[2:-1] + "\n\n")

    return str(response)[2:-1] if to_string else response

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
