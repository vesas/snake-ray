
import math
import random

PI = 3.1415926535897932385

INFINITY = math.inf

def degrees_to_radians(degrees):
    return degrees * PI / 180


def random_double():
    return random.random()

def random_double_range(min: float, max: float):
    return random.uniform(min, max)


def clamp(x: float, min_value: float, max_value: float):

    if x < min_value:
        return min_value

    if x > max_value:
        return max_value

    return x

 