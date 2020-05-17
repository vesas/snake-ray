
import vector as v
import cProfile
import re
import hittable as h

p = v.vec3(0.0,0.0,0.0)
norm = v.vec3(0.0,1.0,0.0)

hit_rec = h.hit_record(p,norm,0.0)

sum = 0.0
for i in range(100):
    target = hit_rec.p + v.random_in_hemisphere(hit_rec.normal)
    sum = sum + target.x

print("avg x: " + str( sum / 100.0))



r = v.ray(v.vec3(0.0,0.0,0.0),v.vec3(1.0,1.0,1.0))

r2 = r.at(-0.5)

print("" + str(r))
print("" + str(r2))



