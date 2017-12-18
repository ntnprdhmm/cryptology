import unittest
import string

from src._functions import monoalphabetic_substitution_cipher

class TestMonoalphabeticSubstitutionCipher(unittest.TestCase):

    def test_simple_encryption(self):
        message = "TROYES"
        encrypted_message = "NSIMUH"
        cypertext_alphabet = "OBLVUCGJRPTZKYIWXSHNADFEMQ"
        plaintext_alphabet = string.ascii_uppercase
        self.assertEqual(monoalphabetic_substitution_cipher(message, plaintext_alphabet, cypertext_alphabet), encrypted_message)

    def test_simple_decryption(self):
        message = "TROYES"
        encrypted_message = "NSIMUH"
        cypertext_alphabet = "OBLVUCGJRPTZKYIWXSHNADFEMQ"
        plaintext_alphabet = string.ascii_uppercase
        self.assertEqual(monoalphabetic_substitution_cipher(encrypted_message, cypertext_alphabet, plaintext_alphabet), message)

if __name__ == '__main__':
    unittest.main()
