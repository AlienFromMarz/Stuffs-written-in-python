import pygame
import numpy
import numba
pygame.init()

w,h=500,500
aspect_ratio=w/h
fov = numpy.pi/2

n = 1
f = 1000

t=numpy.tan(fov/2)*n
b=-t
r=t*aspect_ratio
l=-r


# tmatrix = [[n,0,0,0],
#            [0,n,0,0],
#            [0,0,-(f+n)/(f-n),-2*n*f/(f-n)],
#            [0,0,-1,0],]

tmatrix = [[n/r,0,0,0],
           [0,n/t,0,0],
           [0,0,-(f+n)/(f-n),-2*n*f/(f-n)],
           [0,0,-1,0],]

tmatrix=numpy.matrix(tmatrix)



screen=pygame.display.set_mode((w,h),flags=pygame.RESIZABLE)
clock=pygame.time.Clock()



class tri():
    def __init__(self,p0,p1,p2,c=(255,255,255)) -> None:
        self.point0=[[p0[0]],
                        [p0[1]],
                        [p0[2]],
                        [1]]
        self.point1=[[p1[0]],
                    [p1[1]],
                    [p1[2]],
                    [1]]
        self.point2=[[p2[0]],
                    [p2[1]],
                    [p2[2]],
                    [1]]
        
        self.tpoint0=[0,0,0]
        self.tpoint1=[0,0,0]
        self.tpoint2=[0,0,0]     
        
        self.c=c
        
    def cal(self):
        cal0=tmatrix*self.point0
        cal1=tmatrix*self.point1
        cal2=tmatrix*self.point2
        self.tpoint0=[w/2+cal0.item((0,0)),h/2+cal0.item((1,0)),cal0.item((2,0))]
        self.tpoint1=[w/2+cal1.item((0,0)),h/2+cal1.item((1,0)),cal1.item((2,0))]
        self.tpoint2=[w/2+cal2.item((0,0)),h/2+cal2.item((1,0)),cal2.item((2,0))]
        return cal0,cal1,cal2
    
    
    def draw(self,screen):
        pygame.draw.polygon(screen,self.c,[self.tpoint0[:2],self.tpoint1[:2],self.tpoint2[:2]],1)
        

        
def controll():
    global w,h,r,l
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit()
            quit()
        if e.type==pygame.VIDEORESIZE:
            w,h=pygame.display.get_window_size()
            r=t*aspect_ratio
            l=-r
            
def main():

    l=250
    xstart=-l/2
    ystart=-l/2
    zstart=l
    zend=zstart+l
    


    world = [tri([xstart,ystart,zstart],[xstart+l,ystart,zstart],[xstart,ystart+l,zstart]),
             tri([xstart,ystart,zend],[xstart+l,ystart,zend],[xstart,ystart+l,zend],(255,0,0))]
    
    while(True):
        dt = clock.tick(60)/1000
        controll()
        screen.fill((0,0,0))
        key=pygame.key.get_pressed()


        for face in world:
            face.cal()
            face.draw(screen)
            
        
        pygame.display.flip()
        pygame.display.set_caption(str(clock.get_fps()))
        
            
if __name__=="__main__":
    main()