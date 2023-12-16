
import turtle
import time

delay = 0.01
sttime = time.time()
def factor(a):
    list = []
    for i in range(1,int(a/2+1)):
        if a%i==0:
            list.append(i)
            list.append(int(a/i)) 
            
    list.sort()
    return list
def common_bfactor(a, b):
    a_factors =  factor(a)   
    b_factors =  factor(b)   
    biggest = 1
    for i in a_factors:
        if i in b_factors and i>=biggest:
            biggest=i
    return biggest

def common_smultiple(a,b):
    bfactor = common_bfactor(a, b)
    return (a/bfactor*b*bfactor)



class fraction():
    def __init__(self, a, b):
        self.numerator = a
        self.denominator = b
        
        if self.denominator==1:
            self.type = "int"
        else:
            self.type = "fractal"
    def __getitem__(self, i):
        self.simplest_fraction()
        return [self.numerator, self.denominator][i]
    def __call__(self):
        self.simplest_fraction()
        return [self.numerator, self.denominator]
    
    
    def simplest_fraction(self):
            
        if self.numerator!=0:
            bfac = common_bfactor(abs(self.denominator), abs(self.numerator))
            self.numerator/=bfac
            self.denominator/=bfac
            if self.denominator<0:
                self.numerator*=-1
                self.denominator*=-1
            if self.denominator<0 and self.numerator<0:
                self.denominator*=-1
                self.numerator*=-1
        
def factor_print(f):
    if f[0]==0:
        print("0",end="")
    elif f[1]==1:
        print(f[0],end="")
    else:
        print(f[0],"/",f[1],end="")
        
def factor_expression(f):
    if f[0]==0:
        return "0"
    elif f[1]==1:
        return str(int(f[0]))
    else:
        
        return str("\n\n"+str(int(f[0]))+"\n---- \n"+str(int(f[1])))
        
        
        
def frac_add(a, b):
    #先通分，再加減
    cmul = common_smultiple(a[1],b[1])
    numerator = a[0]*cmul/a[1]+b[0]*cmul/b[1]
    
    denominator = cmul
    return fraction(numerator, denominator)
    
    
def frac_division(a, b):
    if b[0] == 0:
        return fraction(0,1)
    numerator = a[0]*b[1]
    denominator = a[1]*b[0]
    return fraction(numerator, denominator)
    
def frac_times(a, b):
    numerator = a[0]*b[0]
    denominator = a[1]*b[1]
    return fraction(numerator, denominator)
input_array = [[2,3,4,-5,-6],
         [6,7,-8,9,96],
         [10,11,12,13,312],
         [14,15,16,17,416]]

# input_array = [[2,1,1],
#                 [1,0,1]]

# input_array = [[1,1,-1,9],
#                 [0,1,3,3],
#                 [-1,0,-2,2]]


# input_array = [[1,-1,1,0,0,1],
#          [0,1,-1,1,0,2],
#          [0,0,1,-1,1,3],
#          [1,0,0,1,-1,4],
#          [-1,1,0,0,1,5]]


sorted(input_array, key=lambda i: abs(i[0]))






matrix = [] 


for list in input_array:
    matrix.append([])
    for i in list:
        matrix[len(matrix)-1].append(fraction(i,1))   
    
    
# matrix = [
# [fraction(2,1),fraction(3,1),fraction(4,1),fraction(-5,1),fraction(-6,1)],
# [fraction(6,1),fraction(7,1),fraction(-8,1),fraction(9,1),fraction(96,1)],
# [fraction(10,1),fraction(11,1),fraction(12,1),fraction(13,1),fraction(312,1)],
# [fraction(14,1),fraction(15,1),fraction(16,1),fraction(17,1),fraction(416,1)]
# ] 


def printm(m):
  for line in m:
    print("|", end=" ")
    for num in line:
      factor_print(num)
      print(";", end="")
    print("|")

def add(m1, m2):
  newm=[]
  o=0
  for i in m1:
    newm.append(frac_add(i, m2[o]))
    o+=1
  return newm  
  
  
def times(m, a):
  newm=[]
  for i in m:
    newm.append(frac_times(i,a))
  return newm  
  
def swap(a,b,m):
  temp = m[a]
  m[a]=m[b]
  m[b]=temp


def checkifdone(m):
  for i in range(len(m)):
    if i==0: 
      continue
    if i==1:
      if m[i][0].numerator!=0:
        return False
    for j in range(i):
      if m[i][j].numerator!=0:
        return False
        
  return True

def checkifdone1(m):
  for i in range(len(m)-1):
    for j in range(i+1,len(m[0])-1):
        if m[i][j][0]!=0:
            return False
  return True

def simpler(list):
    fracs0 = []
    fracs1 = []
    for i in list:
        if i[0]:
            fracs0.append(i)   
            if i[1]!=0:
                fracs1.append(i)   
    if len(fracs0)>1:
        nbfac = common_bfactor(abs(fracs0[0][0]),abs(fracs0[1][0]))
        for i in range(2,len(fracs0)):
            nbfac = common_bfactor(nbfac, abs(fracs0[i][0]))
    else:
        nbfac = 1
        
    if len(fracs0)>1:
        dbfac = common_bfactor(abs(fracs1[0][1]),abs(fracs1[1][1]))
        dsmul = common_smultiple(abs(fracs1[0][1]),abs(fracs1[1][1]))
        for i in range(2,len(fracs1)):
            dbfac = common_bfactor(dbfac, abs(fracs1[i][1]))
            dsmul = common_smultiple(dsmul, abs(fracs1[i][1]))
    else:
        dbfac = 1
        dsmul = 1
        
    for i in range(len(list)):
        list[i]=frac_times(list[i], fraction(dbfac, nbfac))

t = turtle.Turtle()
t.penup()
t.hideturtle()
turtle.tracer(0)
def draw(t, m, line_a=None, line_b=None):
    size = 100
    t.clear()
    t.sety(-size)
    for line in range(len(m)):
        t.setx(-size*len(m[0])/2)
        for i in m[len(m)-line-1]:
            if line_b == len(m)-line-1 and line_a==len(m)-line-1:
                t.color('purple')
                t.write(factor_expression(i), font=("Arial", 15, "normal"), align = "right")
            elif line_b==len(m)-line-1:
                t.color('blue')
                t.write(factor_expression(i), font=("Arial", 15, "normal"), align = "right")
            elif line_a==len(m)-line-1:
                t.color('red')
                t.write(factor_expression(i), font=("Arial", 15, "normal"), align = "right")    
            else:
                t.color('black')
                t.write(factor_expression(i), font=("Arial", 15, "normal"), align = "right")
            t.setx(t.xcor()+95)
            
            
            
        t.sety(t.ycor()+size)
    turtle.update()
    # time.sleep(1)
   
def elimination(m):
    while(not checkifdone(m)):
        
        for i in range(len(m)):
            # sorted(m, key=lambda x: abs(x[i].denominator))
            simpler(m[i])
            if int(m[i][i][0])==0:
                for j in range(len(m)):
                    if int(m[j][i][0])!=0:
                        swap(i,j,m)
            for j in range(i+1, len(m)): 
                draw(t,matrix,i,j)
                m[j]=add(m[j],times(m[i],frac_times(fraction(-1,1),frac_division(m[j][i],m[i][i]))))
                time.sleep(delay)

            
    while(not checkifdone1(m)):
        for i in range(len(m)):
            

            simpler(m[len(m)-i-1])
            for j in range(0,len(m)-i-1):
                draw(t,m, len(m)-i-1, j)
                m[j]=add(m[j],times(m[len(m)-i-1], frac_times(fraction(-1,1),frac_division(m[j][len(m)-i-1],m[len(m)-i-1][len(m)-i-1]))))
                time.sleep(delay)
    for i in range(len(m)):
        if i==len(m)-1:
            for o in range(len(m)):
                m[o][len(m[o])-1]=frac_division(m[o][len(m[o])-1], m[o][o])
                m[o][o]=frac_division(m[o][o], m[o][o])
elimination(matrix)
draw(t,matrix)
turtle.update()
entime = time.time()

print(entime-sttime)

turtle.done()