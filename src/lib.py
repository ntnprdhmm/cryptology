from math import sqrt
from functools import reduce

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
	while not (is_prime(i) and n % i == 0):
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
