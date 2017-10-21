import sys
from math import sqrt
from functools import reduce
from random import randint

import utils

def gcd(a, b):
	""" Calculate the greatest common divisor of 'a' and 'b' recusively
		Using the euclidean algorithm
	"""
	return euclidean_algorithm(a, b)


def lcm(a, b):
	""" Search the lowest positive integer than can be devide
		by 'a' and 'b'
	"""
	return (a*b) // gcd(a, b)


def bezout(a, b):
	""" Calculate the Bézout's identity of 'a' and 'b'
	"""
	gcd, x, y = euclidean_algorithm(a, b, extended=True)

	# if x and y are reversed, fix it
	if (a*x + b*y) != gcd:
		x, y = y, x

	# print Bezout identity
	print("BEZOUT(%d, %d) : %d * %d + %d * %d = %d " % (a, b, x, a, y, b, gcd))

	return gcd, x, y


def euclidean_algorithm(a, b, x = 0, prev_x = 1, y = 1, prev_y = 0, extended=False, step=1):
	""" Run the euclidean algorithm to calculate the gcd of a and b
		If extended is True, calculate x and y for the Bézout's identity

		Step is usefull to know which factor is negative => if even, it's 'y' else it's 'x'
	"""
	# 'a' has to be greater than 'b'
	if b > a:
		a, b = b, a

	# calculate the remainder of a/b
	remainder = a % b

	# if remainder is 0, stop here : gcd found
	if remainder == 0:
		if not extended:
			return b
		else:
			# use the step parameter to calculate which factor is negative
			x *= (-1)**step
			y *= (-1)**(step+1)
			return b, x, y

	# we continue
	if extended:
		# if extended, update x and y and increment the step
		step += 1
		quotient = a // b
		prev_x, prev_y, x, y = x, y, quotient*x + prev_x, quotient*y + prev_y
		return euclidean_algorithm(b, remainder, x, prev_x, y, prev_y, extended=True, step=step)
	else:
		return euclidean_algorithm(b, remainder, step=step)

def are_coprime(a, b):
	""" Two integers are coprime if their gcd is 1
	"""
	return gcd(a, b) is 1


def is_prime(n):
	""" A number is prime if it can be devide only by 1 and himself
		Check from 2 to sqrt(n). After sqrt(n) the numbers are redondant
	"""
	if n == 1:
		return False

	for i in range(2, int(sqrt(n))):
		if n % i == 0:
			return False
	return True


def prime_decomposition(n, primes = []):
	""" Find the prime numbers pn (recursively) so that
		n = p1^a1 * p2^a2 * ... * pn^an
	"""
	if n <= 1:
		return primes

	i = 2
	while not n % i == 0:
		i += 1
	primes.append(i)

	return prime_decomposition(n // i, primes)


def exponentiation_by_squaring(n, exp):
	""" Fast way to do Exponentiation, recursively
	"""
	# stop when exp is 1
	if exp == 1:
		return n

	if exp % 2 == 1:
		return n * exponentiation_by_squaring(n**2, (exp-1)//2)
	else:
		return exponentiation_by_squaring(n**2, exp//2)


def inverse(n, mod):
	""" Calculate the inverse of 'n' modulo 'mod'
		using bezout identity
	"""
	gcd, x, y = bezout(n, mod)
	return x


def chinese_remainder_theorem(values, modulos):
	""" Solve the following system of congruences
			x = a1 (mod m1)
			x = a2 (mod m2)
			...
			x = an (mod mn)

		'values' is an array, which contains a1, a2, ..., an
		'modules' is an array, which contains m1, m2, ..., mn

		return 'x'
	"""

	M = reduce(lambda x, y: x * y, modulos, 1)
	x = 0

	# for each equation in the system
	for i in range(len(modulos)):
		Mi = M // modulos[i]
		x += values[i] * Mi * inverse(Mi, modulos[i])

	return x


def phi(n):
	""" Euler's totient function. Count the number of integers that
		are relative primes with n in range [1, n-1]
	"""

	# if n is prime, all numbers < n are prime with it
	if is_prime(n):
		return n-1

	# get the integers that are part of the prime decomposition of n
	primes = list(set(prime_decomposition(n, [])))

	result = n
	for prime in primes:
		result *= (1 - (1 /prime))
	return int(result)


def sieve_of_eratosthenes(n):
	""" Search and return the integers lower or equals to 'n'
	"""
	primes = []
	numbers = range(2, n+1)

	# continu while there are numbers
	while len(numbers):
		# the first is a prime
		primes.append(numbers[0])

		# remove all the multiple of the first number
		next_numbers = []
		for i in range(1, len(numbers)):
			if numbers[i] % numbers[0] > 0:
				next_numbers.append(numbers[i])
		numbers = next_numbers

	return primes


def fermat_primality_test(n, k = 1):
	""" Probabilistic test to determine if 'n' is prime
	"""
	if n < 2:
		return False

	if n > 3:
		for _ in range(k):
			a = randint(2, n-2)
			if exponentiation_by_squaring(a, n-1) % n != 1:
				return False

	return True


def miller_rabin_primality_test(n, k = 1):
	""" Probabilistic test to determine if 'n' is prime
	"""
	if n < 2:
		return False

	# special case
	if n == 2:
		return True

	# ensure n is odd
	if n % 2 == 0:
		return False

	# write n-1 as 2^s * d
	# by repeatedly dividing n-1 by 2
	s = 0
	d = n - 1
	while True:
		quotient, remainder = divmod(d, 2)
		if remainder == 1:
			break
		s += 1
		d = quotient

	def is_composite(a):
		if exponentiation_by_squaring(a, d) % n == 1:
			return False
		for i in range(s):
			if exponentiation_by_squaring(a, 2**i * d) % n == n-1:
				return False
		return True

	# do k tests
	for _ in range(k):
		# pick random int
		a = randint(2, n-2)
		# check 'a' to see whether it is a witness for the compositeness of 'n'
		if is_composite(a):
			return False

	# nothing showed that 'n' is composite
	return True


def vernam(M, K):
	""" plaintext xor key = ciphertext
	 	ciphertext xor key = plaintext
			- M is the text
			- K is the key
	"""
	# make sure the key is at least as big as the message
	if len(K) < len(M):
		sys.exit("The key is smaller than the message")

	# convert both message and key in binary
	bM = utils.utf8_to_binary(M)
	bK = utils.utf8_to_binary(K)

	# c[i] = m[i] xor k[i]
	C = ''.join([str(int(bM[i])^int(bK[i])) for i in range(len(bM))])

	# return M encrypted with K
	return utils.binary_to_utf8(C)


def simple_lfsr(register, taps):
	"""	Given a register and a list of tap
		print all the successive states of the register
	"""
	states = {} # avoid infine loop on same states

	R = register
	print(R)
	while 1:
		# xor the taps
		xor = 0
		for tap in taps:
			xor ^= int(R[tap])
		# update R
		R = str(xor) + R[:len(R)-1]
		print(R)
		# stop when R is the initial register
		if R == register or R in states:
			break
		# put this state in the dic
		states[R] = 1

#simple_lfsr('0110', [0, 1, 3])
#simple_lfsr('011001', [0, 1, 3])
