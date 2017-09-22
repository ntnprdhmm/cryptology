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
	return euclidean_algorithm(b, remainder)


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
		# search wich factor is negative and print the equation
		x, y = find_negative_factor(a, b, x, y)
		return b, x, y

	# else, update x and y, and continue
	quotient = a // b
	prev_x, prev_y, x, y = x, y, quotient*x + prev_x, quotient*y + prev_y 
	return extended_euclidean_algorithm(b, remainder, x, prev_x, y, prev_y)
 


def find_negative_factor(a, b, x, y):
	""" Given 'a' and 'b', and the 2 factors 'x' and 'y'
		found with the extended euclidean algorithm, 
		search wich factor is negative in the bezout equation.

		we want 1 = a * x + b * y

		This function print the result and return new 'x' and 'y'
	"""
	if a*x - b*y == 1:
		y = -y
	elif -a*x + b*y == 1:
		x = -x
	elif a*y - b*x == 1:
		x, y = y, -x
	elif -a*y + b*x == 1:
		x, y = -y, x
	
	if y > 0:
		print("1 = %d x %d + %d x %d" % (x, a, y, b))
	else:
		print("1 = %d x %d %d x %d" % (x, a, y, b))

	return x, y


