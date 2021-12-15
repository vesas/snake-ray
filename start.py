
from multiprocessing import Process
import os
import sys
import entry

def rendering_process(filename, count):
    temp_filename = filename + str(count)
    print("pid {} running process, name {}".format(os.getpid(), temp_filename ))

    entry.entry(temp_filename, count)


def combine_images(name, instancecount):

    with open(name + ".ppm", "w") as target_file:

        inputs = []

        for i in range(instancecount):
            fp = open(name + str(i), "r")
            inputs.append(fp)

            # just copy 3 first lines as is
            for j in range(3):
                line = fp.readline()
                if i == 0:
                    target_file.write(line)

        finished = False

        while not finished:
            r = 0
            g = 0
            b = 0
            for i in range(instancecount):
                fp = inputs[i]
                line = fp.readline()

                if not line:
                    finished = True
                    break

                rt, gt, bt = line.split(" ")
                r += int(rt)
                g += int(gt)
                b += int(bt)

            if finished:
                break

            target_file.write("{} {} {}\n".format(int(r/instancecount),int(g/instancecount),int(b/instancecount)))

        for i in range(instancecount):
            inputs[i].close()
            os.remove(name + str(i))



def main():

    arglen = len(sys.argv)

    instancevar = -1

    count = 1

    if arglen <= 1:
        print("usage: python start.py <output filename> <process_count>")
        sys.exit()

    arg1 = sys.argv[1]
    filename = arg1

    if arglen > 2:
        arg0 = sys.argv[0]
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        instancevar = arg2

    filename = arg1
    count = int(arg2)

    process_list = []

    print("starting")

    for i in range(count):
        p = Process(target=rendering_process, args=(filename, i))
        process_list.append(p)
        p.start()

    print("started all")

    # wait for all processes to finish
    for i in range(count):
        p = process_list[i]
        p.join()

    # combine_images
    combine_images(filename, count)

    print("finished all")

if __name__ == "__main__":
    # execute only if run as a script

    main()




