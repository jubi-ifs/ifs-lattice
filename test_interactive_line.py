import numpy as np
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
from matplotlib.mlab import dist_point_to_segment


class TriangularInteractor(object):
    """
    An polygon editor.

    Key-bindings

      't' toggle vertex markers on and off.  When vertex markers are on,
          you can move them, delete them

      'd' delete the vertex under point

      'i' insert a vertex at point.  You must be within epsilon of the
          line connecting two existing vertices

    """


    def __init__(self, ax, poly, show_ifs=True, show_edges=False):
        if poly.figure is None:
            raise RuntimeError('You must first add the polygon to a figure or\
             canvas before defining the interactor')

        self._showverts = show_ifs
        self._showedges = show_edges
        self._epsilon = 5  # max pixel distance to count as a vertex hit
        
        
        self.ax = ax
        canvas = poly.figure.canvas
        
        
#         self.poly = poly
        
#         x, y = zip(*self.poly.xy)
        x, y = zip(*poly.xy)
        self.line = Line2D(x, y, marker='o', markerfacecolor='r',
                           linestyle=' ', animated=True)
        self.ax.add_line(self.line)
        #self._update_line(poly)

#         self.line.add_callback(self.line_changed)

#         cid = self.poly.add_callback(self.poly_changed)
        self._ind = None  # the active vert

        canvas.mpl_connect('draw_event', self.draw_callback)
        canvas.mpl_connect('button_press_event', self.button_press_callback)
        canvas.mpl_connect('key_press_event', self.key_press_callback)
        canvas.mpl_connect('button_release_event', self.button_release_callback)
        canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
        self.canvas = canvas

    def draw_callback(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        #self.ax.draw_artist(self.poly)
        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)

    def line_changes(self, line):
        '''
        This method is called whenever the line object is called
        '''
        pass

    def poly_changed(self, poly):
        'this method is called whenever the polygon object is called'
        # only copy the artist props to the line (except visibility)
        vis = self.line.get_visible()
        Artist.update_from(self.line, poly)
        self.line.set_visible(vis)  # don't use the poly visibility state
#         self.line.set_linestyle(' ')

    def get_ind_under_point(self, event):
        'get the index of the vertex under point if within epsilon tolerance'

        # display coords
        xy = np.asarray(self.line.get_data())
        x, y = xy[0], xy[1]
        print(x)
        print(y)
        print(event.x, event.y)
        print(self.ax.transData.inverted().transform((event.x, event.y)))
        print(event.xdata, event.ydata)
#         xyt = self.poly.get_transform().transform(xy)
#         xyt = self.line.get_transform().transform(xy)
#         xt, yt = xyt[:, 0], xyt[:, 1]
#         print(xt)
#         print(yt)
        d = np.sqrt((x - event.xdata)**2 + (y - event.ydata)**2)
        indseq = np.nonzero(np.equal(d, np.amin(d)))[0]
        ind = indseq[0]
        
        print(ind)
        print(d[ind])

        ind = None if (d[ind] >= self._epsilon) else ind
        
        print(ind)

        return ind

    def button_press_callback(self, event):
        'whenever a mouse button is pressed'
        if not self._showverts:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        self._ind = self.get_ind_under_point(event)

    def button_release_callback(self, event):
        'whenever a mouse button is released'
        if not self._showverts:
            return
        if event.button != 1:
            return
        self._ind = None


    def key_press_callback(self, event):
        'whenever a key is pressed'
        if not event.inaxes:
            return
        if event.key == 't':
            self._showverts = not self._showverts
            self.line.set_visible(self._showverts)
            if not self._showverts:
                self._showedges = False
                self._ind = None
                
        if event.key == '-':
            self._showedges = not self._showedges
            if self._showedges:
                self.line.set_linestyle('-')
                self._showverts = True
                self.line.set_visible(True)
            else:
                self.line.set_linestyle(' ')
#         elif event.key == 'd':
#             ind = self.get_ind_under_point(event)
#             if ind is not None:
#                 self.poly.xy = [tup for i, tup in enumerate(self.poly.xy) if i != ind]
#                 self.line.set_data(zip(*self.poly.xy))
#         elif event.key == 'i':
#             xys = self.poly.get_transform().transform(self.poly.xy)
#             p = event.x, event.y  # display coords
#             for i in range(len(xys) - 1):
#                 s0 = xys[i]
#                 s1 = xys[i + 1]
#                 d = dist_point_to_segment(p, s0, s1)
#                 if d <= self._epsilon:
#                     self.poly.xy = np.array(
#                         list(self.poly.xy[:i]) +
#                         [(event.xdata, event.ydata)] +
#                         list(self.poly.xy[i:]))
#                     self.line.set_data(zip(*self.poly.xy))
#                     break
        self.canvas.draw()


    def motion_notify_callback(self, event):
        'on mouse movement'
        if not self._showverts:
            return
        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        x, y = event.xdata, event.ydata

        xy_data = list(zip(*self.line.get_data()))
        xy_data[self._ind] = (x, y)
        self.line.set_data(zip(*xy_data))
        

        self.canvas.restore_region(self.background)
        # self.ax.draw_artist(self.poly)
        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon

    theta = np.arange(0, 2*np.pi, 0.5)
    r = 1.5

    xs = r*np.cos(theta)
    ys = r*np.sin(theta)

    poly = Polygon(list(zip(xs, ys)),fill=None, 
                   closed=False, animated=True)

    fig, ax = plt.subplots()
    ax.add_patch(poly)
    p = TriangularInteractor(ax, poly)

    #ax.add_line(p.line)
    ax.set_title('Click and drag a point to move it')
    ax.set_xlim((-2, 2))
    ax.set_ylim((-2, 2))
    plt.show()