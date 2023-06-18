import pygame
import keyboard
import math
import random
import time
from pygame.locals import *

#this is not my code i dont know where it came from
def clip(surface, x, y, x_size, y_size):
    handle_surface = surface.copy()
    clipRect = pygame.Rect(x,y,x_size,y_size)
    handle_surface.set_clip(clipRect)
    image = surface.subsurface(handle_surface.get_clip()) 
    return image.copy() 


class main():
    def __init__(self, screensize, mapsize, tile_size):
        self.dev_mode = True
        self.width, self.height = screensize[0], screensize[1]
        self.map_width, self.map_height = mapsize[0], mapsize[1]
        pygame.init()
        pygame.font.get_fonts()
        flags = FULLSCREEN | DOUBLEBUF
        self._font = pygame.font.Font(pygame.font.get_default_font(), 15)
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE, flags)
        
        self.tile_size = tile_size        
        self.map = [[random.randint(0,1) for m in range(0, self.map_width)] for n in range(0, self.map_height)]
        self.cannont_pass_id = [1,2,3,4]
        self.map = [[5,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,6],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [7,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,8],
                    ]
        #23x23 total 100x100
        self.texure = pygame.image.load('texture.png')
        surf = pygame.Surface((100, 100))
        self.texures = []
        surf.blit(self.texure, (0,0))
        for o in range(0,4):
            for i in range(0,4):
                self.texures.append(pygame.transform.scale(clip(surf, 23*i, 23*o, 23, 23), (self.tile_size, self.tile_size)))
        
        print(self.texures)
        
        
        self.surface = pygame.Surface((self.map_width*self.tile_size, self.map_height*self.tile_size))
        
        for y in range(0, len(self.map)):
            for x in range(0, len(self.map[y])):
                surface_texture = pygame.Surface((self.tile_size, self.tile_size))
                surface_texture.blit(self.texures[self.map[y][x]], (0,0))
                rect = pygame.Rect(x*self.tile_size, y*tile_size, self.tile_size, self.tile_size)
                if self.map[y][x]>len(self.texures)-1:
                    pygame.draw.rect(self.surface, (200,0,200), rect)
                else:
                    self.surface.blit(surface_texture, (x*self.tile_size, y*self.tile_size))
                    
                x+=1
                
        self.camera_x, self.camera_y = (0,0)
        
        self.start_x, self.start_y = 0,0
        
        self.player_x, self.player_y = ((self.width/self.tile_size-1)/2+1,(self.height/self.tile_size-1)/2+1)
        
        self.player_radius = 0.7
        self.speed = 0.05
        
        
        self.clock = pygame.time.Clock()
        
        self.released_time_x, self.released_time_y = time.time(),time.time()
        self.follow_time = 1
        self.dirx = 0
        self.diry = 0
        
        
        
        
        
        self.run()
    
    def colliison(self, move_x, move_y,radius):
        check_list = []
        collide = [[0 for i in range(0,3)] for o in range(0,3)]
        if self.dev_mode:
            surface = pygame.Surface((self.tile_size*3, self.tile_size*3))
            surface = surface.convert_alpha()
            surface.fill((0, 0, 0, 50))
        
        for yoff in range(-1, 2):
            for xoff in range(-1, 2):
                x = self.tile_size*(math.floor(self.player_x)+xoff-self.camera_x)
                y = self.tile_size*(math.floor(self.player_y)+yoff-self.camera_y)
                if self.map[math.floor(self.player_y)+yoff][math.floor(self.player_x)+xoff] in self.cannont_pass_id:
                    check_list.append([(xoff, yoff), (x,y)])
                    
                    
        
        player_rect = pygame.Rect(self.tile_size*self.player_x+self.start_x+self.tile_size*move_x-radius*self.tile_size/2, self.tile_size*self.player_y+self.start_y+self.tile_size*move_y-radius*self.tile_size/2, self.tile_size*radius, self.tile_size*radius)
        if self.dev_mode:
            self.window.blit(surface, (self.tile_size*self.player_x+self.start_x+self.tile_size*move_x-1.5*self.tile_size, self.tile_size*self.player_y+self.start_y+self.tile_size*move_y-1.5*self.tile_size))
            print(str(len(check_list))+"\t")
        
        for item in check_list:
            rect = pygame.Rect(item[1][0],item[1][1], self.tile_size, self.tile_size)
            # print(item)
            if self.dev_mode:
                pygame.draw.rect(self.window, (0,0,255), rect)
            if pygame.Rect.colliderect(player_rect, rect):
                collide[item[0][1]+1][item[0][0]+1]=1
                if self.dev_mode:
                    pygame.draw.rect(self.window, (255,0,255), rect)
        if self.dev_mode:
            # pygame.draw.rect(self.window, (255,255,255), player_rect)
            print(collide)
            
        return collide
    
    def controll(self):
        for event in pygame.event.get():
            # if event.type == pygame.VIDEORESIZE:
            #     self.surface=pygame.transform.scale(self.surface, (pygame.display.get_window_size()[1]/self.height*self.tile_size*self.map_width, pygame.display.get_window_size()[1]/self.height*self.tile_size*self.map_height))
            if event.type==pygame.QUIT:
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    quit()
                if event.key==pygame.K_e:
                    if self.dev_mode:
                        self.dev_mode = False
                    else:
                        self.dev_mode = True
                    print(self.dev_mode)
        if keyboard.is_pressed('q'):
            map = self.colliison(0, 0,self.player_radius)
        if keyboard.is_pressed('shift'):
            self.speed=0.2
        else:
            self.speed=0.05
        if keyboard.is_pressed('w') or keyboard.is_pressed('a') or keyboard.is_pressed('s') or keyboard.is_pressed('d'):
            # map = self.colliison(0, 0,self.player_radius)
            if keyboard.is_pressed("w") and self.player_y-self.speed>=0:
                map = self.colliison(0, -1*self.speed,self.player_radius)
                if map[0][0]==0 and map[0][1]==0 and map[0][2]==0: 
                    self.player_y-=self.speed
                    self.diry = -1
            elif keyboard.is_pressed("s") and self.player_y+self.speed<=self.map_height-1:
                map = self.colliison(0, 1*self.speed,self.player_radius)
                if map[2][0]==0 and map[2][1]==0 and map[2][2]==0: 
                    self.player_y+=self.speed
                    self.diry = 1
            else:
                self.released_time_x = time.time()
                
            if keyboard.is_pressed("a") and self.player_x-self.speed>=0:
                map = self.colliison(-1*self.speed, 0,self.player_radius)
                if map[0][0]==0 and map[1][0]==0 and map[2][0]==0:
                    self.player_x-=self.speed
                    self.dirx = -1
            elif keyboard.is_pressed("d") and self.player_x+self.speed<=self.map_width-1:
                map = self.colliison(1*self.speed, 0,self.player_radius)
                if map[0][2]==0 and map[1][2]==0 and map[2][2]==0:
                    self.player_x+=self.speed
                    self.dirx = 1
            else:
                self.released_time_y = time.time()
            
            
            
            
    def follow_player(self):
        # if time.time()-self.released_time_x<=self.follow_time:
        effect_x = -0.3*abs((time.time()-self.released_time_x)-self.follow_time)*self.dirx
            # effect_x = 0.3*math.tan(self.follow_time-(time.time()-self.released_time_x))*self.dirx*-1
        # else:
        #     effect_x = 0
        
        # if time.time()-self.released_time_y<=self.follow_time:
        effect_y = -0.3*abs((time.time()-self.released_time_y)-self.follow_time)*self.diry
            # effect_y = 0.3*math.tan(self.follow_time-(time.time()-self.released_time_y))*self.diry*-1
        # else:
        #     effect_y = 0
        
        if self.player_x>(self.width/self.tile_size-1)/2:
            self.camera_x=self.player_x-5+effect_x
        if self.player_y>(self.height/self.tile_size-1)/2:
            self.camera_y=self.player_y-5+effect_y
    
    
    def map_surface(self):
        self.xoffset = self.camera_x-math.floor(self.camera_x)
        self.yoffset = self.camera_y-math.floor(self.camera_y)
        # print("x:"+str(xoffset)+" y:"+str(yoffset))
        # print((-math.floor(self.camera_x)*self.tile_size-self.tile_size*xoffset, -math.floor(self.camera_y)*self.tile_size-self.tile_size*yoffset))
        self.start_x = -math.floor(self.camera_x)*self.tile_size-self.tile_size*self.xoffset
        self.start_y = -math.floor(self.camera_y)*self.tile_size-self.tile_size*self.yoffset
        
        self.window.blit(self.surface, (self.start_x, self.start_y))
        
        
    def run(self):
        while(1):
            self.window.fill((0,0,0))
            
            self.follow_player()
            
            self.map_surface()
        
        
            player = pygame.Rect(self.tile_size*self.player_x+self.start_x-self.tile_size*self.player_radius/2, self.tile_size*self.player_y+self.start_y-self.tile_size*self.player_radius/2, self.tile_size*self.player_radius, self.tile_size*self.player_radius)
            if self.dev_mode:
                text_sur = self._font.render(str("pos:"+str(pygame.mouse.get_pos())+"\n fps:"+str(format(self.clock.get_fps(), '.2f'))), True, (255,255,255))
            else:
                text_sur = self._font.render(str(format(self.clock.get_fps(), '.2f')), True, (255,255,255))
                # text_sur = self._font.render(str(self.released_time_x)+"y:"+str(self.released_time_y), None, (255,255,255))
                
            self.window.blit(text_sur, (0,0))
            
            self.controll()
            
            pygame.draw.rect(self.window, (255,0,0), player)
            
            
            self.clock.tick(60)
            
            pygame.display.update()
            
if __name__=="__main__":
    app = main((550,550),(110,110),50)