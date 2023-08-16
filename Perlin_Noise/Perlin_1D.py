import matplotlib.pyplot as plt
import numpy
import random


sample = 0.1
world_size = 10
max_x = int(world_size*sample)+int(1/sample+1)

def perlin_noise(step, max_x, gradients):
    _map = []
    # print(len(gradients), gradients)
    x=0
    for _ in range(int(max_x/step-(1/step+1))):
        _x = float(x-int(x))
        f_x = 6*(_x**5)-15*(_x**4)+10*(_x**3)
        value = gradients[int(x)]+f_x*(gradients[int(x)+1]-gradients[int(x)])
        _map.append(min(world_size, value))
        # print(int(x))
        x+=step
    return _map

gradients = [random.uniform(-numpy.pi/2*0.01,numpy.pi/2*0.01) for i in range(max_x)]
_map = perlin_noise(sample,max_x,gradients)
array = numpy.asarray(_map)
plt.plot(array)
plt.show()
