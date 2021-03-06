from collections import deque
from hmath import num


add = num.add
sub = num.sub
mul = num.mul
div = num.div
reciprocal = num.reciprocal


# int -> int
def factorial(n):

	if n < 16:
		return [
			1, 1, 2, 6, 24,
			120, 720, 5040, 40320, 362880,
			3628800, 39916800, 479001600, 6227020800, 87178291200,
			1307674368000, 20922789888000
		][n]

	return n * factorial(n - 1)


# int -> int
def fibonacci(n):

	result = [
		0, 1, 1, 2, 3,
		5, 8, 13, 21, 34,
		55, 89, 144, 233, 377,
		610, 987, 1597, 2584, 4181,
		6765, 10946, 17711
	]

	if n < 23:
		return result[n]

	while len(result) <= n:
		result.append(result[-1] + result[-2])
		
	return result[n]


# int -> [int]
def prime_factorial(n):

	result = deque()
	
	for p in pn:

		while n % p == 0:
			n //= p
			result.append(p)

		if p * p > n:

			if n != 1:
				result.append(n)

			return list(result)

	div = pn[-1]

	while div * div <= n:

		while n % div == 0:
			n //= div
			result.append(div)

		div += 2

	if n != 1:
		result.append(n)

	return list(result)


# [int] -> [int]
def get_divisors(prime_factorials):

	primes = []
	factors = []
	divisors = [1]
	index = -1

	for p in prime_factorials:

		if p not in primes:
			primes.append(p)
			factors.append(1)
			index += 1

		else:
			factors[index] += 1

	for a in range(len(factors)):

		for b in range(len(divisors)):

			for c in range(1, factors[a] + 1):
				divisors.append(divisors[b] * (primes[a] ** c))

	divisors.sort()

	return divisors


# int -> bool
def is_pn(num):

  num = abs(num)

  if num == 1 or num == 0:
    return False
  
  if num in pn:
    return True

  for p in pn:

    if num % p == 0:
      return False

    if p * p > num:
      return True

  div = pn[-1]

  while div * div <= num:

    if num % div == 0:
      return False

    div += 2

  return True


# num, int=50 -> deque([int])
def get_continued_fraction(x, limit=50):

	result = deque()
	
	for _ in range(limit):

		integer = x[1] // x[0]
		result.append(integer)
		x = reciprocal(sub(x, (1, integer)))

		if x[0] == 0:
			break

	return result


# deque([int]) -> num
def continued_fraction_to_num(continued_fraction):

	continued_fraction = deque(list(continued_fraction))  # copy continued_fraction
	
	result = [0, 1]

	while len(continued_fraction) > 0:
		result = reciprocal(result)
		result = add(result, (1, continued_fraction.pop()))

	return result


# func, func, num=(1, 0), num=(1, 0), int=8 -> num
# each func:num->num
# returns x that f(x) is y
def newton_method(f, f_prime, y=(1, 0), begin=(1, 0), limit=8):
  
    a = begin

    while f_prime(a)[0] == 0 or f_prime(a)[1] == 0:
        a = add(a, (1, 1))

    for _ in range(limit):
        a = sub(a, div(sub(f(a), y), f_prime(a)))

    return a


pn = [
  2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
  47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
  107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
  167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227,
  229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
  283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353,
  359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421,
  431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487,
  491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569
]