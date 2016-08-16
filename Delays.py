
'''
Created on Jun 8, 2016
@author: laurynas
'''
from numpy import concatenate,take,uint64,save, int64,zeros,where,argwhere,intersect1d,load,array,append,savetxt,in1d
import sys
from System import load_data
from numpy import uint8,ndarray
from itertools import product
import ttag
from ttag_delays import *
from Statistics import create_binary_string_from_laser_pulses as laser

def remake_coincidence_matrix(coincidence_matrix):
    channels = len(coincidence_matrix[0][:])
    width = channels/2
    height = len(coincidence_matrix[:][0])/2
    matrix = zeros((height,width))
    
    for i in range(height):
        for j in range(width):
            matrix[i][j] = coincidence_matrix[i][channels/2+j]
    return matrix


def check_correlations(aliceTtags,aliceChannels,bobTtags,bobChannels,resolution, A_B_timetags, A_B_channels,channels1,channels2,delays,coincidence_window_radius):
    # channels = transpose([tile(channels1, len(channels2)), repeat(channels2, len(channels1))])
    # for delay,ch1,ch2 in zip(delays,channels[:,0],channels[:,1]):
    #     if delay < 0:
    #         A_B_timetags[A_B_channels == ch2] += (abs(delay)).astype(uint64)
    #     else:
    #         A_B_timetags[A_B_channels == ch1] += delay.astype(uint64)
    #
    indexes_of_order = A_B_timetags.argsort(kind = "mergesort")
    A_B_channels = take(A_B_channels,indexes_of_order)
    A_B_timetags = take(A_B_timetags,indexes_of_order)

    buf_num = ttag.getfreebuffer() 
    buffer = ttag.TTBuffer(buf_num,create=True,datapoints = int(5e7))
    buffer.resolution = 78.125e-12 # 260e-12
    buffer.channels = max(A_B_channels)+1
    buffer.addarray(A_B_channels,A_B_timetags)

    
    buf_num = ttag.getfreebuffer()
    bufDelays = ttag.TTBuffer(buf_num,create=True,datapoints = int(5e7))
    bufDelays.resolution = resolution
    bufDelays.channels = max(A_B_channels)+1
    bufDelays.addarray(A_B_channels,A_B_timetags.astype(uint64))
     
    print delays

    with_delays = (bufDelays.coincidences((A_B_timetags[-1]-1)*bufDelays.resolution, coincidence_window_radius,delays*resolution))
    print with_delays
    remade = remake_coincidence_matrix(with_delays)
    
    print "__COINCIDENCES WITH DELAYS ->>\n",remade.astype(uint64)



    
def calculate_delays(aliceTtags,aliceChannels,bobTtags,bobChannels,
                    resolution= 78.125e-12,
                    coincidence_window_radius = 200e-12,
                    delay_max = 1e-6):
    
    channels1 = [0,1,2,3]
    channels2 = [4,5,6,7]
    
    A_B_timetags = concatenate([aliceTtags,bobTtags])
    A_B_channels = concatenate([aliceChannels,bobChannels])



    indexes_of_order = A_B_timetags.argsort(kind = "mergesort")
    A_B_channels = take(A_B_channels,indexes_of_order)
    A_B_timetags = take(A_B_timetags,indexes_of_order)

    buf_num = ttag.getfreebuffer()
    bufN = ttag.TTBuffer(buf_num,create=True,datapoints = int(5e7))
    bufN.resolution = resolution
    bufN.channels = max(A_B_channels)+1
    bufN.addarray(A_B_channels,A_B_timetags)

    coincidences_before = (bufN.coincidences((A_B_timetags[-1]-1)*bufN.resolution, coincidence_window_radius))
    remade = remake_coincidence_matrix(coincidences_before)
    print "__COINCIDENCES BEFORE-->>\n",remade.astype(uint64)

    channel_number  = len(channels1)*len(channels2)
    # delays = zeros((8,8))
    # k = 0
    # for i,j in product(channels1,channels2):  #zip(channels1, channels2)
    #     delays[i,j] = (getDelay(bufN,i,j,delaymax=delay_max,time=(A_B_timetags[-1]-1)*bufN.resolution))/bufN.resolution
    #     #print delays[i]
    #     #print i,j
    #     k+=1
    #
    # delays = array([0, delays[0,6]+delays[1,6], delays[0,6]+delays[2,6], delays[0,7]+delays[3,7], delays[0,4],   delays[0,6]+delays[1,6]+delays[1,5],  delays[0,6],  delays[0,7]])
    # print delays

    delays = getDelays(bufN,alice_channels,bob_channels,0.0,None,None,0.0000001,(A_B_timetags[-1]-1)*bufN.resolution)

    delays = concatenate((delays[0]/resolution,delays[1]/resolution))




    check_correlations(aliceTtags, aliceChannels, bobTtags, bobChannels, resolution, A_B_timetags, A_B_channels, channels1, channels2, delays, coincidence_window_radius)
    print("Saving delays to file.")
    save("./Delays/delays.npy",delays)
    
if (__name__ == '__main__'):
    alice_channels = [0,1,2,3]
    bob_channels =   [4,5,6,7]
    
    (aliceTtags,aliceChannels) = load_data("alice",alice_channels,100)
    (bobTtags,bobChannels) = load_data("bob",bob_channels,100)
    
    indexes_of_order = aliceTtags.argsort(kind = "mergesort")
    aliceChannels = take(aliceChannels,indexes_of_order)
    aliceTtags = take(aliceTtags,indexes_of_order)
    
    indexes_of_order = bobTtags.argsort(kind = "mergesort")
    bobChannels = take(bobChannels,indexes_of_order)
    bobTtags = take(bobTtags,indexes_of_order)
    
    aliceTtags = aliceTtags[:len(aliceTtags)]
    aliceChannels = aliceChannels[:len(aliceChannels)]
    
    bobTtags = bobTtags[:len(bobTtags)]
    bobChannels = bobChannels[:len(bobChannels)]
    
    calculate_delays(aliceTtags.astype(uint64), aliceChannels.astype(uint8), bobTtags.astype(uint64), bobChannels.astype(uint8),coincidence_window_radius = 200e-12)

