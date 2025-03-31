import numpy
import matplotlib.pyplot as plt

L=1
I=0.1
SCL=1


def get_B(I,l_pos,l_vector,P):
    r_vector = [P[0]-l_pos[0],P[1]-l_pos[1],P[2]-l_pos[2]]
    r = numpy.sqrt(r_vector[0]**2+r_vector[1]**2+r_vector[2]**2)
    if r<=0.00001:
        return [0,0,0]
    r_vector = [r_vector[0],r_vector[1],r_vector[2]]
    
    X=(10**(-7))*I/(r**3)
    B_vector = X*numpy.cross(l_vector,r_vector)

    return B_vector

def dist(p0,p1):
    return numpy.sqrt((p0[0]-p1[0])**2+(p0[1]-p1[1])**2)
    
    
    


test_r = 0.02
test_d = 0.002
x = numpy.arange(-test_r, test_r, test_d)
y = numpy.arange(-test_r, test_r, test_d)
z = numpy.zeros(x.size)

Px,Py,Pz=[],[],[]
Bx,By,Bz=[],[],[]


for _x in x:
    for _y in y:
        v=[0,0,0]
        v0 = get_B(I,[0,0,0],[0,0,1],[_x,_y,0])
        
        v[0]+=v0[0]*SCL
        v[1]+=v0[1]*SCL
        v[2]+=v0[2]*SCL
        
        Bx.append(v[0])
        By.append(v[1])
        Bz.append(v[2])
        Px.append(_x)
        Py.append(_y)
        Pz.append(0)

Bx = numpy.array(Bx)
By = numpy.array(By)
Bz = numpy.array(Bz)
            
Px = numpy.array(Px)
Py = numpy.array(Py)
Pz = numpy.array(Pz)

plt.style.use('dark_background')
ax = plt.figure().add_subplot(projection='3d')

ax.set_xlim([-test_r, test_r])
ax.set_ylim([-test_r, test_r])
ax.set_zlim([-test_r, test_r])

ax.quiver(Px,Py,Pz,Bx,By,Bz,normalize=True,length=0.003)

wirez = numpy.arange(0,L,0.001)
ax.scatter(numpy.zeros(wirez.size),numpy.zeros(wirez.size),wirez,c="orange")

plt.show()

# print(Bx)
# print(By)
# ax.quiver(Px,Py,Bx,By,color="white")


# ax.set_title("B Field of A Wire")
# ax.set_xlabel("X(meters)")
# ax.set_ylabel("Y(meters)")
# plt.gca().set_aspect('equal')
# plt.show()