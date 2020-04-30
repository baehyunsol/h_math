'''
num: [int, int]  # [denom, numer]
'''

from collections import deque
import math


# int, int -> int
def gcd(a, b):

	if a < b:
		a, b = b, a

	while b != 0:
		a, b = b, a % b

	return a


# num, num -> num
def add(num1, num2):
	
	result = [num1[0] * num2[0], num1[0] * num2[1] + num1[1] * num2[0]]
	r = gcd(abs(result[0]), abs(result[1]))
	result = list(map(lambda x: x // r, result))
	return result


# num, int -> num
def add_int(num, n):
	
	return [num[0], num[1] + n * num[0]]


# num, num -> num
def sub(num1, num2):
	
	result = [num1[0] * num2[0], num1[1] * num2[0] - num1[0] * num2[1]]
	r = gcd(abs(result[0]), abs(result[1]))
	result = list(map(lambda x: x // r, result))
	return result


# num, int -> num
def sub_int(num, n):
	
	return [num[0], num[1] - n * num[0]]


# num, num -> num
def mul(num1, num2):
	
	result = [num1[0] * num2[0], num1[1] * num2[1]]
	r = gcd(abs(result[0]), abs(result[1]))
	result = list(map(lambda x: x // r, result))
	return result


# num, int -> num
def mul_int(num, n):
	
	result = [num[0], num[1] * n]
	r = gcd(abs(result[0]), abs(result[1]))
	result = list(map(lambda x: x // r, result))
	return result


# num, num -> num
def div(num1, num2):
	
	result = [num1[0] * num2[1], num1[1] * num2[0]]
	r = gcd(abs(result[0]), abs(result[1]))
	result = list(map(lambda x: x // r, result))
	return result


# num, int -> num
def div_int(num, n):
	
	result = [num[0] * n, num[1]]
	r = gcd(abs(result[0]), abs(result[1]))
	result = list(map(lambda x: x // r, result))
	return result


# num -> num
def neg(num):

	return [-num[0], num[1]]


# num -> boolean
def is_neg(num):

	return (num[0] * num[1]) < 0


# num -> num
def absolute(num):

	return [abs(num[0]), abs(num[1])]


# num, num -> boolean
def eq(num1, num2):

	diff = sub(num1, num2)

	if diff[1] == 0:
		return True

	else:
		return False


# num1 > num2
# num, num -> boolean
def gt(num1, num2):

	result = sub(num1, num2)

	if result[0] * result[1] > 0:
		return True

	else:
		return False


# num1 < num2
# num, num -> boolean
def lt(num1, num2):

	result = sub(num1, num2)

	if result[0] * result[1] < 0:
		return True

	else:
		return False

# num1 >= num2
# num, num -> boolean
def ge(num1, num2):

	return not lt(num1, num2)

# num1 <= num2
# num, num -> boolean
def le(num1, num2):

	return not gt(num1, num2)


# num, num -> boolean
def ne(num1, num2):

	return not eq(num1, num2)


# num -> num
def reciprocal(num):

	return [num[1], num[0]]


# num -> num
def floor(num):

	return [1, num[1] // num[0]]


# string -> num
def str_to_num(string):

	if string[0] == '-':
		neg = True
		string = string[1:]

	else:
		neg = False

	while string[0] == '0':
		string = string[1:]

	try:
		dot_index = string.index('.')

	except ValueError:
		return int(string)
		
	string = string[:dot_index] + string[dot_index + 1:]

	denom = int(10 ** (len(string) - dot_index))
	numer = int(string)
	r = gcd(numer, denom)
	return [denom // r, numer // r]


# int -> num
def int_to_num(integer):

	return [1, integer]


# num, int=50 -> deque([int])
def get_decimal_digits(num, value_length=9):

	result = deque()

	denom, numer = num

	for _ in range(value_length):
		result.append(numer // denom)
		numer, denom = (numer % denom) * 10, denom
	
	return result