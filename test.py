
import vector
import cProfile
import re
import hittable

p = vector.Vec3(0.0,0.0,0.0)
norm = vector.Vec3(0.0,1.0,0.0)

hit_rec = hittable.HitRecord(p,norm,0.0, None)

sum = 0.0
for i in range(100):
    target = hit_rec.position + vector.random_in_hemisphere(hit_rec.normal)
    sum = sum + target.x

print("avg x: " + str( sum / 100.0))



r = vector.Ray(vector.Vec3(0.0,0.0,0.0),vector.Vec3(1.0,1.0,1.0))

r2 = r.at(-0.5)

print("" + str(r))
print("" + str(r2))



