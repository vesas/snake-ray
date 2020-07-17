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

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = util.random_double()

            center = vector.Vec3(a + 0.9*util.random_double(), 0.2, b + 0.9*util.random_double())

            if (center - vector.Vec3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    albedo = vector.random() * vector.random()
                    world.add(hittable.Sphere(center, 0.2, material.Lambertian(albedo)))

                elif choose_mat < 0.95:
                    # metal
                    albedo = vector.random_in_range(.5, 1)
                    fuzz = util.random_double_range(0, .5)

                    world.add(hittable.Sphere(center, 0.2, material.Metal(albedo, fuzz)))
                else:
                    # glass
                    world.add(hittable.Sphere(center, 0.2, material.Dielectric(1.5)))

    world.add(hittable.Sphere(vector.Vec3(0, 1, 0), 1.0, material.Dielectric(1.5)))

    world.add(hittable.Sphere(vector.Vec3(-4, 1, 0), 1.0, material.Lambertian(vector.Vec3(.4, .2, .1))))

    world.add(hittable.Sphere(vector.Vec3(4, 1, 0), 1.0, material.Metal(vector.Vec3(.7, .6, .5), 0.0)))

    return world

def test_scene(seed):

    random.seed(seed)

    world = hittable.HittableList()

    R = math.cos(util.PI/4)

    world.add(hittable.Sphere(vector.Vec3(-R, 0, -1), R, material.Lambertian(vector.Vec3(0, 0, 1))))
    world.add(hittable.Sphere(vector.Vec3(R, 0, -1), R, material.Lambertian(vector.Vec3(1, 0, 0))))

    world.add(hittable.Sphere(vector.Vec3(0, 0, -1), 0.5, material.Lambertian(vector.Vec3(0.1, 0.2, 0.5))))
    world.add(hittable.Sphere(vector.Vec3(0, -100.5, -1), 100, material.Lambertian(vector.Vec3(0.8, 0.8, 0.0))))

    world.add(hittable.Sphere(vector.Vec3(1, 0, -1), 0.5, material.Metal(vector.Vec3(.8, .6, .2), 0.0)))
    world.add(hittable.Sphere(vector.Vec3(-1, 0, -1), 0.5, material.Dielectric(1.5)))
    world.add(hittable.Sphere(vector.Vec3(-1, 0, -1), -0.45, material.Dielectric(1.5)))
  

'''
Writes pixel color to the output file

'''
def write_color(pixel_color: vector.Vec3, samples_per_pixel: int):

    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z

    scale = 1.0 / samples_per_pixel

    r = math.sqrt(r * scale)
    g = math.sqrt(g * scale)
    b = math.sqrt(b * scale)

    print("" + str(int(256 * util.clamp(r, 0.0, 0.999))) + " " + str(int(256 * util.clamp(g, 0.0, 0.999))) + " " + str(int(256 * util.clamp(b, 0.0, 0.999))))

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


def main():
    
    arglen = len(sys.argv)

    instancevar = -1

    if arglen > 1:
        arg0 = sys.argv[0]
        arg1 = sys.argv[1]
        instancevar = arg1

    aspect_ratio = 16.0 / 9.0
    image_width = 384
    #image_width = 800
    image_height = int(image_width / aspect_ratio)
    samples_per_pixel = 10
    max_depth = 50

    lookfrom = vector.Vec3(13, 2, 3)
    lookat = vector.Vec3(0, 0, 0)
    dist_to_focus = 10.0
    aperture = 0.1

    vup = vector.Vec3(0, 1, 0)

    cam = camera.Camera(lookfrom, lookat, vup, 20, aspect_ratio, aperture, dist_to_focus)

    world = random_scene(-1)

    random.seed(instancevar)

    print("P3")
    print("" + str(image_width) + " " + str(image_height))
    print("255")

    for j in range(image_height-1, 0, -1):

        if instancevar == -1:
            sys.stderr.write("\rScanlines remaining: " + str(j) + "     ")

        for i in range(0, image_width, 1):

            pixel_color = vector.Vec3(0.0, 0.0, 0.0)

            for _ in range(samples_per_pixel):

                u1 = (i + util.random_double()) / (image_width-1)
                v1 = (j + util.random_double()) / (image_height-1)

                r = cam.get_ray(u1, v1)

                pixel_color = pixel_color + ray_color(r, world, max_depth)

            
            write_color(pixel_color, samples_per_pixel)


    sys.stderr.write("\nDone (instance: " + str(instancevar) + ")")
        

if __name__ == "__main__":
    # execute only if run as a script
    main()
