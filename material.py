from abc import ABC, abstractmethod
import math

import vector
import util
import hittable

class Material(ABC):

    @abstractmethod
    def scatter(self, ray_in: vector.Ray, hit_record: hittable.HitRecord):
        pass

class Lambertian(Material):

    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray_in: vector.Ray, hit_record: hittable.HitRecord):
        scatter_direction = hit_record.normal + vector.random_unit_vector()
        scattered = vector.Ray(hit_record.position, scatter_direction, ray_in.time)
        return True, self.albedo, scattered


class Metal(Material):

    def __init__(self, color, fuzz):
        self.color = color
        self.fuzz = fuzz

    def scatter(self, ray_in: vector.Ray, hit_record: hittable.HitRecord):


        reflected = vector.reflect(vector.unit_vector(ray_in.direction), hit_record.normal)
        scattered = vector.Ray(hit_record.position, reflected + vector.random_in_unit_sphere().times(self.fuzz), ray_in.time)

        didscatter = (vector.dot(scattered.direction, hit_record.normal) > 0)

        return didscatter, self.color, scattered

class Dielectric(Material):

    def __init__(self, refractive_index):
        self.ref_idx = refractive_index

    def scatter(self, ray_in: vector.Ray, hit_record: hittable.HitRecord):
        attenuation = vector.Vec3(1.0, 1.0, 1.0)
        etai_over_etat = self.ref_idx

        if hit_record.front_face:
            etai_over_etat = 1.0 / self.ref_idx

        unit_direction = vector.unit_vector(ray_in.direction)

        cos_theta = min(vector.dot(-unit_direction, hit_record.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)

        if etai_over_etat * sin_theta > 1.0:
            reflected = vector.reflect(unit_direction, hit_record.normal)
            scattered = vector.Ray(hit_record.position, reflected, ray_in.time)
            return True, attenuation, scattered

        reflect_prob = vector.schlick(cos_theta, etai_over_etat)
        if util.random_double() < reflect_prob:
            reflected = vector.reflect(unit_direction, hit_record.normal)
            scattered = vector.Ray(hit_record.position, reflected, ray_in.time)
            return True, attenuation, scattered

        refracted = vector.refract(unit_direction, hit_record.normal, etai_over_etat)
        scattered = vector.Ray(hit_record.position, refracted, ray_in.time)
        return True, attenuation, scattered
