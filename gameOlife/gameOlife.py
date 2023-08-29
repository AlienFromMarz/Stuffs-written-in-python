import pygame
import random
import time
pygame.init()
world_size = (50,50)
def sum(map, x, y):
    sum=0
    for _x in range(0,3):
        for _y in range(0,3):
            if _x-1+x<0 or _x-1+x>world_size[0]-1:
                continue
            if _y-1+y<0 or _y-1+y>world_size[1]-1:
                continue
            elif _x-1+x==x and _y-1+y==y:
                continue
            sum+=map[_x-1+x][_y-1+y]
            
    return sum
def check(map):
    to_kill = []
    to_spawn = []
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y]==1:
                s = sum(map, x, y)
                if not(s==2 or s==3):
                    to_kill.append((x,y))

            else:
                s = sum(map, x, y)
                if s==3:
                    to_spawn.append((x,y))
                    
    for pos in to_kill:
        map[pos[0]][pos[1]]=0

    for pos in to_spawn:
        map[pos[0]][pos[1]]=1
        
def draw(map, surface):
    w,h = pygame.display.get_window_size()
    rect = pygame.Surface((h,h))
    rect.fill((50,50,50))
    rect.convert_alpha()
    rect.set_alpha(51)
    # surface.fill((0,0,0))
    surface.blit(rect, (0,0))
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y]==1:
                pygame.draw.rect(surface, (255,255,255), [x*tile_size, y*tile_size, tile_size,tile_size])

Map = [[0 for y in range(world_size[1])] for x in range(world_size[0])]

window = pygame.display.set_mode((800,800), flags=pygame.RESIZABLE)
w,h = pygame.display.get_window_size()
tile_size = h/(world_size[1]+2)
clock = pygame.time.Clock()
loop=1
surface = pygame.Surface((h,h))
font = pygame.font.SysFont(['方正粗黑宋简体','microsoftsansserif'],50)
while(loop):
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT:
            quit()
        if ev.type==pygame.KEYDOWN:
            if ev.key==pygame.K_SPACE:
                loop=0
        if ev.type==pygame.VIDEORESIZE:
            w,h = pygame.display.get_window_size()
            surface = pygame.Surface((h,h))
            tile_size = h/(world_size[1]+2)
            
    x,y = pygame.mouse.get_pos()
    left = pygame.mouse.get_pressed()[0]
    right = pygame.mouse.get_pressed()[2]
    if left:
        Map[int((x-w/2-h/2)/tile_size)+1][int(y/tile_size)]=1
    if right:
        Map[int((x-w/2-h/2)/tile_size)+1][int(y/tile_size)]=0
        
    window.fill((0,0,0)) 
    text = font.render("build", False, (255,255,255))
    # check(Map)
    draw(Map, surface)
    window.blit(surface, (w/2-h/2,0))
    window.blit(text, (0,0))
    
    pygame.display.flip()
    
    clock.tick(60)

loop=0
timer=time.time()
gen=0
while(1):
    
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT:
            quit()
        if ev.type==pygame.VIDEORESIZE:
            w,h = pygame.display.get_window_size()
            surface = pygame.Surface((h,h))
            tile_size = h/(world_size[1]+2)
    
    window.fill((0,0,0))  
    if time.time()-timer>=0.1:
        timer=time.time()
        check(Map)
        gen+=1
    
    text = font.render(str(gen), False, (255,255,255))
    draw(Map, surface)
    window.blit(surface, (w/2-h/2,0))
    window.blit(text, (0,0))
    
    pygame.display.flip()
    
    clock.tick(60)
    
quit()