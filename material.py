from abc import ABC, abstractmethod

import vector as v
import util as u
import math

class Material(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def scatter(self,r_in,hit_rec):
        pass

class Lambertian(Material):

    def __init__(self,albedo):
        self.albedo = albedo
        
    def scatter(self,r_in,hit_rec):
        scatter_direction = hit_rec.normal + v.random_unit_vector()
        scattered = v.ray(hit_rec.p, scatter_direction)
        return True, self.albedo, scattered


class Metal(Material):
    
    def __init__(self,color,fuzz):
        self.color = color
        self.fuzz = fuzz

    def scatter(self,r_in,hit_rec):


        reflected = v.reflect(v.unit_vector(r_in.direction), hit_rec.normal)
        scattered = v.ray(hit_rec.p,reflected + v.random_in_unit_sphere().times( self.fuzz ))

        didscatter = (v.dot(scattered.direction, hit_rec.normal) > 0)
        
        return didscatter, self.color,scattered

class Dielectric(Material):

    def __init__(self,refractive_index):
        self.ref_idx = refractive_index

    def scatter(self,r_in,hit_rec):
        attenuation = v.vec3(1.0, 1.0, 1.0)
        etai_over_etat = self.ref_idx

        if hit_rec.front_face == True:
            etai_over_etat = 1.0 / self.ref_idx

        unit_direction = v.unit_vector(r_in.direction)
        
        cos_theta = min(v.dot(-unit_direction,hit_rec.normal),1.0)
        sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)

        if etai_over_etat * sin_theta > 1.0:
            reflected = v.reflect(unit_direction, hit_rec.normal)
            scattered = v.ray(hit_rec.p, reflected)
            return True, attenuation, scattered

        reflect_prob = v.schlick(cos_theta, etai_over_etat)
        if u.random_double() < reflect_prob:
            reflected = v.reflect(unit_direction, hit_rec.normal)
            scattered = v.ray(hit_rec.p, reflected)
            return True, attenuation, scattered

        refracted = v.refract(unit_direction, hit_rec.normal, etai_over_etat)
        scattered = v.ray(hit_rec.p, refracted)
        return True, attenuation, scattered
