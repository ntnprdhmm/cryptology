#!usr/bin/env python3

""" This module contains all the functions to build the menu and the menu's
    options handlers (ciphering functions, ..)
"""

import curses
from src.SHA1 import SHA1
from src.CramerShoup import CramerShoup
from src._utils import (read_file)
from src._functions import (generate_random_unicode_string)
from src._cli_utils import (SCREEN, wait_to_continu, print_option_header,
                           print_data, load_data, output_result, ask_question)

def sha1_hash():
    """ 1 - Ask the user to enter the data he wants to hash and hash it.
        2 - Ask the user if he want the result in the console or in a file.
    """
    print_option_header("hash with sha-1")
    data = load_data()
    text_hash = SHA1().hash(data)
    output_result(text_hash, "sha1.hash")
    # wait before redirect to main menu
    wait_to_continu(next_step=show_main_menu)

def sha1_check():
    """ Ask the user to enter a hash and the hashed text.
        Check if it's the right text by hashing the text and comparing the 2 hashs.
    """
    print_option_header("check a text's sha-1 hash")

    text = load_data(data_name="your data")
    true_hash = load_data(data_name="the real hash", to_string=True)

    # hash the text
    SCREEN.addstr("Hashing your text...\n")
    text_hash = SHA1().hash(text)
    # print the hash
    print_data(text_hash, "Here's the text's hash:")

    # print the result
    if text_hash == true_hash:
        SCREEN.addstr("SUCCESS: The text hasn't been modified.\n")
    else:
        SCREEN.addstr("WARNING: The text has been modified.\n")

    # wait before redirect to main menu
    wait_to_continu(next_step=show_main_menu)

def cramer_shoup_generate_keys():
    """ Generate new public and private keys for Cramer Shoup
    """
    print_option_header("generate keys for cramer-shoup")

    wait_to_continu()

    SCREEN.addstr("generating keys...\n")
    SCREEN.addstr("\n")

    CramerShoup.key_generation()

    SCREEN.addstr("keys have been generated !\n")
    SCREEN.addstr("\n")

    # wait before redirect to main menu
    wait_to_continu(next_step=show_main_menu)

def cramer_shoup_cipher():
    """ Ask the user the text he want to cipher, cipher it,
        and return the ciphertext to him
    """
    print_option_header("cipher with cramer-shoup")

    data = load_data(data_name="data to cipher")
    SCREEN.addstr("Ciphering...\n")
    # ciphertext is a list (b1, b2, c, v)
    ciphertext = CramerShoup.cipher(data)

    output_result(','.join([str(v) for v in ciphertext]), "cramer_shoup.cipher")
    # wait before redirect to main menu
    wait_to_continu(next_step=show_main_menu)

def cramer_shoup_decipher():
    """ Ask the user to put the text he want to decipher, decipher it,
        and return deciphertext to him
    """
    print_option_header("decipher a file with cramer-shoup")
    SCREEN.addstr("Please put your ciphertext in 'outputs/cramer_shoup.cipher' \n")
    # wait
    wait_to_continu()
    # cipher
    SCREEN.addstr("Reading the file...\n")
    content = read_file("cramer_shoup.cipher", directory="outputs")
    SCREEN.addstr("Deciphering the text...\n")
    deciphertext = CramerShoup.decipher(content)

    output_result(deciphertext, "cramer_shoup.decipher")
    # wait before redirect to main menu
    wait_to_continu(next_step=show_main_menu)

def threefish_cipher():
    """ Ask the user some configuration questions and the text he want to cipher,
        cipher it, and return the ciphertext to him
    """
    print_option_header("cipher with threefish")

    # ask the block size
    block_size = int(ask_question(
        question="Block size, in bits: '256', '512' or '1024' (default is '256')",
        answers=['256', '512', '1024'],
        default_answer='256'
    ))
    print_data(block_size, "Choosen block size:")

    key_length = ((block_size + 2*64) // 8)
    # ask the key, or generate it
    SCREEN.addstr("The format of the key for threefish is the following: \n")
    SCREEN.addstr("a unicode string of length (block_size + 2*64 bits) / 8. \n")
    SCREEN.addstr("(the 2 last words are the tweaks) \n")
    SCREEN.addstr("With the block_size you choose, the key must have a length of %d \n\n"
                  % key_length)
    generate_key = ask_question(
        question="Do you have a key ? If no, the key will be generated: 'yes' or 'no' (default is 'no')",
        answers=['yes', 'no'],
        default_answer='no'
    ) == "no"

    if generate_key:
        SCREEN.addstr("Generating a key...\n\n")
        key = generate_random_unicode_string(key_length)
        print_data(key, "Generated key")
        key = bytes(key, 'utf-8')
    else:
        SCREEN.addstr("You said that you already have a key.\n")
        key = load_data(data_name="threefish key")

    data = load_data(data_name="data to cipher")
    SCREEN.addstr("Ciphering...\n")
    # TODO: call the cipher method of threefish
    ciphertext = "yoloo"

    output_result(ciphertext, "threefish.cipher")
    # wait before redirect to main menu
    wait_to_continu(next_step=show_main_menu)

def threefish_decipher():
    """ Ask the user to put the text he want to decipher, decipher it,
        and return deciphertext to him
    """
    print_option_header("decipher a file with threefish")
    SCREEN.addstr("Please put your ciphertext in 'outputs/threefish.cipher' \n")
    # wait
    wait_to_continu()
    # cipher
    SCREEN.addstr("Reading the file...\n")
    content = read_file("threefish.cipher", directory="outputs")
    SCREEN.addstr("Deciphering the text...\n")
    # TODO: call the decipher method of threefish
    deciphertext = "yoloo"

    output_result(deciphertext, "threefish.decipher")
    # wait before redirect to main menu
    wait_to_continu(next_step=show_main_menu)

MENU_ITEMS = [
    ("Hash with SHA-1", sha1_hash),
    ("Check a SHA-1 hash", sha1_check),
    ("Generate keys for Cramer-Shoup", cramer_shoup_generate_keys),
    ("Cipher with Cramer-Shoup", cramer_shoup_cipher),
    ("Decipher with Cramer-Shoup", cramer_shoup_decipher),
    ("Cipher with Threefish", threefish_cipher),
    ("Decipher with Threefish", threefish_decipher),
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
