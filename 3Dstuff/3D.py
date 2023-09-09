import pygame
import math

mode = "tri"
screen = (800,800)
a = screen[0]/screen[1]
fov = math.pi/1.5

zfar = 1000
znear = 0.1


def load(file):
    with open(file, mode="r+") as f:
        verts = []
        faces = []
        lines = f.readlines()
        for line in lines:
            line=line.split()
            print(line)
            if line[0]=="v":
                pos = (float(line[1]), -float(line[2]), float(line[3]))
                verts.append(pos)
            if line[0]=="f":
                if mode=="sq":
                    pos = (int(line[1])-1, int(line[2])-1, int(line[3])-1, int(line[4])-1)
                elif mode=="tri":
                    pos = (int(line[1])-1, int(line[2])-1, int(line[3])-1)
                faces.append(pos)
                
                
    return verts, faces
        
def project(pos):
    x,y,z = pos[0],pos[1],pos[2]
    return (a*(1/math.tan(fov/2))*x/z, (1/math.tan(fov/2))*y/z, z*(zfar/(zfar-znear))-(zfar*znear/zfar-znear))

def cross_product(poses): 
    line1x = poses[1][0]-poses[0][0]
    line1y = poses[1][1]-poses[0][1]
    line1z = poses[1][2]-poses[0][2]
    
    line2x = poses[2][0]-poses[0][0]
    line2y = poses[2][1]-poses[0][1]
    line2z = poses[2][2]-poses[0][2]

    normalX = line1y*line2z-line1z*line2y
    normalY = line1z*line2x-line1x*line2z
    normalZ = line1x*line2y-line1y*line2x
    
    l = math.sqrt(normalX**2+normalY**2+normalZ**2)
    
    if l!=0:
        normalX /= l
        normalY /= l
        normalZ /= l
    else:
        return (0,0,0,0)
    return ((normalX),(normalY),(normalZ),l)
    

        
def light(normal, l_dir=(1,-2,1)):
    l = math.sqrt(l_dir[0]**2+l_dir[1]**2+l_dir[2]**2)
    _l_dir = [l_dir[0], l_dir[1], l_dir[2]]
    _l_dir[0] /= l
    _l_dir[1] /= l
    _l_dir[2] /= l
    dp = normal[0]*l_dir[0]+normal[1]*l_dir[1]+normal[2]*l_dir[2]
    
    return dp

def matrixmul(vect3, m):
    x,y,z = vect3[0],vect3[1],vect3[2]
    _x = x*m[0][0]+y*m[0][1]+z*m[0][2]
    _y = x*m[1][0]+y*m[1][1]+z*m[1][2]
    _z = x*m[2][0]+y*m[2][1]+z*m[2][2]
    return (_x,_y,_z)

def addVector(vect3_0,vect3_1):
    return (vect3_0[0]+vect3_1[0],vect3_0[1]+vect3_1[1],vect3_0[2]+vect3_1[2])
class Vcamera():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        
class triangle():
    def __init__(self, poses):
        self.pos = []
        for pos in poses:
            self.pos.append(pos)
        self.trans_pos = []
        self.pro_pos = []
        
    def update(self, rx=0, ry=0, rz=0, sx=0, sy=0, sz=0):
        for item in range(0,len(self.pos)):
            mx = [[1,0,0],
                  [0,math.cos(rx),-math.sin(rx)],
                  [0,math.sin(rx),math.cos(rx)]]
            my = [[math.cos(ry),0,math.sin(ry)],
                  [0,1,0],
                  [-math.sin(ry),0,math.cos(ry)]]
            mz = [[math.cos(rz),-math.sin(rz),0],
                  [math.sin(rz),math.cos(rz),0],
                  [0,0,1]]
            
            ms = [[sx,0,0],
                  [0,sy,0],
                  [0,0,sz]]
            
            self.pos[item]=matrixmul(self.pos[item], mx)
            self.pos[item]=matrixmul(self.pos[item], my)
            self.pos[item]=matrixmul(self.pos[item], mz)
            
            self.pos[item]=matrixmul(self.pos[item], ms)
            
            
    def projection_cal(self):
        self.pro_pos=[]
        self.trans_pos=[]
        for pos in self.pos:
            pos = (pos[0], pos[1], pos[2]+3)
            self.trans_pos.append(pos)
            self.pro_pos.append(project(pos))
        
    def draw(self, surface):
        _poses = []
        n = cross_product(self.trans_pos)
        if (n[0]*(self.trans_pos[0][0]-camera.x)+n[1]*(self.trans_pos[0][1]-camera.y)+n[2]*(self.trans_pos[0][2]-camera.y))>0:
            color = max(0,min(255,light(n)*255))
            for pos in self.pro_pos:
                _pos = ((pos[0]+1)*0.5*screen[0], (pos[1]+1)*0.5*screen[1], pos[2])
                _poses.append(_pos)
                pygame.draw.rect(surface, (255,0,0), (pos[0],pos[1],1,1))
            if _poses[0][2]<0 or _poses[1][2]<0 or _poses[2][2]<0:
                return False
            pygame.draw.polygon(surface, (color, color, color), ((_poses[0][0],_poses[0][1]),(_poses[1][0],_poses[1][1]),(_poses[2][0],_poses[2][1])))
            # pygame.draw.line(surface, (0,0,0), (_poses[0][0],_poses[0][1]), (_poses[1][0],_poses[1][1]), 1)
            # pygame.draw.line(surface, (0,0,0), (_poses[1][0],_poses[1][1]), (_poses[2][0],_poses[2][1]), 1)
            # pygame.draw.line(surface, (0,0,0), (_poses[2][0],_poses[2][1]), (_poses[0][0],_poses[0][1]), 1)
        
class square():
    def __init__(self, poses):
        self.pos = []
        for pos in poses:
            self.pos.append(pos)
        self.trans_pos = []
        self.pro_pos = []
        
    def update(self, rx=0, ry=0, rz=0, sx=0, sy=0, sz=0):
        for item in range(0,len(self.pos)):
        
            mx = [[1,0,0],
                  [0,math.cos(rx),-math.sin(rx)],
                  [0,math.sin(rx),math.cos(rx)]]
            my = [[math.cos(ry),0,math.sin(ry)],
                  [0,1,0],
                  [-math.sin(ry),0,math.cos(ry)]]
            mz = [[math.cos(rz),-math.sin(rz),0],
                  [math.sin(rz),math.cos(rz),0],
                  [0,0,1]]
            
            ms = [[sx,0,0],
                  [0,sy,0],
                  [0,0,sz]]
            
            self.pos[item]=matrixmul(self.pos[item], mx)
            self.pos[item]=matrixmul(self.pos[item], my)
            self.pos[item]=matrixmul(self.pos[item], mz)
            
            self.pos[item]=matrixmul(self.pos[item], ms)
            
    def projection_cal(self):
        self.pro_pos=[]
        self.trans_pos=[]
        for pos in self.pos:
            pos = (pos[0], pos[1], pos[2]+3)
            self.trans_pos.append(pos)
            self.pro_pos.append(project(pos))
        
    def draw(self, surface):
        _poses = []
        n = cross_product(self.trans_pos)
        if (n[0]*(self.trans_pos[0][0]-camera.x)+n[1]*(self.trans_pos[0][1]-camera.y)+n[2]*(self.trans_pos[0][2]-camera.y))>0:
            color = max(0,min(255,light(n)*255))
            for pos in self.pro_pos:
                _pos = ((pos[0]+1)*0.5*screen[0], (pos[1]+1)*0.5*screen[1], pos[2])
                _poses.append(_pos)
    
            pygame.draw.polygon(surface, (color, color, color), ((_poses[0][0],_poses[0][1]),(_poses[1][0],_poses[1][1]),(_poses[2][0],_poses[2][1]),(_poses[3][0],_poses[3][1])))

            pygame.draw.line(surface, (0,0,0), (_poses[0][0],_poses[0][1]), (_poses[1][0],_poses[1][1]), 2)
            pygame.draw.line(surface, (0,0,0), (_poses[1][0],_poses[1][1]), (_poses[2][0],_poses[2][1]), 2)
            pygame.draw.line(surface, (0,0,0), (_poses[2][0],_poses[2][1]), (_poses[3][0],_poses[3][1]), 2)
            pygame.draw.line(surface, (0,0,0), (_poses[3][0],_poses[3][1]), (_poses[0][0],_poses[0][1]), 2)
            # for pos in _poses:
                # pygame.draw.rect(surface, (255,0,0), (pos[0],pos[1],2,2))
                
class object():
    def __init__(self, faces, verts):
        self.faces = []
        for face in faces:
            if mode=="sq":
                self.faces.append(square((verts[int(face[0])],verts[int(face[1])],verts[int(face[2])],verts[int(face[3])])))
            if mode=="tri":
                self.faces.append(triangle((verts[int(face[0])],verts[int(face[1])],verts[int(face[2])])))
        
    def update(self, rx=0, ry=0, rz=0, sx=0, sy=0, sz=0):
        for face in self.faces:
            face.update(rx, ry, rz, sx, sy, sz)
            
    def projection_cal(self):
        for face in self.faces:
            face.projection_cal()
        
    def draw(self, surface):
        if mode=="sq":
            self.faces.sort(key=lambda face: 1/(face.pro_pos[0][2]+face.pro_pos[1][2]+face.pro_pos[2][2]+face.pro_pos[3][2])/4)
        elif mode=="tri":
            self.faces.sort(key=lambda face: 1/(face.pro_pos[0][2]+face.pro_pos[1][2]+face.pro_pos[2][2])/3)
        
        
        for face in self.faces:
            face.draw(surface)
            
camera=Vcamera(0,0,-3)   

verts, faces = load("teapot.obj")
obj = object(faces, verts)
             
             
window = pygame.display.set_mode((screen[0],screen[1]), flags=pygame.RESIZABLE)
surface = pygame.Surface((screen[0],screen[1]))
clock = pygame.time.Clock()
w,h = pygame.display.get_window_size()
xA=0.01
yA=0.01
zA=0
s = 0.8
while(1):
    window.fill((50,50,50))
    surface.fill((55,55,55))
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            quit()
        if e.type==pygame.VIDEORESIZE:
            w,h = pygame.display.get_window_size()
           
    obj.update(xA,yA,zA,s,s,s)
    obj.projection_cal()
    obj.draw(surface)
    s=1
    window.blit(pygame.transform.scale(surface, (h,h)), (w/2-h/2,0))
    pygame.display.flip()
    clock.tick(60)
    pygame.display.set_caption(str(clock.get_fps()))