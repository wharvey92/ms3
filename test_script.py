from common_txrx import getlpfilter_vector, perform_convolution
import numpy as np
from reciever import Receiver



x = np.array([1, 2, 4, 5, 6, 7, 8])
h = getlpfilter_vector(0.5)
print x
print h

print 
print 
print

print perform_convolution(x, h)
