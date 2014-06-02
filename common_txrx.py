import numpy as np
import math
import operator

import binascii
# Methods common to both the transmitter and receiver.

k_limit = 2

def reverse_np_array(arr):
	return arr[::-1]

def perform_convolution(x, h):
	y = np.array([])
	rev_h = reverse_np_array(h)

	for n in xrange(len(x)):
		x_n_rev = [0 if (i < 0 or i >= len(x)) else x[i] for i in xrange(n - k_limit, n + k_limit + 1)]
		x_n = reverse_np_array(x_n_rev)
		y = np.append(y, np.dot(x_n, h))
	return y

def getlpfilter_vector(omega_cut):
	low_pass_filter = np.array([])
	for n in range(-k_limit, k_limit + 1):
		if n == 0:
			low_pass_filter = np.append(low_pass_filter, omega_cut/math.pi)
		else:
			val = math.sin(omega_cut * n)/(math.pi * n)
			low_pass_filter = np.append(low_pass_filter, val)

	return low_pass_filter

def lpfilter(samples_in, omega_cut):
    '''
    A low-pass filter of frequency omega_cut.
    '''
    # set the filter unit sample response
    # convolve unit sample response with input samples
    # fill in your implementation

    lpfilter_vec = getlpfilter_vector(omega_cut)

    


    return numpy.array(samples_out)