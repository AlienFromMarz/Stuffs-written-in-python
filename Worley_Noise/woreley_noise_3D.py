import pygame
import random
import math
import imageio
import matplotlib.pyplot as plt
import threading

screen_size = (900,900)
sample_size = (2,2,2)
sample_rate = 0.04

tile_size = int(screen_size[1]/(sample_size[2]/sample_rate)*1.5)
def draw(map, surface):
    surface.fill((0,0,0))
    for _x in range(len(map)):
        for _z in range(len(map[0])):
            rect = pygame.Rect(_x*tile_size,_z*tile_size, tile_size,tile_size)
            v0 = max(0, min(255, 255*map[_x][_z][0]))
            # v1 = max(0, min(255, 255-255*map[_x][_z][1]))
            # v2 = max(0, min(255, 255*map[_x][_z][2]))
            
            pygame.draw.rect(surface, (v0,v0,v0), rect)
            
def points():
    int_map = []
    points_ = 20
    for x in range(sample_size[0]):
        for y in range(sample_size[1]):
            for z in range(sample_size[2]):
                if random.randint(0,100)<=100:
                    # _x = random.uniform(0,1)+x
                    # _y = random.uniform(0,1)+y
                    # _z = random.uniform(0,1)+z
                    _x = 0.5+x
                    _y = 0.5+y
                    _z = 0.5+z
                    int_map.append((_x, _y, _z))
                    
    # for i in range(points_):
    #     _x = random.uniform(0,sample_size[0]+1)
    #     _y = random.uniform(0,sample_size[1]+1)
    #     _z = random.uniform(0,sample_size[2]+1)
    #     # _x = random.randint(0,sample_size[0])
    #     # _y = random.randint(0,sample_size[1])
    #     # _z = random.randint(0,sample_size[0])
        
    #     int_map.append((_x, _y, _z))
    
    return int_map

def worley_noise(sample_size, sample_rate, points, t_y):
    map = []
    t_x = 0
    t_z = 0
    for s_x in range(int(sample_size[0]/sample_rate)):
        t_z = 0
        map.append([])
        
        for s_z in range(int(sample_size[2]/sample_rate)):
            lowest_value = None
            first_index = 0
            index=0
            for index in range(len(points)):
                dist = math.dist((t_x, t_y, t_z), points[index])
                if lowest_value==None or (lowest_value>dist):
                    lowest_value = dist
                    first_index=index
                index+=1
                    
            sec_value = None
            sec_index = 0
            index=0
            for index in range(len(points)):
                dist = math.dist((t_x, t_y, t_z), points[index])
                if (sec_value==None or (sec_value>dist)) and index!=first_index:
                    sec_value = dist
                    sec_index=index
                index+=1
                
            third_value = None
            for index in range(len(points)):
                dist = math.dist((t_x, t_y, t_z), points[index])
                if (third_value==None or (third_value>dist)) and index!=sec_index and index!=first_index:
                    third_value = dist
            
            value = [lowest_value, sec_value, third_value]
            map[s_x].append(value)
            
            t_z+=sample_rate
            
        t_x+=sample_rate
    
    return map

window = pygame.display.set_mode(screen_size, flags=pygame.RESIZABLE)
w,h =pygame.display.get_window_size()
surface = pygame.Surface((h,h))
clock = pygame.time.Clock()
Points = points()

def plotting():
    fig = plt.figure("points in space")
    ax = fig.add_subplot(projection='3d')

    xs = [item[0] for item in Points]
    ys = [item[1] for item in Points]
    zs = [item[2] for item in Points]


    ax.scatter(xs, ys, zs, label='points')



    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.show()
    
n_thread = threading.Thread(target=plotting, daemon=True)
n_thread.start()

y=0
dir = 0.01
loop = 1

filenames = []

while(loop):
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            quit()
        if e.type==pygame.VIDEORESIZE:
            w,h = pygame.display.get_window_size()
            tile_size = int(h/(sample_size[2]/sample_rate)*1.5)
            surface = pygame.Surface((h,h))
    map = worley_noise(sample_size, sample_rate, Points, y)
    
    draw(map, surface)
    # pygame.image.save(surface,str(y)+".jpg")
    # filenames.append(str(y)+".jpg")
    
    
    
    window.blit(surface, (w/2-h/2, 0))
    y+=dir
    if y>=sample_size[1] or y<0:
        dir*=-1
    
    pygame.display.flip()

    clock.tick(60)
    
    pygame.display.set_caption("fps: " + str(clock.get_fps())+" at y:"+str(y))
    
n_thread.join()
quit()
# images = []   
# for filename in filenames:
#     images.append(imageio.imread(filename))
# imageio.mimsave('worley_boi.gif', images)