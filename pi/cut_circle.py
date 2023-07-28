import turtle
import math
import time
import keyboard
import pyautogui
# screen.cv._rootwindow.resizable(False, False)
yoff = 0
xoff = 0

def draw_tiles(pixel_per_len, t):
    t.pensize(2)
    t.color('green')
    t.penup()
    t.setpos(-pixel_per_len*10+xoff,0+yoff)
    t.pendown()
    t.setpos(pixel_per_len*10+xoff,0+yoff)
    t.penup()
    t.setpos(0+xoff,pixel_per_len*10+yoff)
    t.pendown()
    t.setpos(0+xoff,-pixel_per_len*10+yoff)
    t.penup()
    for i in range(-5, int(1000/pixel_per_len)+5):
        t.setpos((i-int(1000/pixel_per_len/2))*pixel_per_len+xoff,0+yoff)
        t.pendown()
        t.setpos((i-int(1000/pixel_per_len/2))*pixel_per_len+xoff,50+yoff)
        t.setpos((i-int(1000/pixel_per_len/2))*pixel_per_len+xoff,-50+yoff)
        t.setpos((i-int(1000/pixel_per_len/2))*pixel_per_len+xoff,0+yoff)
        t.penup()
        
    for i in range(int(1000/pixel_per_len)+1):
        t.setpos(0+xoff,(i-int(1000/pixel_per_len/2))*pixel_per_len+yoff)
        t.pendown()
        t.setpos(50+xoff,(i-int(1000/pixel_per_len/2))*pixel_per_len+yoff)
        t.setpos(-50+xoff,(i-int(1000/pixel_per_len/2))*pixel_per_len+yoff)
        t.setpos(0+xoff,(i-int(1000/pixel_per_len/2))*pixel_per_len+yoff)
        t.penup()
    t.hideturtle()


def draw_pi(side_n, pen, pixel_per_len):
    #250 pixel 為一單位
    turtle.tracer(0)
    draw_tiles(pixel_per_len, pen)
    pen.pensize(2)
    sides = side_n
    outer_radius = 1/math.cos(math.radians(180/sides))*pixel_per_len
    outer_side = 2*math.sin(math.radians(180/sides))*outer_radius
    inner_sides = (math.sqrt(1+1-2*math.cos(math.radians(360/sides))))*pixel_per_len
      
    pen.setheading(0)
    pen.color("white")      
    #250, 250 is the center
    pen.penup()
    pen.setpos(0+xoff,-pixel_per_len+yoff)
    pen.pendown()
    pen.circle(pixel_per_len)

    #outer_shape
    pen.color('red')
    pen.penup()
    pen.setpos(pixel_per_len+xoff,0+yoff)
    pen.pendown()
    pen.setheading(90)
    pen.fd(outer_side/2)
    for _ in range(sides):
        pen.left(360/sides)
        pen.fd(outer_side)
    pen.penup()
    #inner_shape
    
    pen.color('light blue')
    pen.penup()
    pen.setpos(pixel_per_len+xoff,0+yoff)
    pen.pendown()
    pen.setheading(90)
    pen.left(360/sides/2)
    pen.fd(inner_sides)
    for _ in range(sides):
        pen.left(360/sides)
        pen.fd(inner_sides)
    pen.penup()
        
    inner_mass = 1/2*math.sin(math.radians(360/sides))*sides
    outer_mass = 1/2*(1/math.cos(math.radians(360/sides/2))**2)*math.sin(math.radians(360/sides))*sides
        
    pen.penup()
    pen.color("white")
    pen.setpos(0,275)
    pen.write(str(inner_mass)+" < pi < "+str(outer_mass), font=('Arial', 25, 'normal'), align="center")
    pen.setpos(0,320)
    pen.write("regular "+str(side_n)+"-gon", font=('Arial', 25, 'normal'), align="center")

    pen.hideturtle()
    turtle.update()
turtle.onclick(None)
n=4
filenames = []
pen = turtle.Turtle()
pixel_per_len = 300



while(n<=120000):
    pen.clear()
    turtle.Screen().bgcolor("black")
    draw_pi(n, pen, pixel_per_len)
    # screen_shot = turtle.getscreen()
    # fileName = str(n)
    
    # screen = screen_shot.getcanvas().postscript(colormode='color', file=fileName+".eps")
    # img = Image.open(fileName + '.eps')
    # img.save(fileName + '.jpg') 
    # filenames.append(fileName+'.jpg') 
    # img.close()
    # os.remove(fileName+".eps")
    # time.sleep(0.1)
    if keyboard.is_pressed("w"):    yoff-=6
    if keyboard.is_pressed("s"):    yoff+=6
    if keyboard.is_pressed("a"):    xoff+=6
    if keyboard.is_pressed("d"):    xoff-=6
    # mouse_pos=[]
    if keyboard.is_pressed("-") and keyboard.is_pressed("shift") and n!=1:
        n-=1
    elif keyboard.is_pressed("-") and pixel_per_len!=10:
        x=xoff/pixel_per_len
        y=yoff/pixel_per_len
        pixel_per_len-=10
        xoff = x * pixel_per_len
        yoff = y * pixel_per_len
    if keyboard.is_pressed("+") and keyboard.is_pressed("shift"):
        n+=1
    elif keyboard.is_pressed("+"):
        x=xoff/pixel_per_len
        y=yoff/pixel_per_len
        pixel_per_len+=10
        xoff = x * pixel_per_len
        yoff = y * pixel_per_len
    # n+=1
    
# images = []
# for filename in filenames:
#     images.append(imageio.imread(filename))
# imageio.mimsave('pi.gif', images)



turtle.done()
