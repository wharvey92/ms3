import numpy as np


one = 4
spb = 3

databits_with_preamble = [1, 0, 0, 0, 0, 1, 1, 1]

samples = np.array([])
for x in databits_with_preamble:
	toAdd = one
	if x == 0:
		toAdd = 0
	for i in xrange(spb):
		samples = np.append(samples, toAdd)

print samples