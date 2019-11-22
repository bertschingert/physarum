import numpy as np
import cairo

from cairo_painter import CairoPainter

def trigonometric_attractor(c_ptr):
    x0 = np.random.rand()
    y0 = np.random.rand()

    a = -1.9
    b = -0.89
    c = 0.93
    d = 0.88
    e = -1.03
    f = 0.33
    g = 1.46
    h = 1.86

    size = 3
    c_ptr.set_transform_scale(-1 * size, size, -1 * size, size, c_ptr.width/20)

    for i in range(50000):
        t = c_ptr.transform((x0, y0))
        c_ptr.arc(t[0], t[1], 0.35)

        x1 = a * np.sin(b * y0) + c * np.cos(d * x0)
        y1 = e * np.sin(f * x0) + g * np.cos(h * y0)

        x0 = x1
        y0 = y1

def aizawa_attractor(c_ptr):
    a = 0.95
    b = 0.7
    c = 0.6
    d = 3.5
    e = 0.25
    f = 0.1

    x0 = 0.1
    y0 = 0
    z0 = 0

    size = 2
    c_ptr.set_transform_scale(-1 * size, size, -1 * size, size, c_ptr.width/20)

    for i in range(50000):
        t = c_ptr.transform((x0, z0))
        c_ptr.arc(t[0], t[1], 0.35)

        dx = (z0 - b) * x0 - d * y0
        dy = d * x0 + (z0 - b) * y0
        dz = c + a * z0 - z0**3 / 3 - (x0**2 + y0**2)*(1 + e*z0) + f * z0 * x0**3

        step = 0.01
        x1 = x0 + step * dx
        y1 = y0 + step * dy
        z1 = z0 + step * dz

        x0 = x1
        y0 = y1
        z0 = z1

def main():
    width = 500 # measured in points
    height = width
    with cairo.SVGSurface(None, width, height) as surface:
        context = cairo.Context(surface)
        c = CairoPainter(context, width, height, initial_color=(0.998, 0.989, 0.978))
        trigonometric_attractor(c)
        surface.write_to_png('out.png')


if __name__ == '__main__':
    main()
