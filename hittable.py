
import math
import vector as v

from abc import ABC, abstractmethod


class hit_record:

    def __init__(self,p, normal, t, mat):

        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = True
        self.m = mat

    def set_face_normal(self,ray, outward_normal):
        self.front_face = v.dot(ray.direction, outward_normal) < 0

        if self.front_face==True:
            self.normal = outward_normal
        else:
            self.normal = -outward_normal
        

class hittable(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def hit(self,r,t_min,t_max):
        pass


class hittable_list(hittable):

    def __init__(self):
        self.objects = []

    def add(self,o):
        self.objects.append(o)

    def hit(self,r,t_min,t_max):
        rec = hit_record(None,None,None,None)
        hit_anything = False
        closest_so_far = t_max

        for o in self.objects:
            didhit, temp_rec = o.hit(r, t_min, closest_so_far)
            if didhit == True:
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec

        return hit_anything,rec
        

class sphere(hittable):

    def __init__(self, center, radius, thematerial):
        
        self.center = center
        self.radius = radius
        self.m = thematerial

    def hit(self,r,t_min,t_max):
        
        oc = r.origin - self.center
        a = r.direction.length_squared()
        half_b = v.dot(oc, r.direction)
        c = oc.length_squared() - self.radius*self.radius
        discriminant = half_b*half_b - a*c

        if (discriminant > 0):
            root = math.sqrt(discriminant)
            temp = (-half_b - root)/a
            if (temp < t_max and temp > t_min):
                hit_rec = hit_record(None,None,None,None)
                hit_rec.t = temp
                hit_rec.p = r.at(hit_rec.t)
                hit_rec.m = self.m
                outward_normal = (hit_rec.p - self.center).divide(self.radius)
                hit_rec.set_face_normal(r, outward_normal)
                return True, hit_rec
        
            temp = (-half_b + root) / a
            if (temp < t_max and temp > t_min):
                hit_rec = hit_record(None,None,None,None)
                hit_rec.t = temp
                hit_rec.p = r.at(hit_rec.t)
                hit_rec.m = self.m
                outward_normal = (hit_rec.p - self.center).divide(self.radius)
                hit_rec.set_face_normal(r, outward_normal)
                return True, hit_rec
        
        return False, None


    