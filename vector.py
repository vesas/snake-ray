

import math
import util as u

class vec3:

    def __init__(self, e1=0.0, e2=0.0, e3=0.0):

        self.x = e1
        self.y = e2
        self.z = e3

    def __add__(self, other):
        ret = vec3(self.x, self.y, self.z)
        ret.x = self.x + other.x
        ret.y = self.y + other.y
        ret.z = self.z + other.z
        return ret

    def __sub__(self, other):
        ret = vec3(self.x, self.y, self.z)
        ret.x = self.x - other.x
        ret.y = self.y - other.y
        ret.z = self.z - other.z
        return ret

    def __mul__(self, other):
        return vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z)


    def divide(self, t):
        ret = vec3(self.x, self.y, self.z)
        ret.x = self.x / t
        ret.y = self.y / t
        ret.z = self.z / t
        return ret

    def times(self, t):
        ret = vec3(self.x, self.y, self.z)
        ret.x = self.x * t
        ret.y = self.y * t
        ret.z = self.z * t
        return ret

    def subtract(self, t):
        ret = vec3(self.x, self.y, self.z)
        ret.x = self.x - t
        ret.y = self.y - t
        ret.z = self.z - t
        return ret


    def length_squared(self):
        return self.x*self.x + self.y*self.y + self.z*self.z

    def length(self):
        return math.sqrt(self.length_squared())

    def __str__(self):
        return "vec3(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"


def random():
    return vec3(u.random_double(), u.random_double(), u.random_double())

def random_in_range(min_value, max_value):
    return vec3(u.random_double_range(min_value, max_value), 
                u.random_double_range(min_value, max_value), 
                u.random_double_range(min_value, max_value))

def random_in_unit_sphere():

    while True:
        p = random_in_range(-1, 1)

        if p.length_squared() >= 1:
            continue

        return p

def random_in_hemisphere(normal):
    in_unit_sphere = random_in_unit_sphere()
    if dot(in_unit_sphere, normal) > 0.0: # In the same hemisphere as the normal
        return in_unit_sphere
    else:
        return -in_unit_sphere

def random_in_unit_disk():
    while True:
        p = vec3(u.random_double_range(-1,1), u.random_double_range(-1,1), 0)
        if p.length_squared() >= 1:
            continue
        return p
        
def unit_vector(v: vec3):
    return v.divide(v.length())

def random_unit_vector():
    a = u.random_double_range(0.0, 2.0*u.PI)
    z = u.random_double_range(-1.0, 1.0)
    r = math.sqrt(1-z*z)
    return vec3(r*math.cos(a), r*math.sin(a), z)

def dot(u_vector: vec3, v_vector: vec3):
    return u_vector.x*v_vector.x + u_vector.y*v_vector.y + u_vector.z*v_vector.z

def cross(u_vector: vec3, v_vector: vec3):
    return vec3(u_vector.y*v_vector.z - u_vector.z*v_vector.y,
                u_vector.z*v_vector.x - u_vector.x*v_vector.z,
                u_vector.x*v_vector.y - u_vector.y*v_vector.x )

def reflect(v_vector: vec3, n_vector: vec3):
    return v_vector - n_vector.times(dot(v_vector, n_vector)*2.0)

def schlick(cosine, ref_idx):
    r0 = (1-ref_idx) / (1+ref_idx)
    r0 = r0 * r0
    return r0 + (1-r0) * math.pow((1- cosine),5)

def refract(uv_vector: vec3, n_vector: vec3, etai_over_etat):
    cos_theta = dot(-uv_vector, n_vector)
    r_out_parallel = (uv_vector + n_vector.times(cos_theta)).times(etai_over_etat)
    r_out_perp = n_vector.times( -math.sqrt(1.0 - r_out_parallel.length_squared()))
    return r_out_parallel + r_out_perp

class ray:

    def __init__(self, origin=None, direction=None):

        self.origin = origin
        self.direction = direction

    def at(self, t):
        return self.origin + (self.direction.times(t))

    def __str__(self):
        return "ray(origin=" + str(self.origin) + ",direction=" + str(self.direction) + ")"
