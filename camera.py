import math

import vector
import util

class Camera:

    def __init__(self, lookfrom: vector.Vec3, lookat: vector.Vec3, vup: vector.Vec3, vfov: float, aspect_ratio: float, aperture: float, focus_dist: float, time0: float, time1: float):

        self.origin = lookfrom
        self.lens_radius = aperture / 2

        theta = util.degrees_to_radians(vfov)

        half_height = math.tan(theta/2)
        half_width = aspect_ratio * half_height

        self.w1 = vector.unit_vector(lookfrom - lookat)
        self.u1 = vector.unit_vector(vector.cross(vup, self.w1))
        self.v1 = vector.cross(self.w1, self.u1)

        self.lower_left_corner = self.origin - self.u1.times(half_width * focus_dist) - self.v1.times(half_height * focus_dist) - self.w1.times(focus_dist)

        self.horizontal = self.u1.times(half_width * 2 * focus_dist)
        self.vertical = self.v1.times(half_height * 2 * focus_dist)

        self.vfov = vfov
        self.aspect_ratio = aspect_ratio

        # camera shutter open/close times
        self.time0 = time0
        self.time1 = time1


    def get_ray(self, s: float, t: float):

        rd = vector.random_in_unit_disk().times(self.lens_radius)
        offset = self.u1.times(rd.x) + self.v1.times(rd.y)

        ret = vector.Ray(self.origin + offset,
                    self.lower_left_corner + self.horizontal.times(s) + self.vertical.times(t) - self.origin - offset,
                    util.random_double_range(self.time0, self.time1))
        return ret
