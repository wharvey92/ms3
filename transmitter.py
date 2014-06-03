import math
import common_txrx as common
import numpy as np
#import matplotlib.pyplot as p

import hamming_db
import channel_coding as cc
 
class Transmitter:
    def __init__(self, carrier_freq, samplerate, one, spb, silence, cc_len):
        self.fc = carrier_freq  # in cycles per sec, i.e., Hz
        self.samplerate = samplerate
        self.one = one
        self.spb = spb
        self.silence = silence
        self.cc_len = cc_len
        print 'Transmitter: '
        
    def add_preamble(self, databits):
        '''
        Prepend the array of source bits with silence bits and preamble bits
        The recommended preamble bits is 
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        The output should be the concatenation of arrays of
            [silence bits], [preamble bits], and [databits]
        '''

        zeroBits = np.zeros(self.silence)
        preambleBits = [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        preambleBits = np.array(preambleBits)
        databits_with_preamble = np.append(zeroBits, preambleBits)
        databits_with_preamble = np.append(databits_with_preamble, databits)

        # fill in your implementation

        print '\tSent Preamble: ', preambleBits # fill in here
        return databits_with_preamble

    def bits_to_samples(self, databits_with_preamble):
        '''
        Convert each bits into [spb] samples. 
        Sample values for bit '1', '0' should be [one], 0 respectively.
        Output should be an array of samples.
        '''
        samples = np.array([])
        for x in databits_with_preamble:
            toAdd = self.one
            if x == 0:
                toAdd = 0
            for i in xrange(self.spb):
                samples = np.append(samples, toAdd)

        return samples
        
    def modulate(self, samples):
        '''
        Multiply samples by a local sinusoid carrier of the same length.
        Return the multiplied result.
        '''

        #Get modulated samples
        modulated_samples = [(samples[i] * math.cos(2 * math.pi * self.fc/self.samplerate * i)) for i in xrange(len(samples))]
        
        # fill in your implementation
        print '\tNumber of samples being sent:', len(modulated_samples)

        cut_off = 4 * math.pi * self.fc / self.samplerate



        filtered = common.lpfilter(modulated_samples, cut_off)

        return filtered


        
    def encode(self, databits, cc_len):
        '''
        Wrapper function for milestone 2. No need to touch it        
        '''
        return cc.get_frame(databits, cc_len)