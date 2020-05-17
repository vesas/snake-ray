import sys

import vector as v
import hittable as g
import material as m
import util as u
import math as math
import camera
import random

def random_scene(seed):

    random.seed(seed)

    world = g.hittable_list()

    world.add(g.sphere(v.vec3(0,-1000,0),1000,m.Lambertian(v.vec3(0.5, 0.5, 0.5))))

    i = 1
    for a in range(-11, 11,1):
        for b in range(-11, 11,1):
            choose_mat = u.random_double()

            center = v.vec3(a + 0.9*u.random_double(), 0.2, b + 0.9*u.random_double())

            if (center - v.vec3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    albedo = v.random() * v.random()
                    world.add(g.sphere(center,0.2,m.Lambertian(albedo)))

                elif (choose_mat < 0.95):
                    # metal
                    albedo = v.random_in_range(.5, 1)
                    fuzz = u.random_double_range(0, .5)

                    world.add(g.sphere(center,0.2,m.Metal(albedo,fuzz)))
                else:
                    # glass
                    world.add(g.sphere(center,0.2,m.Dielectric(1.5)))

    world.add(g.sphere(v.vec3(0, 1, 0),1.0,m.Dielectric(1.5)))

    world.add(g.sphere(v.vec3(-4, 1, 0),1.0,m.Lambertian(v.vec3(.4, .2, .1))))

    world.add(g.sphere(v.vec3(4, 1, 0),1.0,m.Metal(v.vec3(.7, .6, .5),0.0)))
    
    return world

'''
def hit_sphere(center,radius,ray):
    oc = ray.origin - center
    a = ray.direction.length_squared()
    halfb = v.dot(oc,r.direction)
    c = oc.length_squared() - (radius*radius)
    discriminant = halfb*halfb - (a*c)

    if discriminant < 0:
        return -1.0
    else:
        return (-halfb - np.sqrt(discriminant) ) / (a)
'''

'''
vec3 pixel_color
'''
def write_color(pixel_color: v.vec3, samples_per_pixel):

    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z

    scale = 1.0 / samples_per_pixel

    r = math.sqrt(r * scale)
    g = math.sqrt(g * scale)
    b = math.sqrt(b * scale)

    print("" + str(int(256 * u.clamp(r,0.0,0.999))) + " " + str(int(256 * u.clamp(g,0.0,0.999))) + " " + str(int(256 * u.clamp(b,0.0,0.999))))

def ray_color(r: v.ray, world: g.hittable, depth):

    if depth <= 0:
        return v.vec3(0.0,0.0,0.0)

    did_hit, hit_rec = world.hit(r,0.001,u.INFINITY)

    if did_hit == True:

        tempmaterial = hit_rec.m

        didscatter, albedo, scattered = tempmaterial.scatter(r,hit_rec)

        if didscatter == True:

            return albedo * ray_color(scattered,world,depth-1)

        return v.vec3(0,0,0)

    unit_dir = v.unit_vector(r.direction)
    t = (unit_dir.y + 1.0)*0.5
    return v.vec3(1.0, 1.0, 1.0).times(1.0-t) + v.vec3(0.5, 0.7, 1.0).times(t)
    


'''
    t = hit_sphere(v.vec3(0,0,-1), 0.5, r)
    if (t > 0.0):
        N = v.unit_vector(r.at(t) - v.vec3(0,0,-1))
        return v.vec3(N.x+1, N.y+1, N.z+1).times(0.5)

    
    return v.vec3(1.0, 1.0, 1.0).times(1.0-t) + v.vec3(0.5, 0.7, 1.0).times(t)
'''

arglen = len(sys.argv)

instancevar = -1

if arglen > 1:
    arg0 = sys.argv[0]
    arg1 = sys.argv[1]
    instancevar = arg1



#print("arg0: " + str(arg0))
#print("arg1: " + str(arg1))

aspect_ratio = 16.0 / 9.0
image_width = 384
#image_width = 800
image_height = int(image_width / aspect_ratio)
samples_per_pixel = 10
max_depth = 50

lookfrom = v.vec3(13,2,3)
lookat = v.vec3(0,0,0)
dist_to_focus = 10.0
aperture = 0.1

vup = v.vec3(0,1,0)



cam = camera.camera(lookfrom, lookat, vup, 20, aspect_ratio, aperture, dist_to_focus)

R = math.cos(u.PI/4)

world = random_scene(-1)

random.seed(instancevar)

'''
world = g.hittable_list()

world.add(g.sphere(v.vec3(-R,0,-1),R,m.Lambertian(v.vec3(0, 0, 1))))
world.add(g.sphere(v.vec3(R,0,-1),R,m.Lambertian(v.vec3(1,0,0))))
'''

'''
world.add(g.sphere(v.vec3(0,0,-1),0.5,m.Lambertian(v.vec3(0.1, 0.2, 0.5))))
world.add(g.sphere(v.vec3(0,-100.5,-1),100,m.Lambertian(v.vec3(0.8,0.8,0.0))))

world.add(g.sphere(v.vec3(1,0,-1),0.5,m.Metal(v.vec3(.8,.6,.2),0.0)))
world.add(g.sphere(v.vec3(-1,0,-1),0.5,m.Dielectric(1.5)))
world.add(g.sphere(v.vec3(-1,0,-1),-0.45,m.Dielectric(1.5)))
'''


print("P3")
print("" + str(image_width) + " " + str(image_height))
print("255")

for j in range(image_height-1,0,-1):

    if instancevar == -1:
        sys.stderr.write("\rScanlines remaining: " + str(j) + "     ")

    for i in range(0,image_width,1):

        pixel_color = v.vec3(0.0,0.0,0.0)

        for s in range(samples_per_pixel):

            u1 = (i + u.random_double()) / (image_width-1)
            v1 = (j + u.random_double()) / (image_height-1)

            r = cam.get_ray(u1,v1)

            pixel_color = pixel_color + ray_color(r,world,max_depth)

        
        write_color(pixel_color,samples_per_pixel)


sys.stderr.write("\nDone " + str(instancevar) )
        
