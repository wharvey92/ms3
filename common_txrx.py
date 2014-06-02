import numpy
import math
import operator

import binascii
# Methods common to both the transmitter and receiver.

def lpfilter(samples_in, omega_cut):
    '''
    A low-pass filter of frequency omega_cut.
    '''
    # set the filter unit sample response
    # convolve unit sample response with input samples
    # fill in your implementation
    
    return numpy.array(samples_out)