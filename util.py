
import math
import random

PI = 3.1415926535897932385

INFINITY = math.inf

def degrees_to_radians(degrees):
    return degrees * PI / 180


def random_double():
    return random.random()

def random_double_range(min_value: float, max_value: float):
    return random.uniform(min_value, max_value)

def random_int(min_value: int, max_value: int):
    return random.randint(min_value, max_value)

def clamp(x: float, min_value: float, max_value: float):

    if x < min_value:
        return min_value

    if x > max_value:
        return max_value

    return x
