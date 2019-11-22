import numpy as np
import cairo

from cairo_painter import CairoPainter

def chaos_game(c):
    verts = []
    num_verts = 4
    for i in range(num_verts):
        verts.append([c.width/2 + (2*c.width/5) * np.cos(i * 2 * np.pi / num_verts),
                       c.width/2 + (2*c.width/5) * np.sin(i * 2 * np.pi / num_verts)])

    pt = np.array([300, 300])

    num_iters = 100000
    i_0 = 0
    for _ in range(num_iters):
        c.arc(pt[0], pt[1], 0.3)
        i = np.random.randint(num_verts-1)
        if i >= i_0:
            i += 1
        pt = pt + 0.5 * (verts[i] - pt)
        i_0 = i

def main():
    width = 600
    height = width
    with cairo.SVGSurface(None, width, height) as surface:
        context = cairo.Context(surface)
        c = CairoPainter(context, width, height)
        chaos_game(c)
        surface.write_to_png('out.png')
        surface.finish()

if __name__ == '__main__':
    main()
