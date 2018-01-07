from src.Threefish import Threefish
from src._functions import generate_random_unicode_string

# size of a block, in bytes. Possible values: 32, 64, 128
block_size = 64
# generate a random key (with the 2 tweaks at the end)
key = bytes(generate_random_unicode_string(block_size + 16), 'utf-8')
# create a Threefish instance
threefish = Threefish(block_size, key)
# Generate the rounds keys
threefish.key_schedule()

# TEXT TO CIPHER
plaintext = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod \
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis \
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute \
irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. \
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim \
id est laborum."
print("TEXT TO CIPHER: " + plaintext + "\n")
plaintext = bytes(plaintext, 'utf-8')

# If you want CBC mode, set CBC to True
CBC = False
# CBC = True

if CBC:
    # CBC mode activated
    print("CBC MODE\n")
    # generate a random initialization vector
    IV = generate_random_unicode_string(block_size)
    print("INITIALIZATION VECTOR: " + IV + "\n")
    IV = bytes(IV, 'utf-8')
    # cipher in CBC mode
    ciphertext = threefish.cipher(plaintext, IV)
    print("CIPHERTEXT: " + str(ciphertext) + "\n")
    # decipher in CBC mode
    deciphered_text = threefish.decipher(ciphertext, IV)
    print("DECIPHERED TEXT: " + deciphered_text.decode('utf-8') + "\n")
else:
    # ECB mode
    print("ECB MODE\n")
    # cipher in ECB mode
    ciphertext = threefish.cipher(plaintext)
    print("CIPHERTEXT: " + str(ciphertext) + "\n")
    # decipher in ECB mode
    deciphered_text = threefish.decipher(ciphertext)
    print("DECIPHERED TEXT: " + deciphered_text.decode('utf-8') + "\n")
