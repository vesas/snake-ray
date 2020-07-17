import math
from abc import ABC, abstractmethod

import vector

class HitRecord:

    def __init__(self, position: vector.Vec3, normal: vector.Vec3, t: float, material_value):

        self.position = position
        self.normal = normal
        self.t = t
        self.front_face = True
        self.material = material_value

    def set_face_normal(self, ray: vector.Ray, outward_normal: vector.Vec3):
        self.front_face = vector.dot(ray.direction, outward_normal) < 0

        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = -outward_normal


class Hittable(ABC):

    @abstractmethod
    def hit(self, ray: vector.Ray, t_min: float, t_max: float):
        pass


class HittableList(Hittable):

    def __init__(self):
        self.objects = []

    def add(self, o):
        self.objects.append(o)

    def hit(self, ray: vector.Ray, t_min: float, t_max: float):
        rec = HitRecord(None, None, None, None)
        hit_anything = False
        closest_so_far = t_max

        for o in self.objects:
            didhit, temp_rec = o.hit(ray, t_min, closest_so_far)
            if didhit:
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec

        return hit_anything, rec


class Sphere(Hittable):

    def __init__(self, center: vector.Vec3, radius: float, thematerial):

        self.center = center
        self.radius = radius
        self.m = thematerial

    def hit(self, ray: vector.Ray, t_min: float, t_max: float):

        oc = ray.origin - self.center
        a = ray.direction.length_squared()
        half_b = vector.dot(oc, ray.direction)
        c = oc.length_squared() - self.radius*self.radius
        discriminant = half_b*half_b - a*c

        if discriminant > 0:
            root = math.sqrt(discriminant)
            temp = (-half_b - root)/a
            if t_min < temp < t_max:
                hit_rec = HitRecord(None, None, None, None)
                hit_rec.t = temp
                hit_rec.position = ray.at(hit_rec.t)
                hit_rec.material = self.m
                outward_normal = (hit_rec.position - self.center).divide(self.radius)
                hit_rec.set_face_normal(ray, outward_normal)
                return True, hit_rec

            temp = (-half_b + root) / a
            if t_min < temp < t_max:
                hit_rec = HitRecord(None, None, None, None)
                hit_rec.t = temp
                hit_rec.position = ray.at(hit_rec.t)
                hit_rec.material = self.m
                outward_normal = (hit_rec.position - self.center).divide(self.radius)
                hit_rec.set_face_normal(ray, outward_normal)
                return True, hit_rec

        return False, None
