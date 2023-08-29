import numpy
import random
import pygame
import math
pygame.init()
octaves = 1
frequency = 2
gain = 0.6

image_size = (600,600)
screen_size = (600,600)
scl = 2
sample_rate = 0.1

#world_size/sample_rate=screen_size/scl
world_size = (int(screen_size[0]/scl*sample_rate),int(screen_size[1]/scl*sample_rate))
print(world_size)
seed = None



def f(x):
    return 6*(x**5)-15*(x**4)+10*(x**3)

def random_gra(map_size, seed=None, octaves=octaves, frequency=frequency):
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
   
def draw_poly(pos0, pos1, steps, amp, ini, surface, color): 
    r=ini
    dx = (pos0[0] - pos1[0])/steps
    dy = (pos0[1] - pos1[1])/steps
    x,y = pos0[0], pos0[1]
    v = random.uniform(-1.5,1.1)
    dcr = color[0]/steps*v
    dcg = color[1]/steps*v
    dcb = color[2]/steps*v
    for _ in range(steps):
        x += dx
        y += dy
        color = (max(0,min(255,color[0]-dcr)), max(0, min(255,color[1]-dcg)), max(0, min(255,color[2]-dcb)))
        pygame.draw.circle(surface, color, (x, y), r)
        r-=amp


def dir_mapping(map, surface, image):
    surface.fill((0,0,0))
    dir_map = []
    print(len(map), len(map[0]))
    for x in range(len(map)):
        dir_map.append([])
        for y in range(len(map[0])):
            pixel = image.get_at((int(x*scl), int(y*scl)))[:3]
            angle = map[int(x)][int(y)]*3.1415926
            dir_map[x].append(angle)
            end_pos = (math.cos(angle)*scl*random.uniform(0.5,5)+scl*x, math.sin(angle)*scl*random.uniform(0.5,5)+scl*y)
            draw_poly((scl*x, scl*y), end_pos, 500, 0.005, scl*random.uniform(0.8,1.2), surface, pixel)
            
            pygame.draw.line(surface, pixel, (scl*x, scl*y), end_pos, 1)

window = pygame.display.set_mode(screen_size)
surface = pygame.Surface(screen_size)
image = pygame.image.load("as.png")



gradients = random_gra(map_size=world_size, seed=87)
print("done generating gradients")
map = perlin_noise(sample_rate, world_size, gradients)

print("done generating map0")
print("map size" , len(map), len(map[0]))
FBM(map=map, gradients=gradients, frequency=frequency, gain=gain)
        
dir_map = []
dir_mapping(map, surface, image)
        
         
while(1):
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            quit()
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_SPACE:
                pygame.image.save(surface, "image_.jpg")
                
                
    window.fill((0,0,0))
    
    window.blit(surface, (0,0))
    pygame.display.flip()
