def gcd(a, b):
	# 'a' has to be greater than 'b'
	if b > a:
		a, b = b, a
	return euclide(a, b)

def lcm(a, b):
	pass

def bezout(a, b):
	# 'a' has to be greater than 'b'
	if b > a:
		a, b = b, a

	gdc, x, y = extended_euclidean_algorithm(a, b)
	x, y = find_negative_factor(a, b, x, y) 
	return x, y

def find_negative_factor(a, b, x, y):
	# we want : 1 = a * x + b * y
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

def euclidean_algorithm(a, b):
	# calculate the remainder of a/b
	remainder = a % b

	# if remainder is 0, stop here : gcd found
	if remainder == 0:
		return b
	
	# else, continue 
	return euclidean_algorithm(b, remainder)

def extended_euclidean_algorithm(a, b, x = 0, prev_x = 1, y = 1, prev_y = 0):
	# calculate the remainder of a/b
	remainder = a % b

	# if remainder is 0, stop here : gcd found
	if remainder == 0:
		return b, x, y

	# else, update x and y, and continue
	quotient = a // b
	prev_x, prev_y, x, y = x, y, quotient*x + prev_x, quotient*y + prev_y 

	return extended_euclidean_algorithm(b, remainder, x, prev_x, y, prev_y)


print(bezout(1112, 325))
print(bezout(124, 235))
