import pygame
import numpy

pygame.init()

w,h=500,500
screen=pygame.display.set_mode((w,h),flags=pygame.RESIZABLE)
clock=pygame.time.Clock()

aspect_ratio=w/h
fov = numpy.pi/2

n = 0.2
f = 100

t=numpy.tan(fov/2)*n
b=-t
r=t*aspect_ratio
l=-r

X,Y=0,0


#other shit
def load(file,scl=1):
    with open(file, mode="r+") as f:
        verts = []
        faces = []
        lines = f.readlines()
        for line in lines:
            line=line.split()
            if line[0]=="v":
                pos = [float(line[1])*scl, float(line[2])*scl, float(line[3])*scl]
                verts.append(pos)
            if line[0]=="f":
                pos = [int(line[1].split("/")[0])-1, int(line[2].split("/")[0])-1, int(line[3].split("/")[0])-1]
                faces.append(pos)
                
                
    return verts, faces

#math shit
def camera_projection(p,r_v,u_v,f_v,pos):
    l_v = [-r_v[0],-r_v[1],-r_v[2]]
    _f_v = [-f_v[0],-f_v[1],-f_v[2]]
    tx=numpy.dot(pos,r_v)
    ty=numpy.dot(pos,u_v)
    tz=numpy.dot(pos,_f_v)
    
    np = [p[0]*r_v[0]+p[1]*r_v[1]+p[2]*r_v[2]-tx,
          p[0]*u_v[0]+p[1]*u_v[1]+p[2]*u_v[2]-ty,
          p[0]*_f_v[0]+p[1]*_f_v[1]+p[2]*_f_v[2]-tz]
    
    return np

def project_point(p):
    np = [p[0]*n/r,
          p[1]*n/t,
          p[2]*-(f+n)/(f-n)+p[3]*-2*f*n/(f-n),
          -p[2]]
    
    if np[3]>0:
        for i in range(len(np)):
            np[i]/=np[3]
    
    np = [w/2*np[0]+X+w/2,
          h/2*np[1]+Y+h/2,
          (f-n)/2*np[2]+(f+n)/2*np[3],
          np[3]*1]

    return np

def norm(v):
    length = numpy.sqrt(v[0]**2+v[1]**2+v[2]**2)
    for i in range(len(v)):
        v[i]/=length

    
def rotateX(p,theta):
    matrix = numpy.array([[1,0,0],
                          [0,numpy.cos(theta),-numpy.sin(theta)],
                          [0,numpy.sin(theta),numpy.cos(theta)]])
    np = numpy.matmul(matrix,numpy.array([[p[0]],[p[1]],[p[2]]]))
    return [np.item(0,0),np.item(1,0),np.item(2,0)]
    
def rotateY(p,theta):
    matrix = numpy.array([[numpy.cos(theta),0,numpy.sin(theta)],
                          [0,1,0],
                          [-numpy.sin(theta),0,numpy.cos(theta)]])
    np = numpy.matmul(matrix,numpy.array([[p[0]],[p[1]],[p[2]]]))
    return [np.item(0,0),np.item(1,0),np.item(2,0)]
    
def rotateZ(p,theta):
    matrix = numpy.array([[numpy.cos(theta),-numpy.sin(theta),0],
                          [numpy.sin(theta),numpy.cos(theta),0],
                          [0,0,1]])
    np = numpy.matmul(matrix,numpy.array([[p[0]],[p[1]],[p[2]]]))
    return [np.item(0,0),np.item(1,0),np.item(2,0)]

def rotateU(p,u,theta):
    rot_m = numpy.array([[(u[0]**2)*(1-numpy.cos(theta))+numpy.cos(theta),u[0]*u[1]*(1-numpy.cos(theta))-u[2]*numpy.sin(theta),u[0]*u[2]*(1-numpy.cos(theta))+u[1]*numpy.sin(theta)],
                            [u[0]*u[1]*(1-numpy.cos(theta))+u[2]*numpy.sin(theta),(u[1]**2)*(1-numpy.cos(theta))+numpy.cos(theta),u[1]*u[2]*(1-numpy.cos(theta))-u[0]*numpy.sin(theta)],
                            [u[0]*u[2]*(1-numpy.cos(theta))-u[1]*numpy.sin(theta),u[1]*u[2]*(1-numpy.cos(theta))+u[0]*numpy.sin(theta),(u[2]**2)*(1-numpy.cos(theta))+numpy.cos(theta)]])

    np = numpy.array([[p[0]],[p[1]],[p[2]]])
    np = numpy.matmul(rot_m,np)
    
    return [np.item(0,0),np.item(1,0),np.item(2,0)]
class object():
    
    def __init__(self,x,y,z,verts,faces,c=(255,255,255)):
        self.x,self.y,self.z=x,y,z
        
        self.c=c
        self.tris = []
        self.projected_tris=[]
        self.rotation_speed=2
        self.u = [0,0,-1]

        self.tiltangle=0
        self.flipangle=0
        
        
        for face in faces:
            self.tris.append([verts[int(face[0])],verts[int(face[1])],verts[int(face[2])],self.c])
            self.projected_tris.append([[0,0,0],[0,0,0],[0,0,0],(255,255,255)])
        
            
    
        
    def rotateX(self,theta):
        for tri in self.tris:
            tri[0] = rotateX(tri[0],theta)
            tri[1] = rotateX(tri[1],theta)
            tri[2] = rotateX(tri[2],theta)
    
      
    def rotateU(self,u,theta):
        for tri in self.tris:
            tri[0] = rotateU(tri[0],u,theta)
            tri[1] = rotateU(tri[1],u,theta)
            tri[2] = rotateU(tri[2],u,theta)
    
    def cal(self,player):
        i=0
        for tri in self.tris:
            # if tri[0][2]>n and tri[1][2]>n and tri[2][2]>n:

            # rx = (self.x-player.rx)
            # ry = (self.y-player.ry)
            # rz = (self.z-player.rz)
            # p0=project_point([tri[0][0]+rx,tri[0][1]+ry,tri[0][2]+rz,1])
            # p1=project_point([tri[1][0]+rx,tri[1][1]+ry,tri[1][2]+rz,1])
            # p2=project_point([tri[2][0]+rx,tri[2][1]+ry,tri[2][2]+rz,1])
            
            p0 = camera_projection([tri[0][0]+self.x,tri[0][1]+self.y,tri[0][2]+self.z],player.r,player.u,player.f,[player.rx,player.ry,player.rz])
            p1 = camera_projection([tri[1][0]+self.x,tri[1][1]+self.y,tri[1][2]+self.z],player.r,player.u,player.f,[player.rx,player.ry,player.rz])
            p2 = camera_projection([tri[2][0]+self.x,tri[2][1]+self.y,tri[2][2]+self.z],player.r,player.u,player.f,[player.rx,player.ry,player.rz])
            
            p0=project_point([p0[0],p0[1],p0[2],1])
            p1=project_point([p1[0],p1[1],p1[2],1])
            p2=project_point([p2[0],p2[1],p2[2],1])

            self.projected_tris[i]=[p0,p1,p2,tri[3]]
            i+=1    
     
            
    def draw(self,screen,player):
        
        for tri in self.projected_tris:
            if tri[0][2]>0 and tri[1][2]>0 and tri[2][2]>0:
                pygame.draw.polygon(screen,tri[3],[tri[0][:2],tri[1][:2],tri[2][:2]],2)

class fighter():
    
    def __init__(self,x,y,z,verts,faces,c=(255,255,255)):
        self.x,self.y,self.z=x,y,z
        self.rx,self.ry,self.rz=0,0,0
        
        self.c=c
        self.tris = []
        self.projected_tris=[]
        self.rotation_speed=0.1
        self.f = [0,0,0]
        self.u = [0,-1,0]
        self.r = [1,0,0]
        
        self.pitchangle=0
        self.yawangle=numpy.pi*3/2
        self.rollangle=0
        
        self.speed=0
        self.maxspeed=5
        self.acceleration=5
        
        for face in faces:
            self.tris.append([verts[int(face[0])],verts[int(face[1])],verts[int(face[2])],self.c])
            self.projected_tris.append([[0,0,0],[0,0,0],[0,0,0],(255,255,255)])
        
            
    def update(self,key,mouse_pos,dt):
        if key[pygame.K_w]:
            self.rx+=self.f[0]*self.maxspeed*dt
            self.ry+=self.f[1]*self.maxspeed*dt
            self.rz+=self.f[2]*self.maxspeed*dt

        if key[pygame.K_s]:
            self.rx+=-self.f[0]*self.maxspeed*dt
            self.ry+=-self.f[1]*self.maxspeed*dt
            self.rz+=-self.f[2]*self.maxspeed*dt

        if key[pygame.K_d]:
            self.rx+=self.r[0]*self.maxspeed*dt
            self.ry+=self.r[1]*self.maxspeed*dt
            self.rz+=self.r[2]*self.maxspeed*dt

        if key[pygame.K_a]:
            self.rx+=-self.r[0]*self.maxspeed*dt
            self.ry+=-self.r[1]*self.maxspeed*dt
            self.rz+=-self.r[2]*self.maxspeed*dt

        if key[pygame.K_SPACE]:
            self.rx+=-self.u[0]*self.maxspeed*dt
            self.ry+=-self.u[1]*self.maxspeed*dt
            self.rz+=-self.u[2]*self.maxspeed*dt

        if key[pygame.K_LSHIFT]:
            self.rx+=self.u[0]*self.maxspeed*dt
            self.ry+=self.u[1]*self.maxspeed*dt
            self.rz+=self.u[2]*self.maxspeed*dt
        self.yawangle=-(mouse_pos[0]-w/2)/(w-200)*2*numpy.pi+numpy.pi*3/2
        self.pitchangle=-(mouse_pos[1]-h/2)/h*numpy.pi
        if mouse_pos[0]>w-100:
            pygame.mouse.set_pos((100,mouse_pos[1]))
        elif mouse_pos[0]<100:
            pygame.mouse.set_pos((w-100,mouse_pos[1]))

        # if mouse_pos[1]>h-100:
        #     pygame.mouse.set_pos((mouse_pos[0],100))
        # elif mouse_pos[1]<100:
        #     pygame.mouse.set_pos((mouse_pos[0],h-100))
        
        # if self.yawangle>2*numpy.pi:
        #     self.yawangle=0
        # elif self.yawangle<0:
        #     self.yawangle=2*numpy.pi

        # if self.pitchangle>2*numpy.pi:
        #     self.pitchangle=0
        # elif self.pitchangle<0:
        #     self.pitchangle=2*numpy.pi

        
        self.f=[numpy.cos(self.yawangle)*numpy.cos(self.pitchangle),
                numpy.sin(self.pitchangle),
                numpy.sin(self.yawangle)*numpy.cos(self.pitchangle)]
        
        self.u=[numpy.cos(self.yawangle)*numpy.cos(self.pitchangle-numpy.pi/2),
                numpy.sin(self.pitchangle-numpy.pi/2),
                numpy.sin(self.yawangle)*numpy.cos(self.pitchangle-numpy.pi/2)]
        
        self.r=numpy.cross(self.f,self.u)
        
        
        norm(self.f)
        norm(self.u)
        norm(self.r)
        
        
        
    def rotateX(self,theta):
        for tri in self.tris:
            tri[0] = rotateX(tri[0],theta)
            tri[1] = rotateX(tri[1],theta)
            tri[2] = rotateX(tri[2],theta)
        
    def rotateY(self,theta):
        for tri in self.tris:
            tri[0] = rotateY(tri[0],theta)
            tri[1] = rotateY(tri[1],theta)
            tri[2] = rotateY(tri[2],theta)
            
            
    def rotateU(self,u,theta):
        for tri in self.tris:
            tri[0] = rotateU(tri[0],u,theta)
            tri[1] = rotateU(tri[1],u,theta)
            tri[2] = rotateU(tri[2],u,theta)
    
    def cal(self):
        i=0
        for tri in self.tris:
            # if tri[0][2]>n and tri[1][2]>n and tri[2][2]>n:
            # p0 = tri[0][0]*numpy.array(self.r)+tri[0][1]*numpy.array(self.u)+tri[0][2]*numpy.array(self.f)
            # p1 = tri[1][0]*numpy.array(self.r)+tri[1][1]*numpy.array(self.u)+tri[1][2]*numpy.array(self.f)
            # p2 = tri[2][0]*numpy.array(self.r)+tri[2][1]*numpy.array(self.u)+tri[2][2]*numpy.array(self.f)
            
            # p0=project_point([p0[0]+self.x,p0[1]+self.y,p0[2]+self.z,1])
            # p1=project_point([p1[0]+self.x,p1[1]+self.y,p1[2]+self.z,1])
            # p2=project_point([p2[0]+self.x,p2[1]+self.y,p2[2]+self.z,1])
            

            p0=project_point([tri[0][0]+self.x,tri[0][1]+self.y,tri[0][2]+self.z,1])
            p1=project_point([tri[1][0]+self.x,tri[1][1]+self.y,tri[1][2]+self.z,1])
            p2=project_point([tri[2][0]+self.x,tri[2][1]+self.y,tri[2][2]+self.z,1])
            
            self.projected_tris[i]=[p0,p1,p2,tri[3]]
            i+=1    
     
            
    def draw(self,screen):
        
        # for tri in self.projected_tris:
        #     if tri[0][2]>0 and tri[1][2]>0 and tri[2][2]>0:
        #         pygame.draw.polygon(screen,tri[3],[tri[0][:2],tri[1][:2],tri[2][:2]],2)
                
        p_u = project_point((self.x+self.f[0],self.y+self.f[1],self.z+self.f[2],3))
        p_o = project_point((self.x,self.y,self.z,1))
        pygame.draw.line(screen, (255,50,50),p_o[:2],p_u[:2],2)
        
        p_u = project_point((self.x+self.u[0],self.y+self.u[1],self.z+self.u[2],3))
        p_o = project_point((self.x,self.y,self.z,1))
        pygame.draw.line(screen, (50,255,50),p_o[:2],p_u[:2],2)
        
        p_u = project_point((self.x+self.r[0],self.y+self.r[1],self.z+self.r[2],3))
        p_o = project_point((self.x,self.y,self.z,1))
        pygame.draw.line(screen, (50,50,255),p_o[:2],p_u[:2],2)
        
        
#pygame shit
def controll():  
    global w,h,r,l,vmatrix
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit()
            quit()
        if e.type==pygame.VIDEORESIZE:
            w,h=pygame.display.get_window_size()
            aspect_ratio=w/h
            r=t*aspect_ratio
            l=-r

            vmatrix = numpy.array([[w/2,0,0,X+w/2],
                    [0,h/2,0,Y+h/2],
                    [0,0,(f-n)/2,(f+n)/2],
                    [0,0,0,1],])


def main():
    verts, faces=load("fighter.obj",scl=1)
    player = fighter(0,5,-10,verts,faces,c=(100,100,100))
    verts, faces=load("cube.obj",scl=1)

    obj0 = object(0,5,-15,verts,faces,c=(250,250,210))
    obj1 = object(10,5,-20,verts,faces,c=(250,250,210))
    obj2 = object(0,5,-25,verts,faces,c=(250,250,210))
    obj3 = object(10,5,-30,verts,faces,c=(250,250,210))
    player.rotateU([1,0,0],0.8)

    world = []

    while(True):
        dt=clock.tick(60)/1000
        controll()
        key=pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()        
        
        pygame.display.set_caption(str(clock.get_fps()))
        
        player.update(key,mouse_pos,dt)
        player.cal()
        obj0.cal(player)
        
        screen.fill((0,0,0))
        obj0.draw(screen,player)

        player.draw(screen)
        
        pygame.display.update()
        
        
main()