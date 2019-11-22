import numpy as np
import cairo

from cairo_painter import CairoPainter

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

def rosette(c):
    def f(z):
        zb = np.conj(z)
        res = (np.power(z, 3) * np.power(zb, 0)
                + np.power(z, 0) * np.power(zb, 3)
                + 3 * np.power(z, -5) * np.power(zb, 1)
                + 3 * np.power(z, 1) * np.power(zb, -5)
                - 2 * np.power(z, 6) * np.power(zb, -4)
                - 2 * np.power(z, -4) * np.power(zb, 6)
                )
        return res

    def color(z):
        res = np.abs(z)
        col = (2 * sigmoid(res) - 1)
        return (col, col, col)

    c.set_transform_scale(-2, 2, -2, 2, 50)

    for a in np.arange(-2, 2, 0.005):
        for b in np.arange(-2, 2, 0.005):
            z = f(a + 1j * b)
            col = color(z)
            coord = c.transform((a, b))
            c.arc(coord[0], coord[1], 2, color = col)

def main():
    width = 500
    height = width
    with cairo.SVGSurface(None, width, height) as surface:
        context = cairo.Context(surface)
        c = CairoPainter(context, width, height)
        rosette(c)
        surface.write_to_png('out.png')
        surface.finish()


if __name__ == '__main__':
    main()
