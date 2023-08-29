import math
import pygame
pygame.init()

window = pygame.display.set_mode((1000,1000))
w,h = pygame.display.get_window_size()
clock =pygame.time.Clock()

canvas = pygame.Surface((w,h))
canvas.fill((0,0,0))

gravity = 1
#10/360*2*3.14
angle1 = 3.14
angle2 = 3.14/10

mass1 = 100000
mass2 = 1

l1=100
l2=200

v1=0
v2=0

center_x = 500
center_y = 500

hue = 0
rect = pygame.Surface((w,h))
rect.fill((0,0,0))
rect.convert_alpha()
rect.set_alpha(0)
while(1):
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            quit()
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_SPACE:
                angle1 = 3.14/2
                angle2 = 3.14/2
                
                v1=0
                v2=0
                
    prev_y1 = l1*math.cos(angle1)+center_x
    prev_x1 = l1*math.sin(angle1)+center_y
    
    prev_y2 = l2*math.cos(angle2)+prev_y1
    prev_x2 = l2*math.sin(angle2)+prev_x1
    
    
    #calculate first angle
    num0 = -gravity*(2*mass1+mass2)*math.sin(angle1)
    num1 = -mass2*gravity*math.sin(angle1-2*angle2)
    num2 = -2*math.sin(angle1-angle2)*mass2*((v2**2)*l2+(v1**2)*l1*math.cos(angle1-angle2))
    num3 = l1*(2*mass1+mass2-mass2*math.cos(2*angle1-2*angle2))
    a1 = (num0+num1+num2)/num3
    

    #calculate second angel
    
    num4 = 2*math.sin(angle1-angle2)
    num5 = (v1**2)*l1*(mass1+mass2)+gravity*(mass1+mass2)*math.cos(angle1)+(v2**2)*l2*mass2*math.cos(angle1-angle2)
    num7 = l2*(2*mass1+mass2-mass2*math.cos(2*angle1-2*angle2))
    a2=(num4*num5)/num7
    

    
    v1+=a1
    v2+=a2

    angle1+=v1
    angle2+=v2
    
    
    
    y1 = l1*math.cos(angle1)+center_x
    x1 = l1*math.sin(angle1)+center_y
    
    y2 = l2*math.cos(angle2)+y1
    x2 = l2*math.sin(angle2)+x1
    
    #draw
    
    window.fill((0,0,0))
    window.blit(canvas, (0,0))
    canvas.blit(rect, (0,0))
    
    pygame.draw.line(window, (255,255,255), (500,500),(x1,y1))
    pygame.draw.line(window, (255,255,255), (x1,y1),(x2,y2))
    
    pygame.draw.circle(window, (255,0,0), (x1,y1), 5)
    pygame.draw.circle(window, (255,0,0), (x2,y2), 5)
    pygame.draw.line(canvas, (255,255,255), (prev_x2,prev_y2), (x2,y2), 2)

    pygame.display.set_caption(str(round(clock.get_fps())))
    pygame.display.flip()

    clock.tick(60)
    
