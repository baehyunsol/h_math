from hmath import num
from hmath import funcs_math
from hmath import funcs_etc
from collections import deque


calpi = funcs_math.calculate_pi
cale = funcs_math.calculate_e

sin = funcs_math.sin
cos = funcs_math.cos
tan = funcs_math.tan
sec = funcs_math.sec
csc = funcs_math.csc
cot = funcs_math.cot

sinh = funcs_math.sinh
cosh = funcs_math.cosh
tanh = funcs_math.tanh
sech = funcs_math.sech
csch = funcs_math.csch
coth = funcs_math.coth

exp = funcs_math.exp
root = funcs_math.root
power = funcs_math.power
pwalt = funcs_math.power_alternative
pwin = funcs_math.power_int

ln = funcs_math.ln
log = funcs_math.log

reci = num.reciprocal

gcd = num.gcd
fac = funcs_etc.factorial
fib = funcs_etc.fibonacci

nutmet= funcs_etc.newton_method

prf = funcs_etc.prime_factorial
getdv = funcs_etc.get_divisors

str2num = num.str_to_num
int2num = num.int_to_num

getdd = num.get_decimal_digits
getcfr = funcs_etc.get_continued_fraction
cfr2num = funcs_etc.continued_fraction_to_num

add = num.add
sub = num.sub
mul = num.mul
div = num.div

gt = num.gt
lt = num.lt
eq = num.eq

deque = deque


def printn(n, limit=9, print_result=True):

	deq = getdd(n, limit)
	result = str(deq.popleft())
	
	if len(deq) > 0:
		result += '.'

	while len(deq) > 0:
		result += str(deq.popleft())

	if print_result:
		print(result)

	return result