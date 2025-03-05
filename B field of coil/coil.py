import numpy,math
import pygame
pygame.init()


delta=numpy.pi/90
radius = 0.01
L=2*radius*numpy.pi/(numpy.pi*2/delta)
I=2

def get_coil_v(radius=radius,delta=delta):
    #3 degree per time
    
    angle = 0
    vectors = []
    poses = []
    for i in range(int(2*numpy.pi/delta)):
        poses.append([radius*numpy.cos(angle),radius*numpy.sin(angle),0])
        vectors.append([-numpy.sin(angle)*L,numpy.cos(angle)*L,0])
        
        angle+=delta
        
    return poses,vectors


def get_B(I,l_pos,l_vector,P):
    r_vector = [P[0]-l_pos[0],P[1]-l_pos[1],P[2]-l_pos[2]]
    r = numpy.sqrt(r_vector[0]**2+r_vector[1]**2+r_vector[2]**2)
    r_vector = [r_vector[0]/r,r_vector[1]/r,r_vector[2]/r]
    
    X=(10**(-7))*I/(r**2)
    B_vector = X*numpy.cross(l_vector,r_vector)

    return B_vector


coil_pos,coil_vec = get_coil_v()
z = numpy.arange(-5, 5, 0.25)
x, y = numpy.arange(-5, 5, 0.25),numpy.arange(-2, 2, 0.5)

px,py,pz=[],[],[]
Bx,By,Bz=[],[],[]

for _x in x:
    for _z in z:
        v=[0,0,0]
        for i,_ in enumerate(coil_pos):
            v0 = get_B(I,coil_pos[i],coil_vec[i],[_x,0,_z])
            v[0]+=v0[0]
            v[1]+=v0[1]
            v[2]+=v0[2]
        Bx.append(v[0])
        By.append(v[1])
        Bz.append(v[2])
        px.append(_x)
        py.append(0)
        pz.append(_z)

            




def castxzquiver(x,y,z,bx,by,bz,surface,scl=100,fscl=1,norm=True):
    pygame.draw.circle(surface,(255,0,0),(w/2,h/2),3)
    for i,_ in enumerate(x):
        if x[i]==0 and y[i]==0 and z[i]==0 :
            continue
        
        length = math.sqrt(bx[i]**2+by[i]**2+bz[i]**2)
        pygame.draw.circle(surface,(255,255,255),(x[i]*scl+w/2,z[i]*scl+h/2),2)
        
        if length==0:
            continue
        if norm:
            pygame.draw.line(surface,(255,255,255),(x[i]*scl+w/2,z[i]*scl+h/2),(x[i]*scl+bx[i]/length*0.5*scl+w/2,z[i]*scl+bz[i]/length*0.5*scl+h/2),2)
        else:
            pygame.draw.line(surface,(255,255,255),(x[i]*scl+w/2,z[i]*scl+h/2),(x[i]*scl+bx[i]*fscl+w/2,z[i]*scl+bz[i]*fscl+h/2),2)
    pygame.draw.line(surface,(0,0,255),(-radius*scl+w/2,h/2),(radius*scl+w/2,h/2),3)
    
w,h=800,800
screen=pygame.display.set_mode((w,h))

while(True):
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit()
            quit()
            
            
            
    screen.fill((0,0,0))
    castxzquiver(px,py,pz,Bx,By,Bz,screen)
    pygame.display.flip()