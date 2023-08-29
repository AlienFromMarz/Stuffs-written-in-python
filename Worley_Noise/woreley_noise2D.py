import matplotlib.pyplot as plt
import random
import math
import time
sample_size = (5,5)
sample_rate = 0.01
start_time = time.time()

def worley_noise(sample_size, sample_rate):
    int_map = []
    for x in range(sample_size[0]):
        for y in range(sample_size[1]):
            if random.randint(0,100)<=80:
                _x = random.uniform(0,1)+x
                _y = random.uniform(0,1)+y
                int_map.append((_x, _y))
    map = []
    t_x = 0
    t_y = 0
    for s_x in range(int(sample_size[0]/sample_rate)):
        map.append([])
        t_y=0
        for s_y in range(int(sample_size[1]/sample_rate)):
            
            lowest_value = None
            for index in range(len(int_map)):
                if lowest_value==None or (lowest_value>math.dist((t_x, t_y), int_map[index])):
                    lowest_value = math.dist((t_x, t_y), int_map[index])
            value = (lowest_value)
            map[s_x].append(value)

            t_y+=sample_rate
            
        t_x+=sample_rate
        
        
    return map

map = worley_noise(sample_size, sample_rate)
print(time.time()-start_time)
plt.figure('worley noise')
plt.imshow(map, cmap="gray", interpolation='nearest')
plt.show()
