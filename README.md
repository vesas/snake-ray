# Python implementation of Ray tracing in one weekend

Python implementation of Peter Shirley's excellent book Ray Tracing In One Weekend. https://raytracing.github.io/

Tested to run ok with PyPy for significant speedup compared to CPython.

Result image from running 24 instances and averaging the output.

![alt text](result.png "Output")

## Running

It's recommended to use PyPy for running (https://www.pypy.org/)

pypy start.py result 24

This runs the renderer in 24 parallel processes averaging the final result into filename result.ppm.

## Output files

Output files are portable pixmap format (PPM) files. See here https://en.wikipedia.org/wiki/Netpbm

On windows you can use Ifranview to view PPM files directly.

## Dependencies

None