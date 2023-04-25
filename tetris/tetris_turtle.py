import turtle
import random
import time
import keyboard

turtle.Screen().bgcolor('black')
t = turtle.Turtle()
t.penup()
t.shape('square')
t.shapesize(1.5)
t.hideturtle()
t.penup()
turtle.tracer(0,0)
t0 = turtle.Turtle()
t0.penup()
t0.shape('square')
t0.shapesize(1.5)
t0.hideturtle()
t0.penup()
t0.color('white')

#game init setting 
start_block = random.randint(0,6)
drop = True
drop_speed = 30/60
score = 0


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
       [0,0,0,0,0,0,0,0,0,0]]
empty = map

def switchrows(list1, list2):
    templist = []
    templist = list1
    list1=list2
    list2=templist
    return list1, list2

def scan_map(map):
    global score
    global found_row
    found_row = 0
    _map = map
    

    for x in map:
        correct_y = 0
        for i in map:
            line = True
            for item in i:
                if item == 0:
                    line = False
            
            if line:
                score+=1
                found_row = correct_y
                loop_y = found_row+1
                _map[correct_y]=[0,0,0,0,0,0,0,0,0,0]
                while(loop_y!=len(_map)):
                    list1, list2 = switchrows(_map[loop_y], _map[loop_y-1])
                    _map[loop_y] = list1
                    _map[loop_y-1] = list2
                    loop_y+=1
                    turtle.update()
            correct_y+=1
        
    return _map


def draw_map(map, mapt, xpos, lenshape):
    t0.clear()
    mapt.clear()
    for m in range(0, len(map)):
        for n in range(0, len(map[m])):
            mapt.setpos(n*31-15.5*len(map[m]),m*31-15.5*len(map))
            if map[m][n]==0:
                if n-xpos >= 0 and n-xpos<=lenshape-1:
                    mapt.color('white')
                else:
                    mapt.color('grey')
                mapt.stamp()
            #[self.square, self.line, self.L_left, self.L_right, self.T, self.ladder_right, self.ladder_left]
            elif map[m][n]==1:
                mapt.color('yellow')
                mapt.stamp()
            elif map[m][n]==2:
                mapt.color('light blue')
                mapt.stamp()
            elif map[m][n]==3:
                mapt.color('blue')
                mapt.stamp()
            elif map[m][n]==4:
                mapt.color('orange')
                mapt.stamp()
            elif map[m][n]==5:
                mapt.color('purple')
                mapt.stamp()
            elif map[m][n]==6:
                mapt.color('red')
                mapt.stamp()
            elif map[m][n]==7:
                mapt.color('green')
                mapt.stamp()   
class shape():
    def __init__(self, pen, xpos=4, ypos=16, shape=1, map=[], time_delay=1, time_rot_delay=0.1, controll_delay=0.09):
        self.last_controll = 0
        self.controll_delay = controll_delay
        self.last_rotation_time = 0
        self.time_rot_delay = time_rot_delay
        self.last_drop_to_ground = 0
        self.time_delay = time_delay
        self.pen = pen
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
        self.now_shape=random.randint(0,6)
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
                    if self.map[self.ypos+ycor-1][self.xpos+xcor]!=0 or self.ypos==len(self.map_shape)-1:
                        hit = True
                xcor+=1
            ycor -= 1
            
        if hit:        
            self.last_drop_to_ground = time.time()
            while(time.time()-self.last_drop_to_ground<self.time_delay):
                if keyboard.is_pressed('a'):self.left()
                if keyboard.is_pressed('d'):self.right()
                draw_map(map, t, self.xpos, len(self.map_shape[0]))
                self.update()

                self.render()
                
                turtle.update()    
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
        draw_map(map, t, self.xpos, len(self.map_shape[0]))
        turtle.update()
        time.sleep(0.23)
    def render(self):
        self.pen.color('blue')
        ycor = 0
        xcor = 0
        for y in reversed(self.map_shape):
            xcor = 0
            for x in y:
                if x!=0:
                    if self.now_shape+1==1:
                        self.pen.color('yellow')
                    elif self.now_shape+1==2:
                        self.pen.color('light blue')
                    elif self.now_shape+1==3:
                        self.pen.color('blue')
                    elif self.now_shape+1==4:
                        self.pen.color('orange')
                    elif self.now_shape+1==5:
                        self.pen.color('purple')
                    elif self.now_shape+1==6:
                        self.pen.color('red')
                    elif self.now_shape+1==7:
                        self.pen.color('green')
                    self.pen.setpos((self.xpos+xcor)*31-15.5*len(self.map[self.xpos]), (self.ypos+ycor)*31-15.5*len(self.map))
                    self.pen.stamp()
                xcor+=1
            ycor -= 1

def main():   
    global map, empt
    shape_sys = shape(map=map, pen=t, shape=start_block) 
    last_cycle_time = time.time()
    while(True):
        t0.setpos(len(map[0])/2*31-15.5*len(map[0]), 360)
        t0.write(score, align="center", font=('Arial', 20, 'normal'))
        if keyboard.is_pressed('r'):shape_sys.rotate()
        if keyboard.is_pressed('a'):shape_sys.left()
        if keyboard.is_pressed('d'):shape_sys.right()
        if keyboard.is_pressed('s'):
            s_press = True
        else:
            s_press = False
        if keyboard.is_pressed('space'):shape_sys.hardrop()
        draw_map(map, t, shape_sys.xpos, len(shape_sys.map_shape[0]))
        shape_sys.update()

        shape_sys.render()
        
        if time.time()-last_cycle_time>=drop_speed and drop and not(s_press):
                shape_sys.check_ground()
                last_cycle_time = time.time()
        elif time.time()-last_cycle_time>=drop_speed*0.01 and drop and s_press:
                shape_sys.check_ground()
                last_cycle_time = time.time()
        # elif time.time()-last_cycle_time>=drop_speed*0 and drop and space_press:
        #         shape_sys.check_ground()
        #         last_cycle_time = time.time()
        turtle.update()
        
if __name__ == '__main__':
    main()