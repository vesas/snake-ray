
import vector
import util
import math

class AABB:

    def __init__(self, min: vector.Vec3, max: vector.Vec3):

        self.min = min
        self.max = max

    def hit(self, ray: vector.Ray, t_min: float, t_max: float) -> bool:

        # X dim
        dir_inv = 1.0 / ray.direction.x
        t0 = min(   (self.min.x - ray.origin.x) * dir_inv,(self.max.x - ray.origin.x) * dir_inv)
        t1 = max(   (self.min.x - ray.origin.x) * dir_inv,(self.max.x - ray.origin.x) * dir_inv)

        t_min = max(t0, t_min)
        t_max = min(t1, t_max)

        if (t_max <= t_min):
            return False

        # Y dim
        dir_inv = 1.0 / ray.direction.y
        t0 = min(   (self.min.y - ray.origin.y) * dir_inv,(self.max.y - ray.origin.y) * dir_inv)
        t1 = max(   (self.min.y - ray.origin.y) * dir_inv,(self.max.y - ray.origin.y) * dir_inv)

        t_min = max(t0, t_min)
        t_max = min(t1, t_max)

        if (t_max <= t_min):
            return False

        # Z dim
        dir_inv = 1.0 / ray.direction.z
        t0 = min(   (self.min.z - ray.origin.z) * dir_inv,(self.max.z - ray.origin.z) * dir_inv)
        t1 = max(   (self.min.z - ray.origin.z) * dir_inv,(self.max.z - ray.origin.z) * dir_inv)

        t_min = max(t0, t_min)
        t_max = min(t1, t_max)

        if (t_max <= t_min):
            return False

        return True


def surrounding_box(box0: AABB, box1: AABB) -> AABB:

    small = vector.Vec3(min(box0.min.x, box1.min.x),
                        min(box0.min.y, box1.min.y),
                        min(box0.min.z, box1.min.z)
                        )

    big = vector.Vec3(max(box0.max.x, box1.max.x),
                        max(box0.max.y, box1.max.y),
                        max(box0.max.z, box1.max.z)
                        )

    return AABB(small,big)
