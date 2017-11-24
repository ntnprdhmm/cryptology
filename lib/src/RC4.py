class RC4:

    # https://en.wikipedia.org/wiki/RC4

    def __init__(self, key):
        self.S = []
        self.key = key

    def key_scheduling(self):
        """ Initialise the permutation array S
        """
        self.S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + self.S[i] + ord(self.key[i % len(self.key)])) & 0xFF
            self.S[i], self.S[j] = self.S[j], self.S[i]

    def cipher(self, input):
        """ cipher the input
        """
        self.key_scheduling()
        
        output = [None] * len(input)
        i = 0
        j = 0
        for n in range(len(input)):
            i = (i + 1) & 0xFF
            j = (j + self.S[i]) & 0xFF
            self.S[i], self.S[j] = self.S[j], self.S[i]
            output[n] = chr((ord(input[n]) ^ self.S[(self.S[i] + self.S[j]) & 0xFF]))

        return ''.join(output)
