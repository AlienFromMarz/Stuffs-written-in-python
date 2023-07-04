import math
import pygame
import time
import random

pygame.init()
window = pygame.display.set_mode((500,500))


def draw_map(map, closed_node, open_node):
    window.fill((0,0,0))
    rect = pygame.Surface((tile_size,tile_size))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            quit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                loop = True
                while(loop):
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            quit()
                        if event.type==pygame.KEYDOWN:
                            if event.key==pygame.K_e:
                                loop=False
    for x in range(0,len(map)):
        for y in range(0, len(map[x])):
            if (x,y) in open_node:
                rect.fill((0,0,255))
            elif map[x][y]==2:
                rect.fill((255,0,0))
            elif (x,y)==des:
                rect.fill((255,255,0))
            elif (x,y)==start:
                rect.fill((0,255,255))
            elif (x,y) in closed_node:
                rect.fill((0,255,0))
            else:
                rect.fill((0,0,0))
            window.blit(rect, (x*tile_size, y*tile_size))
    pygame.display.update()

def h(startpos, despos):
    value1 = abs(despos[0]-startpos[0])**2
    value2 = abs(despos[1]-startpos[1])**2
    return value1+value2

def astar(map, startpos, despos, id_price, id_obs):
    draw_map(map, [], [])

    OpenNodes = [] #所有的節點之權重
    ClosedNodes = [] #無須列入計算之節點
    ClosedNodes_pos = []
    OpenNodes.append([startpos, 0, None]) #格式為[座標, g, 父節點]
    ClosedNodes.append([startpos, 0, None]) #格式為[座標, g, 父節點]
    ClosedNodes_pos.append(startpos)
    nodes_now = startpos
    nodes_now_index = 0
    path = []


    try:
        while(nodes_now!=despos):
            print("________________")
            surrounding = [(nodes_now[0], nodes_now[1]+1),
                        (nodes_now[0], nodes_now[1]-1),
                        (nodes_now[0]-1, nodes_now[1]),
                        (nodes_now[0]+1, nodes_now[1])]
            
            index=0
            for item in surrounding:
                if not(item in ClosedNodes_pos) and map[item[0]][item[1]]==1:
                    OpenNodes.append([item, ClosedNodes[nodes_now_index][1]+1, nodes_now])
            
            lowest = 0
            index = 0
            for item in OpenNodes:
                # print(item)
                if item[1]+h(item[0], despos)<OpenNodes[lowest][1]+h(OpenNodes[lowest][0], despos) and not(item[0] in ClosedNodes_pos):
                    lowest = index
                index+=1
            
            ClosedNodes.append(OpenNodes[lowest])
            ClosedNodes_pos.append(OpenNodes[lowest][0])
            OpenNodes.pop(lowest)
            
            nodes_now = ClosedNodes[len(ClosedNodes)-1][0]
            nodes_now_index = len(ClosedNodes)-1
            
            map_ = [ClosedNodes[i][0] for i in range(0,len(ClosedNodes))]
            _map_ = [OpenNodes[i][0] for i in range(0,len(OpenNodes))]
            # draw_map(map, map_, _map_)            
    except:
        print("no path")
    # draw_map(map, map_, [])  
    if ClosedNodes_pos[len(ClosedNodes_pos)-1]==despos:
        From_map = [ClosedNodes[i][2] for i in range(0, len(ClosedNodes))]
        point_to_map = [ClosedNodes[i][0] for i in range(0, len(ClosedNodes))]
        
        dic_path = {point_to_map[i]:From_map[i] for i in range(0, len(From_map))}
        path = [des]
        
        node_now = despos
        
        while(node_now!=startpos):
            path.append(dic_path[node_now])
            node_now = dic_path[node_now]
            
            # print("from " + str(From_map[item]) + " to " + str(point_to_map[item]))
            
        draw_map(map, path, [])

    else:
        print("no path")
    

    print("done") 
    
    
    
    
while(True):
    world_size = 8
    start = (random.randint(1,world_size-3),random.randint(1,world_size-3))
    des = (world_size-2,world_size-2)
    map = []
    tile_size = 500/world_size
    for x in range(0,world_size):
        map.append([])
        for y in range(0,world_size):
            if y==0 or y==world_size-1 or x==0 or x==world_size-1:
                map[x].append(2)
            else:
                if random.randint(1,100)<90 or (x,y)==des or (x,y)==start:
                    map[x].append(1)
                else:
                    map[x].append(2)
    
    astar(map, start, des, 0,0)
    
    loop=True
    while(loop):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_e:
                    loop=False