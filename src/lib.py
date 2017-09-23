from math import sqrt

def gcd(a, b):
	""" Calculate the greatest common divisor of 'a' and 'b' recusively
		Using the euclidean algorithm
	"""

	# 'a' has to be greater than 'b'
	if b > a:
		a, b = b, a

	# calculate the remainder of a/b
	remainder = a % b

	# if remainder is 0, stop here : gcd found
	if remainder == 0:
		return b

	# else, continue
	return gcd(b, remainder)


def lcm(a, b):
	""" Search the lowest positive integer than can be devide
		by 'a' and 'b'
	"""
	return (a*b) // gcd(a, b)


def bezout(a, b, x = 0, prev_x = 1, y = 1, prev_y = 0):
	""" Calculate the Bézout's identity of 'a' and 'b' recursively
		Using the extended euclidean algorithm
	"""

	# 'a' has to be greater than 'b'
	if b > a:
		a, b = b, a

	# calculate the remainder of a/b
	remainder = a % b

	# if remainder is 0, stop here : gcd found
	if remainder == 0:
		return b, x, y

	# else, update x and y, and continue
	quotient = a // b
	prev_x, prev_y, x, y = x, y, quotient*x + prev_x, quotient*y + prev_y
	return bezout(b, remainder, x, prev_x, y, prev_y)


def find_negative_factor(a, b, gcd, x, y):
	""" Given 'a' and 'b', and the 2 factors 'x' and 'y'
		found with the extended euclidean algorithm,
		search wich factor is negative in the bezout equation.

		we want gcd(a, b) = a * x + b * y

		This function print the result and return new 'x' and 'y'
	"""
	if a*x - b*y == gcd:
		y = -y
	elif -a*x + b*y == gcd:
		x = -x
	elif a*y - b*x == gcd:
		x, y = y, -x
	elif -a*y + b*x == gcd:
		x, y = -y, x

	if y > 0:
		print("1 = %d x %d + %d x %d" % (x, a, y, b))
	else:
		print("1 = %d x %d %d x %d" % (x, a, y, b))

	return x, y


def are_coprime(a, b):
	""" Two integers are coprime if their gcd is 1
	"""
	return gcd(a, b) is 1


def is_prime(n):
	""" A number is prime if it can be devide only by 1 and himself
		Check from 2 to sqrt(n). After sqrt(n) the numbers are redondant
	"""
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


g, x, y = bezout(100, 35)
print("%d, %d, %d" % (g, x, y))
print(find_negative_factor(100, 35, g, x, y))

print(are_coprime(13,5))
print(are_coprime(225,5))

print(is_prime(7))
print(is_prime(23))
print(is_prime(10))

print(prime_decomposition(2088))
