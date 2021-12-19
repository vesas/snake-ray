import math
from abc import ABC, abstractmethod

import types
import aabb
import util
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

    @abstractmethod
    def bounding_box(self, time0: float, time1: float):
        pass

class HittableList(Hittable):

    def __init__(self):
        self.objects = []

    def bounding_box(self, time0: float, time1: float):

        if len(self.objects) == 0: 
            return False,None

        first_box = True

        temp_box = aabb.AABB()

        for obj in self.objects:

            ret, temp_box = obj.bounding_box(time0, time1)
            if not ret:
                return False, None

            if first_box:
                output_box = temp_box
            else:
                ret, output_box = aabb.surrounding_box(output_box, temp_box)

            first_box = False

        return True, output_box

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


def box_x_compare(a: Hittable):
    return box_compare(a,0)

def box_y_compare(a: Hittable):
    return box_compare(a,1)

def box_z_compare(a: Hittable):
    return box_compare(a,2)

def box_compare(a: Hittable, axis: int):

    a_true, box_a = a.bounding_box(0,0)

    if not a_true:
        print("ERROR, no box in bvh_node __init__")

    if axis == 0:
        return box_a.min.x
    if axis == 1:
        return box_a.min.y
    if axis == 2:
        return box_a.min.z
    

class bvh_node(Hittable):

    def __init__(self, hittable_list, time0: float, time1: float):

        objects = hittable_list
        axis = util.random_int(0,2)

        if axis == 0:
            comparator = box_x_compare
        if axis == 1:
            comparator = box_y_compare
        if axis == 2:
            comparator = box_z_compare
        
        start = 0
        end = len(objects)
        object_span = end - start

        if object_span == 1:
            self.left = self.right = objects[start]
        elif object_span == 2:
            if comparator(objects[start]) < comparator(objects[start+1]):
                self.left = objects[start]
                self.right = objects[start+1]
            else:
                self.left = objects[start+1]
                self.right = objects[start]
        else:

            objs = objects[start: end]
            objs.sort(key=comparator)

            mid = start + object_span//2
            self.left = bvh_node(objs[start: mid], time0, time1)
            self.right = bvh_node(objs[mid: end], time0, time1)

        pass

    def bounding_box(self, time0: float, time1: float):

        return True, self.bounding_box

    def hit(self, ray: vector.Ray, t_min: float, t_max: float):

        hit_left, left_hit_record = self.left.hit(ray, t_min, t_max)
        hit_right, right_hit_record = self.right.hit(ray, t_min, t_max)

        if hit_left:
            return hit_left, left_hit_record
        if hit_right:
            return hit_right, right_hit_record
        
        rec = HitRecord(None, None, None, None)
        return False, rec


class Sphere(Hittable):

    def __init__(self, center: vector.Vec3, radius: float, thematerial):

        self.center = center
        self.radius = radius
        self.m = thematerial

    def bounding_box(self, time0: float, time1: float):

        output_box = aabb.AABB(self.center - vector.Vec3(self.radius, self.radius, self.radius),
                    self.center + vector.Vec3(self.radius, self.radius, self.radius))
        return True, output_box

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


class MovingSphere(Hittable):

    def __init__(self, center0: vector.Vec3, center1: vector.Vec3, time0: float, time1: float, radius: float, thematerial):

        self.center0 = center0
        self.center1 = center1
        self.radius = radius
        self.m = thematerial
        self.time0 = time0
        self.time1 = time1

    def bounding_box(self, time0: float, time1: float):

        center0 = self.center(time0)
        center1 = self.center(time1)

        output_box0 = aabb.AABB(center0 - vector.Vec3(self.radius, self.radius, self.radius),
                    center0 + vector.Vec3(self.radius, self.radius, self.radius))

        output_box1 = aabb.AABB(center1 - vector.Vec3(self.radius, self.radius, self.radius),
                    center1 + vector.Vec3(self.radius, self.radius, self.radius))

        output_box = aabb.surrounding_box(output_box0, output_box1)
        return True, output_box

    def center(self, time: float):
        diff = (self.center1 - self.center0)
        diff = diff.times( ((time - self.time0) / (self.time1 - self.time0)) )
        return self.center0 + diff

    def hit(self, ray: vector.Ray, t_min: float, t_max: float):

        oc = ray.origin - self.center(ray.time)
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
                outward_normal = (hit_rec.position - self.center(ray.time)).divide(self.radius)
                hit_rec.set_face_normal(ray, outward_normal)
                return True, hit_rec

            temp = (-half_b + root) / a
            if t_min < temp < t_max:
                hit_rec = HitRecord(None, None, None, None)
                hit_rec.t = temp
                hit_rec.position = ray.at(hit_rec.t)
                hit_rec.material = self.m
                outward_normal = (hit_rec.position - self.center(ray.time)).divide(self.radius)
                hit_rec.set_face_normal(ray, outward_normal)
                return True, hit_rec

        return False, None
