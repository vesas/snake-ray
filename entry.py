import sys

import vector
import hittable
import material
import util
import math
import camera
import random

def random_scene(seed):

    random.seed(seed)

    world = hittable.HittableList()

    world.add(hittable.Sphere(vector.Vec3(0, -1000, 0), 1000, material.Lambertian(vector.Vec3(0.5, 0.5, 0.5))))

    hitList = []
    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = util.random_double()

            center = vector.Vec3(a + 0.9*util.random_double(), 0.2, b + 0.9*util.random_double())

            if (center - vector.Vec3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    albedo = vector.random() * vector.random()
                    # world.add(hittable.Sphere(center, 0.2, material.Lambertian(albedo)))

                    center2 = center + vector.Vec3(0, util.random_double_range(0,.5), 0)
                    hitList.append(hittable.MovingSphere(center, center2, 0.0, 1.0, 0.2, material.Lambertian(albedo)))

                elif choose_mat < 0.95:
                    # metal
                    albedo = vector.random_in_range(.5, 1)
                    fuzz = util.random_double_range(0, .5)

                    hitList.append(hittable.Sphere(center, 0.2, material.Metal(albedo, fuzz)))
                else:
                    # glass
                    hitList.append(hittable.Sphere(center, 0.2, material.Dielectric(1.5)))

    world.add(hittable.bvh_node(hitList, 0,1, 0, 1))
    world.add(hittable.Sphere(vector.Vec3(0, 1, 0), 1.0, material.Dielectric(1.5)))

    world.add(hittable.Sphere(vector.Vec3(-4, 1, 0), 1.0, material.Lambertian(vector.Vec3(.4, .2, .1))))

    world.add(hittable.Sphere(vector.Vec3(4, 1, 0), 1.0, material.Metal(vector.Vec3(.7, .6, .5), 0.0)))

    return world

def test_scene(seed):

    random.seed(seed)

    world = hittable.HittableList()

    R = math.cos(util.PI/4)

    hit_list = []

    world.add(hittable.Sphere(vector.Vec3(0, -1000, 0), 1000, material.Lambertian(vector.Vec3(0.6, 0.6, 0.6))))

    for _ in range(200):
        ranx = util.random_double_range(-10,10)
        ranz = util.random_double_range(-10,10)

        sp1 = hittable.Sphere(vector.Vec3(ranx, 0.3, ranz), 0.3,  material.Lambertian(vector.Vec3(.4, .2, .1)))
        hit_list.append(sp1)
    
    # world.add(hittable.Sphere(vector.Vec3(1, 0, -1), 0.5, material.Metal(vector.Vec3(.8, .6, .2), 0.0)))
    # 

    bvh = hittable.bvh_node(hit_list,0,1)
    world.add(bvh)

    return world

def test_scene2(seed):

    random.seed(seed)

    world = hittable.HittableList()

    R = math.cos(util.PI/4)

    hit_list = []

    world.add(hittable.Sphere(vector.Vec3(0, -1000, 0), 1000, material.Lambertian(vector.Vec3(0.6, 0.6, 0.6))))
    
    sp1 = hittable.Sphere(vector.Vec3(-0.7, 0.5, 0), 0.5,  material.Lambertian(vector.Vec3(.4, .2, .81)))
    hit_list.append(sp1)
    sp2 = hittable.Sphere(vector.Vec3(0.0, 0.5, 0), 0.5,  material.Lambertian(vector.Vec3(.4, .2, .81)))
    hit_list.append(sp2)
    sp3 = hittable.Sphere(vector.Vec3(0.7, 0.5, 0), 0.5,  material.Lambertian(vector.Vec3(.4, .2, .81)))
    hit_list.append(sp3)
    
    # world.add(hittable.Sphere(vector.Vec3(1, 0, -1), 0.5, material.Metal(vector.Vec3(.8, .6, .2), 0.0)))
    # 

    bvh = hittable.bvh_node(hit_list,0,1)
    world.add(bvh)

    return world



'''
Writes pixel color to the output file

'''
def write_color(outfile, pixel_color: vector.Vec3, samples_per_pixel: int):

    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z

    scale = 1.0 / samples_per_pixel

    r = math.sqrt(r * scale)
    g = math.sqrt(g * scale)
    b = math.sqrt(b * scale)

    outfile.write("" + str(int(255.999 * util.clamp(r, 0.0, 0.999))) + " " + str(int(255.999 * util.clamp(g, 0.0, 0.999))) + " " + str(int(255.999 * util.clamp(b, 0.0, 0.999))))
    outfile.write("\n")

def ray_color(ray: vector.Ray, world: hittable.Hittable, depth):

    if depth <= 0:
        return vector.Vec3(0.0, 0.0, 0.0)

    did_hit, hit_rec = world.hit(ray, 0.001, util.INFINITY)

    if did_hit:

        tempmaterial = hit_rec.material

        didscatter, albedo, scattered = tempmaterial.scatter(ray, hit_rec)

        if didscatter:

            return albedo * ray_color(scattered, world, depth-1)

        return vector.Vec3(0, 0, 0)

    unit_dir = vector.unit_vector(ray.direction)
    t = (unit_dir.y + 1.0)*0.5
    return vector.Vec3(1.0, 1.0, 1.0).times(1.0-t) + vector.Vec3(0.5, 0.7, 1.0).times(t)


def entry(filename, instanceid):
    
    aspect_ratio = 16.0 / 9.0
    # image_width = 384
    image_width = 800
    image_height = int(image_width / aspect_ratio)
    samples_per_pixel = 60
    max_depth = 50

    lookfrom = vector.Vec3(0, 1.5, -8)
    lookat = vector.Vec3(0, 0.5, 0)
    dist_to_focus = 8.0
    aperture = 0.1

    vup = vector.Vec3(0, 1, 0)

    cam = camera.Camera(lookfrom, lookat, vup, 20, aspect_ratio, aperture, dist_to_focus,0.0, 1.0)

    world = test_scene2(-1)

    random.seed(instanceid)

    outfile = open(filename, mode='w', encoding='utf-8', buffering=1)

    outfile.write("P3\n")
    outfile.write("" + str(image_width) + " " + str(image_height) + "\n")
    outfile.write("255\n")
    
    for j in range(image_height-1, -1, -1):

        #print(sys.stdout.encoding,file=sys.stderr)

        if instanceid == 0:
            sys.stderr.write("\rScanlines remaining: " + str(j) + "     ")

        for i in range(0, image_width, 1):

            pixel_color = vector.Vec3(0.0, 0.0, 0.0)

            for _ in range(samples_per_pixel):

                u1 = (i + util.random_double()) / (image_width-1)
                v1 = (j + util.random_double()) / (image_height-1)

                r = cam.get_ray(u1, v1)

                pixel_color = pixel_color + ray_color(r, world, max_depth)

            
            write_color(outfile,pixel_color, samples_per_pixel)


    outfile.flush()
    outfile.close()

    sys.stderr.write("\nDone (instance: " + str(instanceid) + ")")
        

if __name__ == "__main__":
    # execute only if run as a script

    # for debugging
    entry("temp", 1)
