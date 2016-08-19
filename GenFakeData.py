
import numpy.random as rnd
from numpy import *

resolution = 78.125e-12

# Data rate (pairs per second)

r = 1000000

times = rnd.rand(r)
indexes = times.sort(kind='mergesort')
times = times[indexes]
channels = rnd.randint(0,4,r)

alice_channels = channels
alice_ttags = times[0]/resolution

bob_channels = channels + 4
bob_ttags = alice_ttags


alice_retained_indices = rnd.choice(arange(len(alice_ttags)), len(alice_ttags)/2, replace = False)
alice_retained_indices = sort(alice_retained_indices)
bob_retained_indices = rnd.choice(arange(len(bob_ttags)), len(bob_ttags)/2, replace = False)
bob_retained_indices = sort(bob_retained_indices)

alice_ttags = alice_ttags[alice_retained_indices]
alice_channels = alice_channels[alice_retained_indices]

bob_ttags = bob_ttags[bob_retained_indices]
bob_channels = bob_channels[bob_retained_indices]



bob_ttag_errors = rnd.choice([-1,0,1],len(bob_ttags),p=[0.15,0.7,0.15])

bob_ttags += bob_ttag_errors

print bob_ttags


save('./DarpaQKD/aliceFakeChannels.npy',alice_channels)
save('./DarpaQKD/aliceFakeTtags.npy',alice_ttags)
save('./DarpaQKD/bobFakeChannels.npy',bob_channels)
save('./DarpaQKD/bobFakeTtags.npy',bob_ttags)


save('./Delays/delays.npy',[0,0,0,0,0,0,0,0])
