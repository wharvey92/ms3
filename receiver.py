import sys
import math
import cmath
import numpy as np
#import matplotlib.pyplot as p
import scipy.cluster.vq
import common_txrx as common
from graphs import *
import random
from numpy import linalg as LA
from operator import itemgetter


import hamming_db
import channel_coding as cc

class Receiver:
    def __init__(self, carrier_freq, samplerate, spb):
        '''
        The physical-layer receive function, which processes the
        received samples by detecting the preamble and then
        demodulating the samples from the start of the preamble 
        sequence. Returns the sequence of received bits (after
        demapping)
        '''
        self.fc = carrier_freq
        self.samplerate = samplerate
        self.spb = spb 
        print 'Receiver: '

    def detect_threshold(self, demod_samples):
        '''
        Returns representative sample values for bit 0, 1 and the threshold.
        Use kmeans clustering with the demodulated samples
        '''

        clusters, centroids = self.kmeans_clustering(np.array(demod_samples), 2)
        one = max(centroids)
        zero = min(centroids)
        thresh = 1.0 * (one + zero) / 2
        return one, zero, thresh
 
    def detect_preamble(self, demod_samples, thresh, one):
        '''
        Find the sample corresp. to the first reliable bit "1"; this step 
        is crucial to a proper and correct synchronization w/ the xmitter.
        '''

        '''
        First, find the first sample index where you detect energy based on the
        moving average method described in the milestone 2 description.
        '''


        energy_offset = 0
        while(True):
            currSamples = demod_samples[energy_offset: energy_offset + self.spb]

            #print "currsamples - detect_preamble", currSamples

            middleIndex = self.spb / 2
            samplesToAvg = currSamples[middleIndex - (self.spb / 4): middleIndex + (self.spb / 4)]
            samplesToAvg = np.array(samplesToAvg)

            #print "samplesToAvg - detect_preamble", samplesToAvg

            avg = np.average(samplesToAvg)

            if len(samplesToAvg) == 0:
                exit("this error")


            if (avg > ((one + thresh) / 2)):
                break
            energy_offset += 1


        # Find the sample corresp. to the first reliable bit "1"; this step 
        # is crucial to a proper and correct synchronization w/ the xmitter.
        offset =  energy_offset
        if offset < 0:
            print '*** ERROR: Could not detect any ones (so no preamble). ***'
            print '\tIncrease volume / turn on mic?'
            print '\tOr is there some other synchronization bug? ***'
            sys.exit(1)

        '''
        Then, starting from the demod_samples[offset], find the sample index where
        the cross-correlation between the signal samples and the preamble 
        samples is the highest. 
        '''        
        original_preamble_bits = [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        preambleSamples = np.array([])
        for x in original_preamble_bits:
            toAdd = one
            if x == 0:
                toAdd = 0
            for i in xrange(self.spb):
                preambleSamples = np.append(preambleSamples, toAdd)


        energy_samples = demod_samples[energy_offset:energy_offset + 3 * len(preambleSamples)]

        max_idx = 0
        max_val = 0
        i = 0
        while (True):
            
            potential_sample = energy_samples[i:i+len(preambleSamples)]

            corr_val = np.dot(preambleSamples, potential_sample)/np.linalg.norm(potential_sample)

            #print corr_val - np.dot(potential_sample, preambleSamples)
            #print



            if corr_val > max_val:
                
                max_val = corr_val
                max_idx = i

            i += 1
            if i >= len(energy_samples) - len(preambleSamples):
                break
        pre_offset = max_idx

        '''
        [pre_offset] is the additional amount of offset starting from [offset],
        (not a absolute index reference by [0]). 
        Note that the final return value is [offset + pre_offset]
        '''
        return offset + pre_offset
        

    def kmeans_clustering(self, samples, numClusters):

        clusterInd = random.sample(range(len(samples)), numClusters)
        centroids = [samples[i] for i in clusterInd]
        clusters = [None] * len(samples)
        while(True):

            stopRun = True

            #Assign points to centroids
            for i in range(len(samples)):
                currSamp = samples[i]
                centroidDists = [abs(centroids[j] - currSamp) for j in range(len(centroids))]
                closestCentroid = min(enumerate(centroidDists), key=itemgetter(1))[0]
                if (clusters[i] != closestCentroid):
                    stopRun = False
                clusters[i] = closestCentroid
            #Recompute custers
            for i in range(len(centroids)):
                totalVal = 0
                totalNum = 0
                for j in range(len(clusters)):
                    if (clusters[j] == i):
                        totalVal += samples[j]
                        totalNum += 1
                totalVal = totalVal / (1.0 * totalNum)
                centroids[i] = totalVal
            if (stopRun):
                return clusters, centroids


    

    def demap_and_check(self, demod_samples, barker_start):
        '''
        Demap the demod_samples (starting from [preamble_start]) into bits.
        1. Calculate the average values of midpoints of each [spb] samples
           and match it with the known preamble bit values.
        2. Use the average values and bit val[None] * len(samples) of the preamble samples from (1)
           to calculate the new [thresh], [one], [zero]
        3. Demap the average values from (1) with the new three values from (2)
        4. Check whether the first [preamble_length] bits of (3) are equal to
           the preamble. If it is proceed, if not print an error message and 
           terminate the program. 
        Output is the array of data_bits (bits without preamble)
        '''
        preambleBits = [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]

        data_bits = []
        offset = barker_start
        preambleOneVolts = []
        preambleZeroVolts = []

        preambleGuessese = []

        for i in range(len(preambleBits)):
            currSamples = demod_samples[offset: offset + self.spb]
            middleIndex = self.spb / 2
            samplesToAvg = currSamples[middleIndex - (self.spb / 4): middleIndex + (self.spb / 4)]
            samplesToAvg = np.array(samplesToAvg)

            avg = np.average(samplesToAvg)
            if (preambleBits[i] == 1):
                preambleOneVolts.append(avg)
            else:
                preambleZeroVolts.append(avg)
            offset += self.spb
            
        preambleOneVolts = np.array(preambleOneVolts)
        preambleZeroVolts = np.array(preambleZeroVolts)

        one = np.average(preambleOneVolts)
        zero = np.average(preambleZeroVolts)

        thresh = (one + zero) / 2

        offset = barker_start

        while (True):

            currSamples = demod_samples[offset: offset + self.spb]
            middleIndex = self.spb / 2

            samplesToAvg = currSamples[middleIndex - (self.spb / 4): middleIndex + (self.spb / 4)]
            samplesToAvg = np.array(samplesToAvg)

            if len(samplesToAvg) == 0:
                break
            avg = np.average(samplesToAvg)
            if (avg > thresh):
                data_bits.append(1)
            else:
                data_bits.append(0)
            if (offset + self.spb >= len(demod_samples)):
                break

            offset += self.spb

        if (data_bits[0] != preambleBits[0] or data_bits[1] != preambleBits[1] or data_bits[2] != preambleBits[2]):
            exit("PREAMBLE MISMATCH")

        return data_bits[len(preambleBits):]

        # Fill in your implementation

    def demodulate(self, samples):
        ''' 
        Perform quadrature modulation.
        Return the demodulated samples.
        '''
        expval = (0 + 1j) * 2 * math.pi * self.fc / self.samplerate
        exp_samples = [np.exp(expval * n) * samples[n] for n in xrange(len(samples))]

        # sin_demodulated_samples = [(samples[i] * math.sin(2 * math.pi * self.fc/self.samplerate * i)) for i in xrange(len(samples))]
        # cut_off = math.pi * self.fc / self.samplerate
        # sinOutput = common.lpfilter(sin_demodulated_samples, cut_off)

        # cos_demodulated_samples = [(samples[i] * math.cos(2 * math.pi * self.fc/self.samplerate * i)) for i in xrange(len(samples))]
        cut_off = math.pi * self.fc / self.samplerate
        output = common.lpfilter(exp_samples, cut_off)
        abs_output = [abs(x) for x in output]
        # w = (sinOutput ** 2) + (cosOutput ** 2)
        # w = np.sqrt(w)

        #p.show()
        return abs_output

    def decode(self, recd_bits):
        return cc.get_databits(recd_bits)
