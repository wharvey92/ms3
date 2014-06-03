import numpy as np


k_limit = 2

def reverse_np_array(arr):
	return arr[::-1]

def perform_convolution(x, h):
	y = np.array([])
	rev_h = reverse_np_array(h)

	for n in xrange(len(x)):
		x_n_rev = [0 if (i < 0 or i >= len(x)) else x[i] for i in xrange(n - k_limit, n + k_limit + 1)]
		x_n = reverse_np_array(x_n_rev)

		print x_n
		print h
		print

		y = np.append(y, np.dot(x_n, h))
	return y



print perform_convolution([1, 2, 3, 4, 5, 6], [-1, -2, 3, 1, 2])