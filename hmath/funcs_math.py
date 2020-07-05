from hmath import num
from collections import deque


add = num.add
sub = num.sub
mul = num.mul
div = num.div

add_int = num.add_int
sub_int = num.sub_int
mul_int = num.mul_int
div_int = num.div_int

neg = num.neg
absolute = num.absolute

gt = num.gt
lt = num.lt
eq = num.eq

reciprocal = num.reciprocal


# int=24 -> num
def calculate_pi(accuracy=12):

	each = [1, 1]
	pi = [1, 0]

	for k in range(accuracy):
		pi = add(mul(add(add((8 * k + 1, 4), (8 * k + 4, -2)), add((8 * k + 5, -1), (8 * k + 6, -1))), each), pi)
		each[0] *= 16

	return pi


# int=12 -> num
def calculate_e(accuracy=12):

	e = [1, 0]
	each = [1, 1]

	# taylor series
	for n in range(1, accuracy):
		e = add(e, each)
		each[0] *= n

	return e


# num, int=7 -> num
def exp(x, accuracy=7):

	while gt(absolute(x), (3, 2)):
		x = div_int(x, 6)
		return power_int(exp(x, accuracy), 6)

	each = [1, 1]
	result = [1, 0]

	# taylor series
	for n in range(1, accuracy):
		result = add(result, each)
		each[0] *= n
		each = mul(each, x)

	return result


# num, int=8 -> num
def sin(x, accuracy=8):

	result = [1, 0]
	each = x
	x_sqr = mul(x, x)

	# taylor series
	for n in range(1, accuracy):
		result = add(result, each)
		each = mul(each, x_sqr)
		each[0] *= -(4 * n * n + 2 * n)

	return result


# num, int=8 -> num
def cos(x, accuracy=8):

	result = [1, 0]
	each = [1, 1]
	x_sqr = mul(x, x)

	# taylor series
	for n in range(1, accuracy):
		result = add(result, each)
		each = mul(each, x_sqr)
		each[0] *= 2 * n - 4 * n * n

	return result


# num, int=8 -> num
def tan(x, accuracy=8):

	return div(sin(x, accuracy), cos(x, accuracy))


# num, int=8 -> num
def sec(x, accuracy=8):

	cos_ = cos(x, accuracy)
	return reciprocal(cos_)


# num, int=8 -> num
def csc(x, accuracy=8):

	sin_ = sin(x, accuracy)
	return reciprocal(sin_)


# num, int=8 -> num
def cot(x, accuracy=8):

	return div(cos(x, accuracy), sin(x, accuracy))


# num, int=12 -> num
def sinh(x, accuracy=12):

	ex = exp(x, accuracy)
	ex2 = reciprocal(ex)

	return div_int(sub(ex, ex2), 2)


# num, int=12 -> num
def cosh(x, accuracy=12):

	ex = exp(x, accuracy)
	ex2 = reciprocal(ex)

	return div_int(add(ex, ex2), 2)


# num, int=12 -> num
def tanh(x, accuracy=12):

	ex = exp(x, accuracy)
	ex2 = reciprocal(ex)

	return div(sub(ex, ex2), add(ex, ex2))


# num, int=12 -> num
def sech(x, accuracy=12):

	ex = exp(x, accuracy)
	ex2 = reciprocal(ex)

	return div((1, 2), add(ex, ex2))


# num, int=12 -> num
def csch(x, accuracy=12):

	ex = exp(x, accuracy)
	ex2 = reciprocal(ex)

	return div((1, 2), sub(ex, ex2))


# num, int=12 -> num
def coth(x, accuracy=12):

	ex = exp(x, accuracy)
	ex2 = reciprocal(ex)

	return div(add(ex, ex2), sub(ex, ex2))


# num, int=8 -> num
def asin(x, accuracy=8):
	
	# taylor series
	each = x
	result = [1, 0]
	x_squared = mul(x, x)

	for n in range(accuracy):
		result = add(each, result)
		each = mul(each, x_squared)
		each = mul(each, (4 * n * n + 10 * n + 6, 4 * n * n + 4 * n + 1))

	return result


# num, int=8 -> num
def acos(x, accuracy=8):

	raise NotImplementedError


# num, int=16 -> num
def atan(x, accuracy=16):

	if gt((1, 1), x):
		raise NotImplementedError

	# taylor series
	result = [1, 0]
	coeff = [1, 1]
	each = x
	minus_x_squared = neg(mul(x, x))

	for n in range(accuracy):
		coeff[0] = 2 * n + 1
		result = add(result, mul(each, coeff))
		each = mul(each, minus_x_squared)

	return result


# x ^ n
# num, int=2 -> num  # n > 0
def power_int(x, n=2):
	
	# power2s[n] = x^(2^n)
	power2s = [(x[0], x[1])]
	index = 1

	result = (1, 1)

	while index < n:
		power2s.append(mul(power2s[-1], power2s[-1]))
		index *= 2

	n_in_binary = []

	while n >= 1:
		n_in_binary.append(n % 2)
		n //= 2

	for i in range(len(n_in_binary)):

		if n_in_binary[i] == 1:
			result = mul(result, power2s[i])

	return result


# a ^ x
# num, num, int=6 -> num
def power(a, x, accuracy=6):

	x = mul(x, ln(a, accuracy))
	return exp(x, accuracy)


# a ^ x (whem the denominator and the numerator of x are small enough)
# num, num, int=6 -> num
def power_alternative(a, x, accuracy=6):

	return root(power_int(a, x[1]), x[0], accuracy)


# x ^ (1 / order)
# num, int=2, int=6 -> num
def root(x, order=2, accuracy=6):

	# make |x -1 | < 1
	coeff = [1, 1]

	cuts = [
		(3, 4),
		(8, 9),
		(15, 16),
		(24, 25),
		(125, 126)
	]

	if order > 10:
		cuts.append((1024, 1025))

	for c in cuts:
		powered = power_int(c, order)

		while gt(x, powered):
			coeff = mul(coeff, c)
			x = div(x, powered)

	# taylor series
	x = sub(x, (1, 1))
	result = [1, 0]
	each = [1, 1]

	for n in range(accuracy):
		result = add(result, each)
		each = mul(each, (order * (n + 1), 1 - order * n))
		each = mul(each, x)

	return mul(result, coeff)


# num, int=7 -> num
def ln(x, accuracy=7):
  
  if x[0] * x[1] <= 0:
    raise ValueError

	coeff = [1, 1]

	while gt(x, (5, 6)):
		x = root(x, 5, accuracy)
	  coeff = mul_int(coeff, 5)

	# taylor series
	x = sub(x, (1, 1))
	result = [1, 0]
	each = [-1, 1]
	denom = [1, 1]

	for n in range(1, accuracy):
		denom[0] = n
		each = mul(each, neg(x))
		result = add(result, mul(each, denom))

	return mul(result, coeff)


# log_a(x)
# num, num, int=7 -> num
def log(a, x, accuracy=7):
	
	return div(ln(x, accuracy), ln(a, accuracy))
