class Caesar:
    """ Caesar cipher for utf-8 strings
    """

    def __init__(self, shift):
        self.shift = shift

    def cipher(self, plaintext):
        return ''.join([chr((ord(c) + self.shift) & 0xFF) for c in plaintext])

    def decipher(self, ciphertext):
        return ''.join([chr((ord(c) + (256 - self.shift)) & 0xFF) for c in ciphertext])
