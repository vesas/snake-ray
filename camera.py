
import vector as v
import util as u
import math

class camera:

    def __init__(self, lookfrom, lookat, vup, vfov, aspect_ratio, aperture, focus_dist):

        self.origin = lookfrom
        self.lens_radius = aperture / 2

        theta = u.degrees_to_radians(vfov)

        half_height = math.tan(theta/2)
        half_width = aspect_ratio * half_height

        self.w1 = v.unit_vector(lookfrom - lookat)
        self.u1 = v.unit_vector(v.cross(vup, self.w1))
        self.v1 = v.cross(self.w1, self.u1)

        self.lower_left_corner = self.origin - self.u1.times( half_width * focus_dist ) - self.v1.times( half_height * focus_dist ) - self.w1.times(focus_dist)

        self.horizontal = self.u1.times( half_width * 2 * focus_dist )
        self.vertical = self.v1.times( half_height * 2 * focus_dist )

        self.vfov = vfov
        self.aspect_ratio = aspect_ratio


    def get_ray(self,s,t):

        rd = v.random_in_unit_disk().times(self.lens_radius)
        offset = self.u1.times(rd.x) + self.v1.times(rd.y)

        ret = v.ray(self.origin + offset, self.lower_left_corner + self.horizontal.times(s) + self.vertical.times(t) - self.origin - offset)
        return ret
