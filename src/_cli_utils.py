#!/usr/bin/env python3

""" This module contains functions to simplify the cli building
"""

import curses
from src._utils import (read_file, write_file)

SCREEN = curses.initscr()

def wait_to_continu(leave=False, next_step=None):
    """ Print a message and wait for the user to press any key to continu

        Args:
            leave -- boolean -- if True, inform the user that the program will leave
            next_step -- function -- if not None, call this function after
    """
    destination = "leave" if leave else "continu"

    SCREEN.addstr("\n\n")
    print_instruction("Press any key to " + destination + ".\n")
    SCREEN.getch()

    if next_step:
        next_step()

def print_option_header(title):
    """ Clear the console and print the option's title

        Args:
            title -- string -- the choosen option's title
    """
    SCREEN.clear()
    SCREEN.addstr(title.upper(), curses.A_BOLD | curses.A_STANDOUT)
    SCREEN.addstr("\n\n")

def ask_question(question, answers, default_answer):
    """ Ask a question to the user and return his response

        Args:
            question -- string -- the question to display
            answers -- array of strings -- the authorized answers
            default_answer -- string -- if the user answer nothing, this answer
                is selected

        return his answer
    """
    print_help("The default value is in yellow\n")
    print_help("- press 'enter' to accept the default value\n")
    print_help("- or write another possible answer\n")
    user_answer = None
    while not user_answer in answers:
        print_instruction(question)
        SCREEN.addstr(" (")
        for i in range(len(answers)-1):
            SCREEN.addstr(answers[i],
                          curses.color_pair(3 if answers[i] == default_answer else 0))
            SCREEN.addstr(", ")
        SCREEN.addstr(answers[len(answers)-1],
                      curses.color_pair(3 if answers[len(answers)-1] == default_answer else 0))
        SCREEN.addstr(")\n")
        curses.echo()
        user_answer = str(SCREEN.getstr())[2:-1]
        if not user_answer:
            user_answer = default_answer
    return user_answer

def load_data(data_name=None, to_string=False):
    """ Ask the data to the user. He has to choose between:
            - paste his text in the console
            - paste the name of his file in the console

        Args:
            to_string -- boolean -- if True, the data as string, else bytes

        return the data
    """
    if data_name:
        SCREEN.addstr("TO LOAD: " + data_name + "\n", curses.color_pair(1))

    print_instruction("How do you want to load it ?\n")
    print_help("- press 't' to type (or paste) your it directly in the console\n")
    print_help("- press 'f' if you want to choose a file\n\n")
    choice = -1
    while choice != 102 and choice != 116:
        curses.noecho()
        choice = SCREEN.getch()
    if choice == 116:
        SCREEN.addstr("You choose to type directly in the console.\n\n")
        print_instruction("Enter your data:\n")
        curses.echo()
        data = SCREEN.getstr()
    else:
        SCREEN.addstr("You choose to load it by file.\n\n")
        print_help("Your file must be in the '/assets' directory.\n")
        print_instruction("Enter the name of your file:\n")
        curses.echo()
        filename = str(SCREEN.getstr())[2:-1]
        data = read_file(filename, read_bytes=True)

    return str(data)[2:-1] if to_string else data

def output_result(data, default_filename="None"):
    """ Ask the user where he wants the result to be output
            - print it in the console
            - save it in a file

        Args:
            data -- string -- the data to save
            default_filename -- string -- if not None, suggest this filename
    """
    print_instruction("How do you want the result to be output ?\n")
    print_help("- press 'c' if you  want it directly in the console\n")
    print_help("- press 'f' if you want it to be store in a file\n\n")

    choice = -1
    while choice != 99 and choice != 102:
        curses.noecho()
        choice = SCREEN.getch()
    if choice == 99:
        SCREEN.addstr("You choose 'in the console'.\n\n")
        print_result("Here is the ouput\n")
        SCREEN.addstr(data + "\n")
    else:
        SCREEN.addstr("You choose 'in a file'.\n\n")
        print_help("The file will be created in the 'outputs' directory.\n")
        print_instruction("Please enter a name for the file ")
        if default_filename:
            print_info("(" + default_filename + ")")
        SCREEN.addstr(": \n")
        # read the filename
        curses.echo()
        filename = str(SCREEN.getstr())[2:-1]
        if len(filename) == 0:
            filename = default_filename
        # write in the file
        write_file(filename, data)
        print_result("The output has been wrote in '/outputs/" + filename + "' \n")

def print_data(data, message=None, done=False):
    """ Print some data at the screen

        Args:
            data -- string -- the data to display
            message -- string -- if not None, add the message before the data
            done -- boolean -- if set to True, show diplay "done" to inform that
                the user that this is the final output
    """
    if done:
        print_result("DONE !!!\n")
    if message:
        print_info(message + "\n")
    SCREEN.addstr(str(data) + "\n\n")


def print_instruction(m):
    SCREEN.addstr(m, curses.A_BOLD | curses.color_pair(2))

def print_help(m):
    SCREEN.addstr(m, curses.color_pair(4))

def print_info(m):
    SCREEN.addstr(m, curses.A_BOLD | curses.color_pair(3))

def print_result(m):
    SCREEN.addstr(m, curses.A_BOLD | curses.color_pair(5))
