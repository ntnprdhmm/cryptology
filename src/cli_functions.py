#!usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains all function uses in cli.py
"""

import curses
from src.SHA1 import SHA1
from src.CramerShoup import CramerShoup
from src.utils import read_file

SCREEN = curses.initscr()

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

    if main_menu:
        show_main_menu()

def sha1_hash_text():
    """ Ask the user to enter the text he wants to hash,
        hash it, and print the result
    """
    # clear the main menu
    SCREEN.clear()

    # header
    SCREEN.addstr("HASH A TEXT WITH SHA-1\n")
    SCREEN.addstr("\n")

    SCREEN.addstr("Please enter the text you want to hash:\n")
    # read the text to hash
    text = SCREEN.getstr()
    # print the text to hash
    SCREEN.addstr("text: " + str(text)[2:-1] + "\n")
    SCREEN.addstr("\n")
    # hash the text
    SCREEN.addstr("Hashing your text...\n")
    text_hash = SHA1().hash(text)
    # print the hash
    SCREEN.addstr("\n")
    SCREEN.addstr("Here's your hash: \n")
    SCREEN.addstr(text_hash)
    # wait before redirect to main menu
    wait_to_continu(main_menu=True)

def check_sha1_hash_text():
    """ Ask the user to enter a hash and the hashed text.
        Check if it's the right text by hashing the text and comparing the 2 hashs.
    """
    # clear the main menu
    SCREEN.clear()

    # header
    SCREEN.addstr("CHECK A TEXT'S SHA-1 HASH\n")
    SCREEN.addstr("\n")

    SCREEN.addstr("Please enter the true hash of the text:\n")
    # read the true hash of the text
    true_hash = str(SCREEN.getstr())[2:-1]
    # print the true hash
    SCREEN.addstr("true hash: " + str(true_hash)[2:-1] + "\n")
    SCREEN.addstr("\n")

    SCREEN.addstr("Please enter the text you want to verify:\n")
    # read the text to verify
    text = SCREEN.getstr()
    # print the text to verify
    SCREEN.addstr("text: " + str(text)[2:-1] + "\n")
    SCREEN.addstr("\n")

    # hash the text
    SCREEN.addstr("Hashing your text...\n")
    text_hash = SHA1().hash(text)
    # print the hash
    SCREEN.addstr("\n")
    SCREEN.addstr("Here's the text's hash: \n")
    SCREEN.addstr(text_hash)
    SCREEN.addstr("\n\n")

    # print the result
    if text_hash == true_hash:
        SCREEN.addstr("SUCCESS: The text hasn't been modified.\n")
    else:
        SCREEN.addstr("WARNING: The text has been modified.\n")

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
    file_hash = SHA1().hash(content)
    # print the hash
    SCREEN.addstr("\n")
    SCREEN.addstr("Here's your hash: \n")
    SCREEN.addstr(file_hash)
    # wait before redirect to main menu
    wait_to_continu(main_menu=True)

def check_sha1_hash_file():
    """ Ask the user to enter the name of a file and the hashed file.
        Check if it's the right file by hashing the file and comparing the 2 hashs.
    """
    # clear the main menu
    SCREEN.clear()

    # header
    SCREEN.addstr("CHECK A FILE'S SHA-1 HASH\n")
    SCREEN.addstr("\n")

    SCREEN.addstr("Please enter the true hash of the file:\n")
    # read the true hash of the file
    true_hash = str(SCREEN.getstr())[2:-1]
    # print the true hash
    SCREEN.addstr("true hash: " + str(true_hash)[2:-1] + "\n")
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
    file_hash = SHA1().hash(content)
    # print the hash
    SCREEN.addstr("\n")
    SCREEN.addstr("Here's your hash: \n")
    SCREEN.addstr(file_hash)

    SCREEN.addstr("\n\n")

    # print the result
    if file_hash == true_hash:
        SCREEN.addstr("SUCCESS: The file hasn't been modified.\n")
    else:
        SCREEN.addstr("WARNING: The file has been modified.\n")

    # wait before redirect to main menu
    wait_to_continu(main_menu=True)

def cramer_shoup_generate_keys():
    """ Generate new public and private keys for Cramer Shoup
    """
    # clear the main menu
    SCREEN.clear()

    # header
    SCREEN.addstr("GENERATE KEYS FOR CRAMER-SHOUP\n")
    SCREEN.addstr("\n")

    SCREEN.addstr("generating keys...\n")
    SCREEN.addstr("\n")

    wait_to_continu()

    CramerShoup.key_generation()

    SCREEN.addstr("keys have been generated !\n")
    SCREEN.addstr("\n")

    # wait before redirect to main menu
    wait_to_continu(main_menu=True)

def cramer_shoup_cipher_file():
    """ Ask the user to put the text he want to cipher in a specific file,
        read the content of the file, cipher it, and put the content in a file
    """
    # clear the main menu
    SCREEN.clear()
    # header
    SCREEN.addstr("CIPHER A FILE WITH CRAMER-SHOUP\n")
    SCREEN.addstr("\n")
    SCREEN.addstr("Please put your text in 'assets/cramer_shoup.txt' \n")
    # wait
    wait_to_continu()
    # cipher
    SCREEN.addstr("Ciphering your text...\n")
    CramerShoup.cipher()
    # done !
    SCREEN.addstr("\n")
    SCREEN.addstr("DONE ! \n")
    SCREEN.addstr("you can find the result in 'outputs/cramer_shoup.cipher'\n")
    # wait before redirect to main menu
    wait_to_continu(main_menu=True)

def cramer_shoup_decipher_file():
    """ Ask the user to put the text he want to decipher in a specific file,
        read the content of the file, decipher it, and put the content in a file
    """
    # clear the main menu
    SCREEN.clear()
    # header
    SCREEN.addstr("DECIPHER A FILE WITH CRAMER-SHOUP\n")
    SCREEN.addstr("\n")
    SCREEN.addstr("Please put your ciphertext in 'outputs/cramer_shoup.cipher' \n")
    # wait
    wait_to_continu()
    # cipher
    SCREEN.addstr("Deciphering your text...\n")
    CramerShoup.decipher()
    # done !
    SCREEN.addstr("\n")
    SCREEN.addstr("DONE ! \n")
    SCREEN.addstr("you can find the result in 'outputs/cramer_shoup.decipher'\n")
    # wait before redirect to main menu
    wait_to_continu(main_menu=True)

MENU_ITEMS = [
    ("Hash a text with SHA-1", sha1_hash_text),
    ("Check a text's SHA-1 hash", check_sha1_hash_text),
    ("Hash a file with SHA-1", sha1_hash_file),
    ("Check a file's SHA-1 hash", check_sha1_hash_file),
    ("Generate keys for Cramer-Shoup", cramer_shoup_generate_keys),
    ("Cipher a file with Cramer-Shoup", cramer_shoup_cipher_file),
    ("Decipher a file with Cramer-Shoup", cramer_shoup_decipher_file),
    ("Quit", lambda: None)
]

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
