import numpy
import math
import operator

import binascii
# Methods common to both the transmitter and receiver.

def dot_vectors(vec1, vec2):
	dot_sum = 0
	if len(vec1) != len(vec2):
		print "Error: Dot product of two different length vectors"
		return -1

	for i in xrange(len(vec1)):
		dot_sum += vec1[i] * vec2[i]
	return dot_sum

def lpfilter(samples_in, omega_cut):
    '''
    A low-pass filter of frequency omega_cut.
    '''
    # set the filter unit sample response
    # convolve unit sample response with input samples
    # fill in your implementation
    
    return numpy.array(samples_out)