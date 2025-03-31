import numpy
import matplotlib.pyplot as plt

delta=numpy.pi/90
radius = 0.01
wirethickness=0.005
L=2*radius*numpy.pi/(numpy.pi*2/delta)
I=0.01
SCL=1

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
    r_vector = [r_vector[0],r_vector[1],r_vector[2]]
    
    X=(10**(-7))*I/(r**3)
    B_vector = X*numpy.cross(l_vector,r_vector)

    return B_vector

def dist(p0,p1):
    return numpy.sqrt((p0[0]-p1[0])**2+(p0[1]-p1[1])**2)
    
    
    

coil_pos,coil_vec = get_coil_v()
coil_pos,coil_vec = numpy.array(coil_pos),numpy.array(coil_vec)

test_r = 0.02
test_d = 0.001
z = numpy.arange(-test_r,test_r, test_d)
x = numpy.arange(-test_r, test_r, test_d)
y = numpy.zeros(x.size)

Px,Py,Pz=[],[],[]
Bx,By,Bz=[],[],[]


for _x in x:
    for _z in z:
        # exclude on the wire itself
        dist0 = dist((_x,_z),(radius,0))
        dist1 = dist((_x,_z),(-radius,0))

        # if dist0<=wirethickness or dist1<=wirethickness:
        #     continue
        v=[0,0,0]
        for i,_ in enumerate(coil_pos):
            v0 = get_B(I,coil_pos[i],coil_vec[i],[_x,0,_z])
            v[0]+=v0[0]*SCL
            v[1]+=v0[1]*SCL
            v[2]+=v0[2]*SCL
        # print(v)
        Bx.append(v[0])
        By.append(v[1])
        Bz.append(v[2])
        Px.append(_x)
        Py.append(0)
        Pz.append(_z)

Bx = numpy.array(Bx)
By = numpy.array(By)
Bz = numpy.array(Bz)
            
Px = numpy.array(Px)
Py = numpy.array(Py)
# Pz = numpy.array(Pz)

plt.style.use('dark_background')
ax = plt.figure().add_subplot()
ax.set_xlim([-test_r, test_r])
ax.set_ylim([-test_r, test_r])
# ax.set_zlim([-0.025, 0.025])

# ax.quiver(Px,Py,Pz,Bx,By,Bz)
# ax.scatter(coil_pos[:,0],coil_pos[:,1],coil_pos[:,2],color="orange")
# plt.show()

# length = numpy.sqrt(Bx**2+By**2+Bz**2) 

# Bx = 5*Bx / length
# By = 5*By / length
# Bz = 5*Bz / length

ax.quiver(Px,Pz,Bx,Bz,color="white")
ax.scatter([radius,-radius],[0,0],color="orange")

ax.set_title("B Field of A Coil")
ax.set_xlabel("X(meters)")
ax.set_ylabel("Z(meters)")
plt.gca().set_aspect('equal')
plt.show()
