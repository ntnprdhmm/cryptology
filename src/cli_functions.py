#!usr/bin/env python3

""" This module contains all the functions to build the menu and the menu's
    options handlers (ciphering functions, ..)
"""

import curses
from src.SHA1 import SHA1
from src.CramerShoup import CramerShoup
from src.utils import (read_file, write_file)
from src.cli_utils import (SCREEN, wait_to_continu, print_option_header, ask_question,
                           print_data)

def sha1_hash_text():
    """ Ask the user to enter the text he wants to hash,
        hash it, and print the result
    """
    print_option_header("hash a text with sha-1")

    text = ask_question("Please enter the text you want to hash")
    # hash the text
    SCREEN.addstr("Hashing your text...\n")
    text_hash = SHA1().hash(text)
    print_data(text_hash, "Here's your hash:", done=True)
    # wait before redirect to main menu
    wait_to_continu(next_step=show_main_menu)

def check_sha1_hash_text():
    """ Ask the user to enter a hash and the hashed text.
        Check if it's the right text by hashing the text and comparing the 2 hashs.
    """
    print_option_header("check a text's sha-1 hash")

    true_hash = ask_question("Please enter the true hash of the text", to_string=True)

    text = ask_question("Please enter the text you want to verify")

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

def sha1_hash_file():
    """ Ask the user to enter the name of the file he wants to hash,
        read the content of the file, hash it, and print the result
    """
    print_option_header("hash a file with sha-1")

    filename = ask_question("Put your file in the 'assets' directory\nand enter the \
                            complete file name (with the extension):", to_string=True)
    # read the content of the file to hash
    content = read_file(filename, read_bytes=True)
    # hash the file
    SCREEN.addstr("Hashing your file...\n")
    file_hash = SHA1().hash(content)
    # print the hash
    print_data(file_hash, "Here's your hash:")
    # wait before redirect to main menu
    wait_to_continu(next_step=show_main_menu)

def check_sha1_hash_file():
    """ Ask the user to enter the name of a file and the hashed file.
        Check if it's the right file by hashing the file and comparing the 2 hashs.
    """
    print_option_header("check a file's sha-1 hash")

    true_hash = ask_question("Enter the true hash of the file", to_string=True)

    message = "Put your file in the 'assets' directory\nand enter the complete file name (with the extension):"
    filename = ask_question(message, to_string=True)

    # read the content of the file to hash
    content = read_file(filename, read_bytes=True)
    # hash the file
    SCREEN.addstr("Hashing your file...\n")
    file_hash = SHA1().hash(content)
    # print the hash
    print_data(file_hash, "Here's your hash:")

    # print the result
    if file_hash == true_hash:
        SCREEN.addstr("SUCCESS: The file hasn't been modified.\n")
    else:
        SCREEN.addstr("WARNING: The file has been modified.\n")

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

def cramer_shoup_cipher_file():
    """ Ask the user to put the text he want to cipher in a specific file,
        read the content of the file, cipher it, and put the content in a file
    """
    print_option_header("cipher a file with cramer-shoup")
    SCREEN.addstr("Please put your text in 'assets/cramer_shoup.txt' \n")
    # wait
    wait_to_continu()
    # cipher
    SCREEN.addstr("Reading the file content...\n")
    content = read_file("cramer_shoup.txt", read_bytes=True)
    SCREEN.addstr("Ciphering the file...\n")
    # ciphertext is a list (b1, b2, c, v)
    ciphertext = CramerShoup.cipher(content)
    # write the ciphertext in a file
    write_file('cramer_shoup.cipher', ','.join([str(v) for v in ciphertext]))
    # done !
    SCREEN.addstr("\n")
    SCREEN.addstr("DONE ! \n")
    SCREEN.addstr("you can find the result in 'outputs/cramer_shoup.cipher'\n")
    # wait before redirect to main menu
    wait_to_continu(next_step=show_main_menu)

def cramer_shoup_decipher_file():
    """ Ask the user to put the text he want to decipher in a specific file,
        read the content of the file, decipher it, and put the content in a file
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
    # write the decipher text in a file
    write_file('cramer_shoup.decipher', deciphertext)
    # done !
    SCREEN.addstr("\n")
    SCREEN.addstr("DONE ! \n")
    SCREEN.addstr("you can find the result in 'outputs/cramer_shoup.decipher'\n")
    # wait before redirect to main menu
    wait_to_continu(next_step=show_main_menu)

def cramer_shoup_cipher_text():
    pass

def cramer_shoup_decipher_text():
    pass

MENU_ITEMS = [
    ("Hash a text with SHA-1", sha1_hash_text),
    ("Check a text's SHA-1 hash", check_sha1_hash_text),
    ("Hash a file with SHA-1", sha1_hash_file),
    ("Check a file's SHA-1 hash", check_sha1_hash_file),
    ("Generate keys for Cramer-Shoup", cramer_shoup_generate_keys),
    ("Cipher a text with Cramer-Shoup", cramer_shoup_cipher_text),
    ("Decipher a text with Cramer-Shoup", cramer_shoup_decipher_text),
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
