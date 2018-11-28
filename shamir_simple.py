import random
import sys
from argparse import ArgumentParser

# max value of X
MAX_X = 100

# Need exactly N keys out of K keys to get the secret S back
N, K, S = 4, 7, 29

# coefficients for the function
C = [S, 12, 5, 42, 91]

_usage = '''Usage: Enter space separated values for mentioned
type, X or Y. eg:
X: x1 x2 x3 ...
Y: y1 y2 y3 ...
'''

def f(x):
	_x, _s = 1, 0
	for v in C:
		_s = _s + v * _x
		_x = _x * x 
	return _s

def create_keys():
	if K < N:
		print >> sys.stderr, "Number of Keys generated should be more than equal to the quorum"
		return []

	X = []
	# generate keys
	while len(X) < K:
		r = random.randint(1, MAX_X)
		if r not in X:
			X.append(r)

	Y = [f(x) for x in X]

	# return all keys [(x, y),...]
	return zip(X, Y)

def get_secret(keys, N):
	if len(keys) < N + 1:
		print >> sys.stderr, "Need at least {} keys to get secret".format(N + 1)
		return None

	X = [k[0] for k in keys]
	Y = [k[1] for k in keys]

	S = 0.0
	for i in range(N + 1):
		_num = 1.0
		_den = 1.0
		for j in range(N + 1):
			if j != i:
				_num = _num * X[j]
				_den = _den * (X[j] - X[i])
		S += (float(Y[i]) * _num ) / _den

	return S 

if __name__ == '__main__':
	p = ArgumentParser(description="Demonstrate Shamir Secret Sharing")
	p.add_argument("opt", help="Options=gen, solve")

	args = p.parse_args()

	if args.opt == 'gen':
		print "\n".join(["{}, {}".format(x, y) for x, y in create_keys()])

	elif args.opt == 'solve':
		print >> sys.stderr, _usage
		X = map(int, raw_input('X: ').split())
		Y = map(int, raw_input('Y: ').split())
		if len(X) != N + 1 or len(Y) != N + 1:
			print >> sys.stderr, "Need atleast {} keys".format(N + 1)
			sys.exit(-1)

		print get_secret(zip(X, Y), N)
	else:
		p.print_usage()
		sys.exit(-1)
