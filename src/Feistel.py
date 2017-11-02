import utils

class Feistel:

    def __init__(self, m, k, func_F, func_next_subkey):
        # original message
        self.m = m
        # split the message in 2 blocks
        self.left = m[:(len(m)//2)]
        self.right = m[len(m)//2:]
        # the original key
        self.k = k
        # Feistel F function
        self.func_F = func_F
        # function to generate the next key
        self.func_next_subkey = func_next_subkey

    def get_ciphertext(self):
        return self.left + self.right

    def next_round(self):
        # generate the next subkey
        self.k = self.func_next_subkey(self.k)
        # calculate the result of func_F
        f = self.func_F(self.k, self.right)
        # calculate the new left and right
        next_left = self.right
        next_right = utils.binary_xor(self.left, f).zfill(len(self.m)//2)
        # set left and right attributes
        self.left, self.right = next_left, next_right

    def run(self, nb_rounds):
        """ Run 'nb_rounds' Feistel rounds
            and return the result
        """
        for _ in range(nb_rounds):
            self.next_round()
        return self.get_ciphertext()
