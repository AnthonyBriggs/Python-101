#!/usr/bin/python

import sys
import wave
import random
import struct
import datetime

from perlin import pnoise


SAMPLE_LEN = 44100 * 300 # 300 seconds of noise, 5 minutes
#SAMPLE_LEN = 44100 * 10 # 10 seconds of noise
COUNT = 44100
print(COUNT, SAMPLE_LEN)


def normalise(values):
    """Bring a sequence of noise back within parameters.
       Note that if the max/min are too far outside bounds,
       it'll make the noise very quiet.

       Doing it this way (rather than for each sample)
       makes the sound "warmer" and "more natural" ;)
    """
    max_value = max(values)
    min_value = min(values)
    factor = 32767.0 / max(max_value, abs(min_value))
    return (int(v * factor) for v in values)

def white_noise():
    """White noise - just a random value across the range."""
    return random.randint(-32767, 32767)

brown_val = 0
BROWN_FACTOR = 50
def brown_noise():
    """Brown, aka. Brownian Noise. Start at zero and move randomly up and down.
    I've arbitrarily set the maximum movement as 1/10th of white noise."""
    # TODO: try different values of BROWN_FACTOR
    #       ... just seems to make it noisier or quieter - no change in freq
    global brown_val
    if brown_val > 32767:
        brown_val = brown_val - abs(white_noise()) / BROWN_FACTOR
    elif brown_val < -32767:
        brown_val = brown_val + abs(white_noise()) / BROWN_FACTOR
    else:
        brown_val = brown_val + white_noise() / BROWN_FACTOR
    return int(brown_val)

curr_tick = 0
curr_noise = [white_noise() for i in range(5)]
octave_lookup = [0,1,0,2,0,1,0, 3, 0,1,0,2,0,1,0, 4, 0,1,0,2,0,1,0, 3, 0,1,0,2,0,1,0]
def pink_noise():
    """
    pink noise can be generated (sort of) by adding
    together different "octaves" of noise like this:
    0    x x x x x x x x x x x x x x x x
    1     x   x   x   x   x   x   x   x
    2       x       x       x       x
    3           x               x
    4                   x

    Octave 4 changes it's contribution every 31 samples, whereas
    octave 0 changes every other one.

    Each sample, we rerandomise one of the curr_noise samples based on the
    lookup, then add them all up to get our final value.
    """
    global curr_tick
    octave = octave_lookup[curr_tick]
    curr_noise[octave] = int(white_noise() / (5-octave))
    curr_tick += 1
    if curr_tick >= len(octave_lookup):
        curr_tick = 0
    return sum(curr_noise)

def pink_brown():
    """Just add pink + brown noise together"""
    return pink_noise() + brown_noise()


### WARNING! Perlin noise repeats, so is incredibly irritating!
perlin_x_index = 0
#perlin_x_factor = 0.001    # low freq rumbling
#perlin_x_factor = 0.01    # airplane
#perlin_x_factor = 0.1    # irritating techno
perlin_x_factor = 1.0    # hummingbird on crack

perlin_y = 0.0
perlin_z = 0.0
def perlin_init():
    global perlin_x_index, perlin_y, perlin_z
    perlin_y = random.random() * 10.0
    perlin_z = random.random() * 10.0
    perlin_x_index = 0

def perlin_noise():
    global perlin_x_index, perlin_x_factor, perlin_y, perlin_z
    perlin_x_index += 1
    # This resets the noise every 100 samples or so
    # which makes it slightly easier to listen to,
    # but it's effectively turning the sample into white noise
    #if random.random() > 0.99:
    #    perlin_init()
    #    #perlin_y += perlin_x_factor
    #    #perlin_z += perlin_x_factor
    return int(pnoise(perlin_x_index * perlin_x_factor, perlin_y, perlin_z) * 32767)


noises = {
    '--white': white_noise,
    '--brown': brown_noise,
    '--pink': pink_noise,
    '--pinkbrown': pink_brown,
    '--perlin': perlin_noise,
}

noise_funcs = [n for n in list(noises.keys()) if n in sys.argv]
if not noise_funcs:
    print("Need to specify a noise function!")
    print("  eg. %s brown_noise.wav --brown" % sys.argv[0])
    print("Possible noise generation arguments are:")
    for arg, function in list(noises.items()):
        print("   ", arg)
    sys.exit(1)
else:
    noise_func = noises[noise_funcs[0]]
    if noise_func == perlin_noise:
        perlin_init()

noise_output = wave.open(sys.argv[1].replace('--', '')+'.wav', 'w')
noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
values = []

for i in range(0, SAMPLE_LEN):
    value = noise_func()
    #packed_value = struct.pack('h', value)
    #values.append(packed_value)
    #values.append(packed_value)
    #print value,

    values.append(value)
    values.append(value)
    if i % COUNT == 0:
        #print ".",
        print(value, end=' ')
        sys.stdout.flush()

output_values = (struct.pack('h', v) for v in normalise(values))
value_str = b''.join(output_values)
noise_output.writeframes(value_str)
noise_output.close()

