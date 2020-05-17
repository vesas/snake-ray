
import math
import random

PI = 3.1415926535897932385

INFINITY = math.inf

def degrees_to_radians(degrees):
    return degrees * PI / 180


def random_double():
    return random.random()

def random_double_range(min,max):
    return random.uniform(min,max)


def clamp(x,min,max):

    if x < min:
        return min

    if x > max:
        return max

    return x

 