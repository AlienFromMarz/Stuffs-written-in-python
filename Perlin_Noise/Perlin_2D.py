import numpy
import random
import matplotlib.pyplot as plt



sample_rate = 0.01
world_size = (10,10)

def f(x):
    return 6*(x**5)-15*(x**4)+10*(x**3)
def polar(vector):
    x,y = vector[0],vector[1]
    angle = numpy.atan2(y,x)
    dis = numpy.sqrt(x**2+y**2)
    return (angle, dis)
def random_gra(map_size):
    gradients=[]
    for _x in range(map_size[0]):
        gradients.append([])
        for _y in range(map_size[1]):
            v0 = random.uniform(-numpy.pi/2,numpy.pi/2)
            v1 = random.uniform(-numpy.pi/2,numpy.pi/2)
            gradients[len(gradients)-1].append([v0, v1])

    return gradients
def in_pro(vect0, vect1):
    return (vect0[0]*vect1[0]+vect0[1]*vect1[1])
def perlin_noise(sample_rate, world_size, gradients):
    _x=0
    map=[]
    for _ in range(int(world_size[0]/sample_rate-(1/sample_rate+1))):
        _y=0
        map.append([])
        for __ in range(int(world_size[1]/sample_rate-(1/sample_rate+1))):
            p0 = (int(_x),int(_y))
            p1 = (p0[0]+1, p0[1])
            p2 = (p0[0], p0[1]+1)
            p3 = (p0[0]+1, p0[1]+1)
            
            gp0 = gradients[p0[0]][p0[1]]
            gp1 = gradients[p1[0]][p1[1]]
            gp2 = gradients[p2[0]][p2[1]]
            gp3 = gradients[p3[0]][p3[1]]
            
            inter_x = _x - p0[0]
            inter_y = _y - p0[1]
            
            u,v = f(inter_x), f(inter_y)
            
            v0 = (1.0-u)*in_pro(gp0, (_x-p0[0], _y-p0[1]))+u*in_pro(gp1, (_x-p1[0], _y-p1[1]))
            v1 = (1.0-u)*in_pro(gp2, (_x-p2[0], _y-p2[1]))+u*in_pro(gp3, (_x-p3[0], _y-p3[1]))
            
            final_value = (1.0-v)*v0+v*v1
            map[len(map)-1].append(final_value+1)
            
            _y+=sample_rate
        _x+=sample_rate
    return map

gradients = random_gra(map_size=world_size)
map = perlin_noise(sample_rate, world_size, gradients)
array = numpy.asarray(map)

plt.figure('Perlin Noise')
plt.imshow(array, cmap="gray", interpolation='nearest')
plt.title("Perlin Noise, sample rate: 0.01, sample size: (10,10)")
plt.show()
