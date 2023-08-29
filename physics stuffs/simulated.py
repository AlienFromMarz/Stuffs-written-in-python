import math
import pygame
pygame.init()
g = [0,0.6]

def minus(v0, v1):
    return [v0[0]-v1[0],v0[1]-v1[1]]
def add(v0, v1):
    v0[0]+=v1[0]
    v0[1]+=v1[1]
def mult(v0, v1):
    v0[0]*=v1[0]
    v0[1]*=v1[1]
class spring():
    def __init__(self,A,B,ks,color=(255,255,255)):
        self.color = color
        self.ks = ks
        self.l = math.sqrt((A.pos[0]-B.pos[0])**2+(A.pos[1]-B.pos[1])**2)
        self.max_l = math.sqrt((A.pos[0]-B.pos[0])**2+(A.pos[1]-B.pos[1])**2)
        self.A = A
        self.B = B
        
    def update(self):
        # self.A=A
        # self.B=B
        
        self.l = math.sqrt((self.A.pos[0]-self.B.pos[0])**2+(self.A.pos[1]-self.B.pos[1])**2)
        force = -self.ks*(self.l-self.max_l)
        
        center_x = (self.A.pos[0]+self.B.pos[0])/2
        center_y = (self.A.pos[1]+self.B.pos[1])/2
        angle = math.atan2(self.A.pos[1]-center_y,self.A.pos[0]-center_x)
        Xforce = force*math.cos(angle)
        Yforce = force*math.sin(angle)
        
        
        self.A.add_force([Xforce, Yforce])
        self.B.add_force([-Xforce, -Yforce])
        
            
    def draw(self, window):
        pygame.draw.line(window, self.color, self.A.pos, self.B.pos, 5)
        

class particle():
    def __init__(self,pos,mass,color=(255,0,0),w=800,h=800):
        self.color = color
        self.pos = pos
        self.mass = mass
        self.velocity = [0,0]
        self.acceleration = [0,0]
        self.w, self.h = w,h
    def add_force(self, force):
        add(self.acceleration, (force[0]/self.mass,force[1]/self.mass))
        
    def update(self):
        add(self.acceleration,g)
        add(self.velocity, self.acceleration)
        if self.velocity[1]+self.pos[1]>=self.h:
            pass
        else:
            add(self.pos, self.velocity)
            
        mult(self.acceleration, [0,0])
    
        mult(self.velocity, [0.9,0.9])
        
    def draw(self, window):
        pygame.draw.circle(window, self.color, self.pos, 10)
        
window = pygame.display.set_mode((800,800))    
w,h = pygame.display.get_window_size()
clock = pygame.time.Clock()

p0 = particle([w/2, h/2],1)
p1 = particle([w/2+100, h/2],1,color=(50,50,255))
p2 = particle([w/2+100, h/2+100],10,color=(50,255,50))
p3 = particle([w/2, h/2+100],1,color=(50,255,50))
p0.add_force([50,50])
s0 = spring(p0, p1, 0.5)
s1 = spring(p1, p2, 0.5)
s2 = spring(p2, p3, 0.5)
s3 = spring(p3, p0, 0.5)
s4 = spring(p0, p2, 0.5)
s5 = spring(p1, p3, 0.5)


while(1):
    
    
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT:
            quit()
            
    mousepos = pygame.mouse.get_pos()
    mouseleft = pygame.mouse.get_pressed()[0]
    if mouseleft:
        p0.pos = [mousepos[0],mousepos[1]]
    p0.update()
    p1.update()
    p2.update()
    p3.update()

    
    s0.update()
    s1.update()
    s2.update()
    s3.update()
    s4.update()
    s5.update()
    
    window.fill((0,0,0))
    
    s0.draw(window)
    s1.draw(window)
    s2.draw(window)
    s3.draw(window)
    s4.draw(window)
    s5.draw(window)
    
    p0.draw(window)
    p1.draw(window)
    p2.draw(window)
    p3.draw(window)
    pygame.display.flip()
    clock.tick(60)
    