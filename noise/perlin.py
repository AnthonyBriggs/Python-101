#!/usr/bin/python

"""
TODO: where'd I get this from?
"""

import math
import random

p = (
151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,
30,69,142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,
62,94,252,219,203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,
125,136,171,168,68,175,74,165,71,134,139,48,27,166,77,146,158,231,
83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,102,
143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,18,169,200,
196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,
250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,
58,17,182,189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,
221,153,101,155,167,43,172,9,129,22,39,253,19,98,108,110,79,113,
224,232,178,185,112,104,218,246,97,228,251,34,242,193,238,210,144,
12,191,179,162,241,81,51,145,235,249,14,239,107,49,192,214,31,181,
199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,138,236,
205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180,
151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,
30,69,142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,
62,94,252,219,203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,
125,136,171,168,68,175,74,165,71,134,139,48,27,166,77,146,158,231,
83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,102,
143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,18,169,200,
196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,
250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,
58,17,182,189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,
221,153,101,155,167,43,172,9,129,22,39,253,19,98,108,110,79,113,
224,232,178,185,112,104,218,246,97,228,251,34,242,193,238,210,144,
12,191,179,162,241,81,51,145,235,249,14,239,107,49,192,214,31,181,
199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,138,236,
205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180)
  
def lerp(t, a, b):
    return a + t * (b - a)
  
def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)
  
def grad(hash, x, y, z):
    h = hash & 15
    if h < 8:
        u = x
    else:
        u = y
    if h < 4:
        v = y
    elif h == 12 or h == 14:
        v = x
    else:
        v = z
    if h & 1 != 0:
        u = -u
    if h & 2 != 0:
        v = -v
    return u + v
  
def pnoise(x, y, z):
    global p
    X = int(math.floor(x)) & 255
    Y = int(math.floor(y)) & 255
    Z = int(math.floor(z)) & 255
    x -= math.floor(x)
    y -= math.floor(y)
    z -= math.floor(z)
    
    u = fade(x)
    v = fade(y)
    w = fade(z)
    
    A =  p[X] + Y
    AA = p[A] + Z
    AB = p[A + 1] + Z
    B =  p[X + 1] + Y
    BA = p[B] + Z
    BB = p[B + 1] + Z
    
    pAA = p[AA]
    pAB = p[AB]
    pBA = p[BA]
    pBB = p[BB]
    pAA1 = p[AA + 1]
    pBA1 = p[BA + 1]
    pAB1 = p[AB + 1]
    pBB1 = p[BB + 1]
    
    gradAA =  grad(pAA, x,   y,   z)
    gradBA =  grad(pBA, x-1, y,   z)
    gradAB =  grad(pAB, x,   y-1, z)
    gradBB =  grad(pBB, x-1, y-1, z)
    gradAA1 = grad(pAA1,x,   y,   z-1)
    gradBA1 = grad(pBA1,x-1, y,   z-1)
    gradAB1 = grad(pAB1,x,   y-1, z-1)
    gradBB1 = grad(pBB1,x-1, y-1, z-1)
    return lerp(w, 
    lerp(v, lerp(u, gradAA, gradBA), lerp(u, gradAB, gradBB)),
    lerp(v, lerp(u, gradAA1,gradBA1),lerp(u, gradAB1,gradBB1)))


def perlin_multifractal(x,y,z, octaves, lambda_, amplitude):
    """Multi fractal just means that we have more noise,
    at higher frequencies (aka. octaves), layered on top
    of the existing noise."""
    sum = 0
    for oct in range(octaves):
        #print oct, amplitude, lambda_
        amp = amplitude / (2 ** oct);
        lam = lambda_ / (2 ** oct);
        # todo - find a decent interpolation function?
        #add = interpolate(x/lam, y/lam, z/lam) * amp;
        add = pnoise(x/lam, y/lam, z/lam) * amp;
        if oct > 1:
            add *= sum;
        sum += add;
    return sum

def perlin_multi_common(x, y, z):
    return perlin_multifractal(x,y,z, 4, 1.0, 1.0)


def perlin_ridged(x, y, z):
    """Ridged means that instead of varying from -1..1, 
    the value varies from -1..1..-1"""
    value = pnoise(x, y, z)
    if value > 0:
        value = (-value) + 1
    else:
        value = value + 1
    return 2*value - 1


def perlin_ridged_multifractal(x,y,z, octaves, lambda_, amplitude):
    sum = 0
    # k is a scaling constant. NFI what it should be though...
    k = 0.1
    for oct in range(octaves):
        #print oct, amplitude, lambda_
        amp = amplitude / (2 ** oct);
        lam = lambda_ / (2 ** oct);
        #add = interpolate(x/lam, y/lam, z/lam) * amp;
        add = perlin_ridged(x/lam, y/lam, z/lam) * amp;
        if oct > 1:
            add *= k * sum;
        sum += add;
    return sum

def perlin_ridged_multi_common(x, y, z):
    return perlin_ridged_multifractal(x,y,z, 4, 1.0, 1.0)


def get_random_range(num_steps=100):
    startx = random.random(); endx = random.random()
    if endx < startx:
        startx, endx = endx, startx
    stepx = (endx - startx) / num_steps
    return startx, endx, stepx


def make_landscape(x_size, y_size, noise_func, startx, stepx, starty, stepy):
    """Display some perlin noise as an image in a window."""
    heights = []
    landscape = Image.new("RGB", (x_size, y_size))

    for x in range(x_size):
        for y in range(y_size):
            xnoise, ynoise = (startx + x*stepx, starty + y*stepy)
            # make noise 0..2.0 instead of -1..1 and mult up to 256 max
            height = 128 * (noise_func(xnoise, ynoise, 0.5) + 1.0)
            heights.append((height, height, height))
    print(len(heights),  "heights generated")

    landscape.putdata(heights)
    landscape.show()


if __name__ == '__main__':
    for z in range(10):
        for y in range(10):
            for x in range(10):
                print("%.02f" % pnoise(x/10.0, y/10.0, z/10.0), end=' ')
            print()
        print()
    
    # pnoise is deterministic
    for i in range(10):
        print(pnoise(0.1, 0.1, 0.1))

    import Image
    x_size = 200; y_size = 200

    #startx, endx, stepx = get_random_range()
    #starty, endy, stepy = get_random_range()
    startx, endx, stepx = (0.0, 5.0, 5.0/x_size)
    starty, endy, stepy = (0.0, 5.0, 5.0/y_size)

    make_landscape(x_size, y_size, pnoise, startx, stepx, starty, stepy)
    make_landscape(x_size, y_size, perlin_multi_common, startx, stepx, starty, stepy)
    make_landscape(x_size, y_size, perlin_ridged, startx, stepx, starty, stepy)
    make_landscape(x_size, y_size, perlin_ridged_multi_common, startx, stepx, starty, stepy)

