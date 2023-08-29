import numpy
import random
import matplotlib.pyplot as plt

octaves = 5
frequency = 3
gain = 0.5

sample_rate = 0.01
world_size = (5,5)

def f(x):
    return 6*(x**5)-15*(x**4)+10*(x**3)

def random_gra(map_size, seed=None):
    if seed:
        print("seed: ",seed)
        random.seed(seed)
        
    gradients=[]
    print("gradients map size: ",map_size[0]*(frequency**(octaves+1))+1, map_size[1]*(frequency**(octaves+1))+1)
    for _x in range(map_size[0]*(frequency**(octaves))):
        gradients.append([])
        for _y in range(map_size[1]*(frequency**(octaves))):
            v0 = random.uniform(-numpy.pi/2,numpy.pi/2)
            v1 = random.uniform(-numpy.pi/2,numpy.pi/2)
            gradients[len(gradients)-1].append([v0, v1])

    return gradients

def in_pro(vect0, vect1):
    return (vect0[0]*vect1[0]+vect0[1]*vect1[1])
def single_noise(gradients, pos):
    try:
        _x, _y = pos[0], pos[1]
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
        return final_value
    except:
        print(len(gradients), len(gradients[0]))
        print(p0)
        
def perlin_noise(sample_rate, world_size, gradients):
    _x=0
    map=[]
    for _ in range(int(world_size[0]/sample_rate)):
        _y=0
        map.append([])
        for __ in range(int(world_size[1]/sample_rate)):
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
            map[_].append(final_value+1)
            
            _y+=sample_rate
        _x+=sample_rate
    return map
def FBM(map=None, gradients=None, frequency=2, gain=0.5):
    if not gradients:
        gradients = random_gra(map_size=world_size, seed=87)
    if not map:
        map = perlin_noise(sample_rate, world_size, gradients)
        
    for x in range(len(map)):
        for y in range(len(map[0])):
            _x, _y = x*sample_rate, y*sample_rate
            amp = gain
            for i in range(octaves):
                # print(x,y)
                map[x][y]+=single_noise(gradients, (_x, _y))*amp
                _x, _y = _x*frequency, _y*frequency
                amp*=gain
                

gradients = random_gra(map_size=world_size, seed=87)
print("done generating gradients")
map = perlin_noise(sample_rate, world_size, gradients)
_map = map.copy()
_array = numpy.asarray(_map)

print("done generating map0")
print("map size" , len(map), len(map[0]))
FBM(map=map, gradients=gradients, frequency=frequency, gain=gain)
        
array = numpy.asarray(map)

plt.style.use("dark_background")

fig, ax = plt.subplots(nrows=1,ncols=2)

plt.suptitle("FBM Octaves: "+str(octaves)+" Frequency: "+str(frequency)+" Gain: "+str(gain))

ax[0].imshow(array, interpolation='nearest', cmap='plasma')
ax[0].set_title("FBM\n Octaves: "+str(octaves)+" Frequency: "+str(frequency)+" Gain: "+str(gain))
ax[1].imshow(_array, interpolation='nearest', cmap='plasma')
ax[1].set_title('original')



ax[0].axis('off')
ax[1].axis('off')

plt.show()