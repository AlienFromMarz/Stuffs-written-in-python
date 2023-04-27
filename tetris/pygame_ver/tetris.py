import sys
import pygame
import keyboard
import random
import time
import math

#game setting
width, height = 403, 682

pygame.init()
pygame.mixer.init
screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
pygame.display.set_caption('Tetris by allen wu')

rotate_sound = pygame.mixer.Sound("sounds/Button5.wav")
rotate_sound.set_volume(0.2)

# waku = pygame.mixer.Sound("sounds/1.mp3")
# waku.set_volume(0.2)
# senpai = pygame.mixer.Sound("sounds/2.mp3")
# senpai.set_volume(0.2)
# one = pygame.mixer.Sound("sounds/3.mp3")
# one.set_volume(0.2)
# ara = pygame.mixer.Sound("sounds/4.mp3")
# ara.set_volume(0.2)



hard_drop = pygame.mixer.Sound("sounds/hard_drop.wav")
hard_drop.set_volume(0.2)

clear = pygame.mixer.Sound("sounds/clear.wav")
clear.set_volume(0.2)

# music= pygame.mixer.music.load("sounds/song.mp3")
# pygame.mixer.music.set_volume(0.05)
# pygame.mixer.music.play()


#ingame setting
start_block = random.randint(0,6)
drop = True
drop_speed = 30/60
score = 0
start_block = random.randint(0,6)
drop = True
drop_speed = 30/60
score = 0


w, h = pygame.display.get_surface().get_size()
start_x = w/2
map = [[0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0]]#W10H21
empty = map

def clip(surface, x, y, x_size, y_size): #Get a part of the image
    handle_surface = surface.copy() #Sprite that will get process later
    clipRect = pygame.Rect(x,y,x_size,y_size) #Part of the image
    handle_surface.set_clip(clipRect) #Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip()) #Get subsurface
    return image.copy() #Return


def switchrows(list1, list2):
    templist = []
    templist = list1
    list1=list2
    list2=templist
    return list1, list2

def scan_map(map):
    global sum
    global score
    global found_row
    found_row = 0
    _map = map
    sum = 0

    for x in map:
        correct_y = 0
        for i in map:
            line = True
            for item in i:
                if item == 0:
                    line = False
            if line:
                sum+=1
                score+=1
                found_row = correct_y
                loop_y = found_row+1
                _map[correct_y]=[0,0,0,0,0,0,0,0,0,0]
                while(loop_y!=len(_map)):
                    list1, list2 = switchrows(_map[loop_y], _map[loop_y-1])
                    _map[loop_y] = list1
                    _map[loop_y-1] = list2
                    loop_y+=1
            correct_y+=1
    if sum == 1:
        clear.play()
    if sum == 2:
        clear.play()
    if sum == 3:
        clear.play()
    if sum == 4:
        clear.play()
    return _map

def draw_map(map, xpos=0, lenshape=0, screen=screen, screen_width=width, screen_height=height, holdpiece=None, holdpiecenum=None, shake=False):
    global _one, two, three, four, five, six, seven
    # IMAGE = pygame.image.load('image/background.jpg')
    # IMAGE = pygame.transform.scale(IMAGE, (735*h/1140, h))
    block_y = h/(len(map))
    screen.fill((0,0,0))
    # screen.blit(IMAGE, (w/2-735*h/1140/2,0))
    
    _one = pygame.image.load('image/1.png')
    _one = clip(_one, 0,0,23,23)
    _one = pygame.transform.scale(_one, (int(block_y)+1, int(block_y)+1))
    onerect = _one.get_rect()
    onerect.center = ((block_y)/2+1, (block_y)/2+1)

    two = pygame.image.load('image/2.png')
    two = clip(two, 0,0,23,23)
    two = pygame.transform.scale(two, (int(block_y)+1, int(block_y)+1))
    tworect = two.get_rect()
    tworect.center = ((block_y)/2+1, (block_y)/2+1)

    three = pygame.image.load('image/3.png')
    three = clip(three, 0,0,23,23)
    three = pygame.transform.scale(three, (int(block_y)+1, int(block_y)+1))
    threerect = three.get_rect()
    threerect.center = ((block_y)/2+1, (block_y)/2+1)

    four = pygame.image.load('image/4.png')
    four = clip(four, 0,0,23,23)
    four = pygame.transform.scale(four, (int(block_y)+1, int(block_y)+1))
    fourrect = four.get_rect()
    fourrect.center = ((block_y)/2+1, (block_y)/2+1)

    five = pygame.image.load('image/5.png')
    five = clip(five, 0,0,23,23)
    five = pygame.transform.scale(five, (int(block_y)+1, int(block_y)+1))
    fiverect = five.get_rect()
    fiverect.center = ((block_y)/2+1, (block_y)/2+1)

    six = pygame.image.load('image/6.png')
    six = clip(six, 0,0,23,23)
    six = pygame.transform.scale(six, (int(block_y)+1, int(block_y)+1))
    sixrect = six.get_rect()
    sixrect.center = ((block_y)/2+1, (block_y)/2+1)

    seven = pygame.image.load('image/7.png')
    seven = clip(seven, 0,0,23,23)
    seven = pygame.transform.scale(seven, (int(block_y)+1, int(block_y)+1))
    sevenrect = seven.get_rect()
    sevenrect.center = ((block_y)/2+1, (block_y)/2+1)
    if shake:
        offset = random.uniform(-10.0, 10.0)
    else:
        offset = time.time()
    for m in range(0, len(map)):
        for n in range(0, len(map[m])):
            if shake:
                x = start_x-5*block_y+n*block_y+math.sin(offset)*15+math.sin(offset)*3
                y = float(h)-m*block_y-block_y*2+math.sin(offset)*15+math.sin(offset)*3
            else:
                x = start_x-5*block_y+n*block_y+math.sin(offset)*3
                y = float(h)-m*block_y-block_y*2+math.sin(offset)*3
            rect = pygame.Rect(x, y, block_y, block_y)
            if map[m][n]==1:
                screen.blit(_one, (x,y))
                # pygame.draw.rect(screen, (255, 255, 0), rect)
            elif map[m][n]==2:
                screen.blit(two, (x,y))
                # pygame.draw.rect(screen, (0, 255, 255), rect)
            elif map[m][n]==3:
                screen.blit(three, (x,y))
                # pygame.draw.rect(screen, (0, 0, 255), rect)
            elif map[m][n]==4:
                screen.blit(four, (x,y))
                # pygame.draw.rect(screen, (255, 128, 0), rect)
            elif map[m][n]==5:
                screen.blit(five, (x,y))
                # pygame.draw.rect(screen, (204, 0, 204), rect)
            elif map[m][n]==6:
                screen.blit(six, (x,y))
                # pygame.draw.rect(screen, (255, 0, 0), rect)
            elif map[m][n]==7:
                screen.blit(seven, (x,y))
                # pygame.draw.rect(screen, (0, 255, 0), rect)
            
            else:
                if n-xpos >= 0 and n-xpos<=lenshape-1:
                    rect = pygame.Surface((int(block_y)+1, int(block_y)+1))
                    rect.set_alpha(230) 
                    rect.fill((150, 150, 150))
                    screen.blit(rect, (x,y))
                else:
                    rect = pygame.Surface((int(block_y)+1, int(block_y)+1))
                    rect.set_alpha(230) 
                    rect.fill((100, 100, 100))
                    screen.blit(rect, (x,y))
                    
    if holdpiece!=None:
        ycor = 0
        xcor = 0
        for y in reversed(holdpiece):
            xcor = 0
            for x in y:
                rect.set_alpha(0) 
                posx = start_x-5*block_y+(13+xcor)*block_y
                posy = h-(18+ycor)*block_y-block_y*2
                if x==1:
                    if holdpiecenum+1==1:
                        screen.blit(_one, (posx,posy))
                    if holdpiecenum+1==2:
                        screen.blit(two, (posx,posy))
                    if holdpiecenum+1==3:
                        screen.blit(three, (posx,posy))
                    if holdpiecenum+1==4:
                        screen.blit(four, (posx,posy))
                    if holdpiecenum+1==5:
                        screen.blit(five, (posx,posy))
                    if holdpiecenum+1==6:
                        screen.blit(six, (posx,posy))
                    if holdpiecenum+1==7:
                        screen.blit(seven, (posx,posy))
                elif x==0:
                    rect = pygame.Surface((block_y,block_y))
                    rect.set_alpha(300) 
                    rect.fill((40, 40, 40))
                screen.blit(rect, (posx,posy))
                xcor+=1
            ycor -= 1

class shape():
    def __init__(self, xpos=4, ypos=19, shape=1, map=[], time_delay=1, time_rot_delay=0.09, controll_delay=0.075,screen_height=height):
        self.hard_drop_delay = 0.1
        self.hold = 0
        self.screen_height=screen_height
        self.last_controll = 0
        self.controll_delay = controll_delay
        self.last_rotation_time = 0
        self.time_rot_delay = time_rot_delay
        self.last_drop_to_ground = 0
        self.time_delay = time_delay
        self.xpos = xpos
        self.ypos = ypos
        self.now_shape = shape
        
        self.map = map
        self.rotation = 0
        
        self.square = [[1,1],
                       [1,1]]
        
        self.line = [[1,1,1,1]]
                
        self.L_right = [[1,0,0],
                        [1,1,1]]
        
        self.L_left = [ [0,0,1],
                        [1,1,1]]
        
        self.T = [[0,1,0],
                  [1,1,1]]
        
        self.ladder_right = [[0,1,1],
                            [1,1,0]]
        
        self.ladder_left = [[1,1,0],
                            [0,1,1]]

        self.shapelist=[self.square, self.line, self.L_left, self.L_right, self.T, self.ladder_right, self.ladder_left]
        self.map_shape = self.shapelist[self.now_shape]
        
    def respawn(self):
        self.xpos=4
        self.ypos=len(self.map)-1
        self.now_shape=random.randint(0,8)
        if self.now_shape>6:
            self.now_shape=1
        self.map = scan_map(self.map)
        self.rotation = 0

    def update(self):
        self.map_shape = self.shapelist[self.now_shape]
        self.shapelist=[self.square, self.line, self.L_left, self.L_right, self.T, self.ladder_right, self.ladder_left]
        
    def check_ground(self):
        hit = False
        ycor = 0
        xcor = 0
        for y in reversed(self.map_shape):
            xcor = 0
            for x in y:
                if x!=0:
                    if not(self.ypos==len(self.map_shape)-1):
                        if self.map[self.ypos+ycor-1][self.xpos+xcor]!=0:
                            hit = True
                    else:
                        hit = True
                xcor+=1
            ycor -= 1
            
        if hit:        
            self.last_drop_to_ground = time.time()
            while(time.time()-self.last_drop_to_ground<self.time_delay):
                if keyboard.is_pressed('a'):self.left()
                if keyboard.is_pressed('d'):self.right()
                draw_map(map=map, xpos=self.xpos, lenshape=len(self.map_shape[0]), holdpiece=self.shapelist[self.hold], holdpiecenum=self.hold)
                self.update()

                self.render()
                
                pygame.display.update()    
            ycor = 0
            xcor = 0
            
            for y in reversed(self.map_shape):
                xcor = 0
                for x in y:
                    if x!=0:
                        self.map[self.ypos+ycor][self.xpos+xcor]=self.now_shape+1
                    xcor+=1
                ycor -= 1
            self.respawn()
        else:
            self.ypos-=1
            
            
            
    def collision(self, block_map):
        allow = True
        ycor = 0
        xcor = 0
        for y in reversed(block_map):
            xcor = 0
            for x in y:
                if self.ypos+ycor<len(self.map)-1 and self.xpos+xcor<len(self.map[0]):
                    if self.map[self.ypos+ycor][self.xpos+xcor]!=0 or self.ypos==len(self.map_shape):
                            allow = False   
                else :
                    allow = False
                xcor+=1
            ycor -= 1
        return allow
            
    
    def rotate(self):
        if time.time()-self.last_rotation_time>=self.time_rot_delay:
            rotate_sound.play()
            if self.now_shape == 1:
                last_shape = self.line
                last_rotation = self.rotation
                if self.rotation==0:
                    self.line = [[1,1,1,1]]
                    self.rotation=1
                else:
                    self.line = [[1],
                                [1],
                                [1],
                                [1]]
                    self.rotation=0
                if not(self.collision(self.line)):
                    self.line = last_shape
                    self.rotation = last_rotation
                
            if self.now_shape == 2:
                last_shape = self.L_left
                last_rotation = self.rotation
                if self.rotation==0:
                    self.L_left = [[1,1],
                                   [0,1],
                                   [0,1]]
                    self.rotation=1
                elif self.rotation == 1:
                    self.L_left = [[0,0,1],
                                   [1,1,1]]
                    self.rotation=2
                elif self.rotation == 2:
                    self.L_left = [[1,0],
                                   [1,0],
                                   [1,1]]
                    self.rotation=3
                    
                elif self.rotation == 3:
                    self.L_left = [[1,1,1],
                                   [1,0,0]]
                    self.rotation=0
                if not(self.collision(self.L_left)):
                    self.L_left = last_shape
                    self.rotation = last_rotation
                    
            if self.now_shape == 3:
                last_shape = self.L_right
                last_rotation = self.rotation
                if self.rotation==0:
                    self.L_right = [[0,1],
                                    [0,1],
                                    [1,1]]
                    self.rotation=1
                elif self.rotation == 1:
                    self.L_right = [[1,0,0],
                                    [1,1,1]]
                    self.rotation=2
                elif self.rotation == 2:
                    self.L_right = [[1,1],
                                    [1,0],
                                    [1,0]]
                    self.rotation=3
                    
                elif self.rotation == 3:
                    self.L_right = [[1,1,1],
                                    [0,0,1]]
                    self.rotation=0    
                if not(self.collision(self.L_right)):    
                    self.L_right = last_shape
                    self.rotation = last_rotation
                
            if self.now_shape == 4:
                last_shape = self.T
                last_rotation = self.rotation
                if self.rotation==0:
                    self.T = [[0,1],
                              [1,1],
                              [0,1]]
                    self.rotation=1
                elif self.rotation == 1:
                    self.T = [[0,1,0],
                              [1,1,1]]
                    self.rotation=2
                elif self.rotation == 2:
                    self.T = [[1,0],
                              [1,1],
                              [1,0]]
                    self.rotation=3
                    
                elif self.rotation == 3:
                    self.T = [[1,1,1],
                              [0,1,0]]
                    self.rotation=0            
                if not(self.collision(self.T)):
                    self.T = last_shape
                    self.rotation = last_rotation
                
                
            if self.now_shape == 5:
                last_shape = self.ladder_right
                last_rotation = self.rotation
                if self.rotation==0:
                    self.ladder_right = [[1,0],
                                         [1,1],
                                         [0,1]]
                    self.rotation=1
                elif self.rotation == 1:
                    self.ladder_right = [[0,1,1],
                                         [1,1,0]]
                    self.rotation=0  
                    
                if not(self.collision(self.ladder_right)):
                    self.ladder_right = last_shape
                    self.rotation = last_rotation
                
            if self.now_shape == 6:
                last_shape = self.ladder_left
                last_rotation = self.rotation
                if self.rotation==0:
                    self.ladder_left = [[0,1],
                                        [1,1],
                                        [1,0]]
                    self.rotation=1
                elif self.rotation == 1:
                    self.ladder_left = [[1,1,0],
                                        [0,1,1]]
                    self.rotation=0  
                if not(self.collision(self.ladder_left)):
                    self.ladder_left = last_shape
                    self.rotation = last_rotation
                
                
            self.last_rotation_time = time.time()


    def left(self):
        if time.time()-self.last_controll>=self.controll_delay:
            hit = False
            ycor = 0
            xcor = 0
            for y in reversed(self.map_shape):
                xcor = 0
                for x in y:
                    if xcor==0:
                        if self.xpos+xcor-1>-1:
                            if x!=0:
                                if self.map[self.ypos+ycor][self.xpos+xcor-1]!=0:
                                    hit = True            
                        else:
                            hit = True  
                    xcor+=1
                ycor -= 1
            if not(hit):    self.xpos-=1
            self.last_controll=time.time()
                
        
    def right(self):
        if time.time()-self.last_controll>=self.controll_delay:
            hit = False
            ycor = 0
            xcor = 0
            for y in reversed(self.map_shape):
                xcor = 0
                for x in y:
                    if xcor==len(y)-1:
                        if self.xpos+xcor+1<len(self.map[0]):
                            if x!=0:
                                if self.map[self.ypos+ycor][self.xpos+xcor+1]!=0:
                                    hit = True                 
                        else:
                            hit = True  
                        
                    xcor+=1
                ycor -= 1
            if not(hit):    self.xpos+=1
            self.last_controll=time.time()
    def hardrop(self):
        hit = False
        if time.time()-self.last_controll>=self.controll_delay:
            while(not(hit)):
                ycor = 0
                xcor = 0
                for y in reversed(self.map_shape):
                    xcor = 0
                    for x in y:
                        if x!=0:
                            if self.map[self.ypos+ycor-1][self.xpos+xcor]!=0 or self.ypos==len(self.map_shape)-1:
                                hit = True
                        xcor+=1
                    ycor -= 1
                    
                if hit:        
                    ycor = 0
                    xcor = 0
                    for y in reversed(self.map_shape):
                        xcor = 0
                        for x in y:
                            if x!=0:
                                self.map[self.ypos+ycor][self.xpos+xcor]=self.now_shape+1
                            xcor+=1
                        ycor -= 1
                    self.respawn()
                else:
                    self.ypos-=1
        hard_drop.play()
        time0 = time.time()
        while(not(time.time()-time0>=self.hard_drop_delay)):
            draw_map(map=map, xpos=self.xpos, lenshape=len(self.map_shape[0]), holdpiece=self.shapelist[self.hold], holdpiecenum=self.hold, shake=True)
            pygame.display.update()
        time.sleep(0.25)
        
    def swap(self):
        if time.time()-self.last_controll>=self.controll_delay:
            if self.hold!=None:
                temp=self.now_shape
                self.xpos=4
                self.ypos=len(self.map)-1
                self.now_shape=self.hold
                self.hold=temp
                self.rotation = 0
            else:
                self.hold=self.now_shape
                self.respawn()
            self.last_controll = time.time()
            time.sleep(0.002)
            
    def find(self):
        find_x = self.xpos
        find_y = self.ypos
        hit = False
        while(not(hit)):
            ycor = 0
            xcor = 0
            for y in reversed(self.map_shape):
                xcor = 0
                for x in y:
                    if x!=0:
                        try:
                            if not(find_y<len(self.map_shape)) and not(find_x+xcor>len(self.map[0])-1):
                                if self.map[find_y+ycor-1][find_x+xcor]!=0:
                                    hit = True
                            else:
                                hit = True
                        except:
                            print("self.now_shape: ", str(self.now_shape), " find_x: ", str(find_x), " find_y: ", str(find_y), " xcor: ", str(xcor), " yocr: ", str(ycor))
                    xcor+=1
                ycor -= 1
                
            if hit:        
                ycor = 0
                xcor = 0
                for y in reversed(self.map_shape):
                    xcor = 0
                    for x in y:
                        if x!=0:
                            block_y = h/(len(self.map))
                            x = start_x-5*block_y+(find_x+xcor)*block_y+math.sin(time.time())*3
                            y = h-(find_y+ycor)*block_y-block_y*2+math.sin(time.time())*3
                            rect = pygame.Rect(x, y, block_y+1, block_y+1)
                            pygame.draw.rect(screen, (200, 200, 200), rect)
                        xcor+=1
                    ycor -= 1
            else:
                find_y-=1
                    
    def render(self):
        ycor = 0
        xcor = 0
        for y in reversed(self.map_shape):
            xcor = 0
            for x in y:
                if x!=0:
                    block_y = h/(len(self.map))
                    x = start_x-5*block_y+(self.xpos+xcor)*block_y+math.sin(time.time())*3
                    y = h-(self.ypos+ycor)*block_y-block_y*2+math.sin(time.time())*3
                    rect = pygame.Rect(x, y, block_y+1, block_y+1)
                    if self.now_shape+1==1:
                        screen.blit(_one, (x,y))
                    elif self.now_shape+1==2:
                        screen.blit(two, (x,y))
                    elif self.now_shape+1==3:
                        screen.blit(three, (x,y))
                    elif self.now_shape+1==4:
                        screen.blit(four, (x,y))
                    elif self.now_shape+1==5:
                        screen.blit(five, (x,y))
                    elif self.now_shape+1==6:
                        screen.blit(six, (x,y))
                    elif self.now_shape+1==7:
                        screen.blit(seven, (x,y))
                xcor+=1
            ycor -= 1

def main():   
    global map, empt, start_x, w, h
    shape_sys = shape(map=map, shape=start_block) 
    last_cycle_time = time.time()
    while(True):
        w, h = pygame.display.get_surface().get_size()
        start_x = w/2
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        if keyboard.is_pressed('r'):
            shape_sys.rotate()
        if keyboard.is_pressed('c'):
            shape_sys.swap()
        if keyboard.is_pressed('a'):
            shape_sys.left()
        if keyboard.is_pressed('d'):
            shape_sys.right()
        if keyboard.is_pressed('space'):
            shape_sys.hardrop()
            
        if keyboard.is_pressed('s'):
            s_press = True
        else:
            s_press = False
        draw_map(map=map, xpos=shape_sys.xpos, lenshape=len(shape_sys.map_shape[0]), holdpiece=shape_sys.shapelist[shape_sys.hold], holdpiecenum=shape_sys.hold)
        shape_sys.update()

        shape_sys.render()
        shape_sys.find()
        if time.time()-last_cycle_time>=drop_speed and drop and not(s_press):
                shape_sys.check_ground()
                last_cycle_time = time.time()
        elif time.time()-last_cycle_time>=drop_speed*0.05 and drop and s_press:
                shape_sys.check_ground()
                last_cycle_time = time.time()
        # elif time.time()-last_cycle_time>=drop_speed*0 and drop and space_press:
        #         shape_sys.check_ground()
        #         last_cycle_time = time.time()
        pygame.display.update()
        
if __name__ == '__main__':
    main()



