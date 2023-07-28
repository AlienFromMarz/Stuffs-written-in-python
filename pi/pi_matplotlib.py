import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy
from matplotlib.widgets import Slider


fig, ax = plt.subplots(num='割圓術 by 吳承軒')
sides = 4
ax_slider = plt.axes([0.18,0.01,0.65,0.03])

slider_ = Slider(ax_slider, "sides", valmin=3, valmax=100, valinit=4, valstep=1)
def update(side_):
    global sides
    sides = slider_.val
    ax.clear()
    ax.set_xlim((-2.5,2.5))
    ax.set_ylim((-2,2))
    ax.set_aspect('equal')

    inner = 1/2*numpy.sin(numpy.radians(360/sides))*sides
    outer = 1/2*(1/numpy.cos(numpy.radians(360/sides/2))**2)*numpy.sin(numpy.radians(360/sides))*sides
        
    ax.set_title(str(inner)+ " < pi < "+ str(outer))
    circle = plt.Circle((0,0), 1, fill=True, color=[0,1,0])
    
    angle = 360/sides
    #inner
    inner_poly = []
    _angle = 0
    for i in range(sides):
        _angle+=angle
        x,y = numpy.cos(numpy.radians(_angle)), numpy.sin(numpy.radians(_angle))
        inner_poly.append((x,y))
    inner_poly = numpy.array(inner_poly)
    inner_poly_draw = Polygon(inner_poly, facecolor = 'k', fill=True, color=[0,0,1])

    outer_poly = []
    Radius = 1/(numpy.cos(numpy.radians(angle/2)))
    _angle = angle/2
    for i in range(sides):
        _angle+=angle
        x,y = Radius*numpy.cos(numpy.radians(_angle)), Radius*numpy.sin(numpy.radians(_angle))
        outer_poly.append((x,y))
    outer_poly = numpy.array(outer_poly)
    outer_poly_draw = Polygon(outer_poly, facecolor = 'k', fill=True, color=[1,0,0])
    
    ax.add_patch(outer_poly_draw)
    ax.add_patch(circle)
    ax.add_patch(inner_poly_draw)
    ax.grid(True)
    fig.canvas.draw()
    

update(sides)


slider_.on_changed(update)

plt.show()