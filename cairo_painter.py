import numpy as np
import cairo

class CairoPainter():
    def __init__(self, cairo_context, width, height, initial_color = (1, 1, 1)):
        self.context = cairo_context
        self.width = width
        self.height = height

        self.context.rectangle(0, 0, width, height)
        self.context.set_source_rgb(initial_color[0],
                                    initial_color[1],
                                    initial_color[2])
        self.context.fill()

        self.set_defaults()

    def set_defaults(self, line_width = 1.0, color = (0, 0, 0, 1)):
        self.context.set_line_width(line_width)
        self.default_color = color
        self.set_transform_scale(-1, 1, -1, 1, 50)

    def rectangle(self, x, y, width, height, color = None):
        if color is None:
            color = self.default_color
        self.context.rectangle(x, y, width, height)
        self.context.set_source_rgba(color[0], color[1], color[2], 1)
        self.context.fill()

    def ngon(self, n, x, y, r, theta = 0, color = None, style='stroke'):
        """ constructs a regular n-gon centered at (x, y)
            r is the distance from the center to a vertex
            theta is the rotation offset in radians """
        if color is None:
            color = self.default_color
        for i in range (n+1):
            self.context.line_to(r * np.cos(i*2*np.pi/n + theta) + x,
                                 r * np.sin(i*2*np.pi/n + theta) + y)
        self.context.set_source_rgb(color[0], color[1], color[2])
        if n ==2 or style == 'stroke':
            self.context.stroke()
        else:
            self.context.fill()

    def arc(self, x, y, r, extent = (0, 2*np.pi), color = None, style = 'fill'):
        """ constructs an arc centered at (x, y) with radius r
            that stretches from extent[0] to extent[1] """
        if color is None:
            color = self.default_color
        self.context.arc(x, y, r, extent[0], extent[1])
        self.context.set_source_rgb(color[0], color[1], color[2])
        if style == 'fill':
            self.context.fill()
        else:
            self.context.stroke()

    def line(self, x1, y1, x2, y2, color = None):
        if color is None:
            color = self.default_color
        self.context.move_to(x1,y1)
        self.context.line_to(x2,y2)
        self.context.set_source_rgba(color[0], color[1], color[2], color[3])
        self.context.stroke()

    def transform(self, coord, padding = 50):
        """ transforms a coordinate from the pre-scaled range
        to the range of the cairo surface, according to the set parameters
        """
        x = self.trans_padding + self.trans_xscale * (coord[0] - self.trans_x0)
        y = self.trans_padding + self.trans_yscale * (coord[1] - self.trans_y0)
        return (x, y)

    def set_transform_scale(self, x0, x1, y0, y1, padding):
        """ set the linear transformation to map x0 to the left edge of the canvas
            ( plus the padding ), x1 to the right edge, y0 to the top y1 to the bottom """
        self.trans_x0 = x0
        self.trans_x1 = x1
        self.trans_y0 = y0
        self.trans_y1 = y1
        self.trans_padding = padding
        self.trans_xscale = (self.width - 1 - 2*self.trans_padding) / (self.trans_x1 - self.trans_x0)
        self.trans_yscale = (self.height - 1 - 2*self.trans_padding) / (self.trans_y1 - self.trans_y0)
