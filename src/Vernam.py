from src import utils

class Vernam:

    def xor(self, T, K):
        """ plaintext xor key = ciphertext
    	 	ciphertext xor key = plaintext
    			- T is the ciphertext or the plaintext
    			- K is the key

            Using XOR, we can use the same method to cipher and decipher
    	"""
        # make sure the key is at least as big as the text
        if len(K) < len(T):
            sys.exit("The key is smaller than the text")

        # convert both text and key in binary
        bT = utils.utf8_to_binary(T)
        bK = utils.utf8_to_binary(K)

        # c[i] = t[i] xor k[i]
        C = ''.join([str(int(bT[i])^int(bK[i])) for i in range(len(bT))])

        return utils.binary_to_utf8(C)
