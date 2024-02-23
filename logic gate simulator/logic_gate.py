import pygame
import os


#dev log:
#change the searchihng algrithum
flags = pygame.RESIZABLE|pygame.DOUBLEBUF
pygame.init()
win = pygame.display.set_mode((500,500), flags=flags)
# map_surface = pygame.Surface((20000,20000))
w,h = pygame.display.get_window_size()
# font = pygame.font.SysFont("PMingLiU", 20)
# bfont = pygame.font.SysFont("PMingLiU", 30)

font = pygame.font.SysFont(None, 20)
bfont = pygame.font.SysFont(None, 30)


gate_size = 100
zoom = 1

mode = "init"

gates_type = ["Leave", "source","peak time source","peak time source 2","peak detector","time source","not gate", "or gate", "and gate","xor gate","nand gate", "LED", "node"]
interectable = ["source"]



view_point = [0,0]
speed = 20

mouse_pos = []
original_pos = []

delta_time = 5

clock = pygame.time.Clock()

all_id = []
node_drawm = 0
line_drawn = 0

name = "NEWEST.txt"


def save(all_gate):
    with open("saving.txt", mode="w+") as f:
        for gate in all_gate:
            f.write(gate.name+" "+str(gate.id)+" "+str(gate.x)+" "+str(gate.y)+" ")
            for i in range(gate.connectectors):
                f.write(str(gate.connected[i]))
                f.write(" ")
            if gate.name == "time_source":
                f.write(str(gate.T)+" ")
            f.write("\n")
            
def openx(name, map):
    with open(name, mode="r+") as f:
        for gate in f.readlines():
            gate = gate.split(" ")
            x,y = float(gate[2]),float(gate[3])
            if "\n" in gate:
                gate.remove("\n")
            print(gate)
            if gate[0]=="or_gate":
                
                if len(gate)==6:
                    if gate[4]!="None" and gate[5]!="None":
                        map.create_or_gate(x, y,id=int(gate[1]),a=int(gate[4]),b=int(gate[5]))
                    elif gate[4]!="None" and gate[5]=="None":
                        map.create_or_gate(x, y,id=int(gate[1]),a=int(gate[4]))
                    elif gate[4]=="None" and gate[5]!="None":
                        map.create_or_gate(x, y,id=int(gate[1]),b=int(gate[5]))
                    elif gate[4]=="None" and gate[5]=="None":
                        map.create_or_gate(x, y,id=int(gate[1]))
                else:
                    map.create_or_gate(x, y,id=int(gate[1]))
            if gate[0]=="and_gate":
                if len(gate)==6:
                    if gate[4]!="None" and gate[5]!="None":
                        map.create_and_gate(x, y,id=int(gate[1]),a=int(gate[4]),b=int(gate[5]))
                    elif gate[4]!="None" and gate[5]=="None":
                        map.create_and_gate(x, y,id=int(gate[1]),a=int(gate[4]))
                    elif gate[4]=="None" and gate[5]!="None":
                        map.create_and_gate(x, y,id=int(gate[1]),b=int(gate[5]))
                    elif gate[4]=="None" and gate[5]=="None":
                        map.create_and_gate(x, y,id=int(gate[1]))
                
                
                else:
                    map.create_and_gate(x, y,id=int(gate[1]))
            if gate[0]=="source":
                map.create_source(x,y,id=int(gate[1]))
                
            if gate[0]=="time_source":
                if len(gate)>4:
                    map.create_time_source(x,y,id=int(gate[1]),T=int(gate[4])) 
                else:
                    map.create_time_source(x,y,id=int(gate[1]))
            if gate[0]=="peak_time_source":
                if len(gate)>4:
                    map.create_peak_time_source(x,y,id=int(gate[1]),T=int(gate[4])) 
                else:
                    map.create_peak_time_source(x,y,id=int(gate[1]))  
            if gate[0]=="peak_detector":
                if len(gate)>4:
                    if gate[4]!="None":
                        map.create_peak_detector(x,y,id=int(gate[1]),a=int(gate[4])) 
                    else:
                        map.create_peak_detector(x,y,id=int(gate[1]))
                else:
                    map.create_peak_detector(x,y,id=int(gate[1]))   
                    
                    
            if gate[0]=="peak_time_source2":
                if len(gate)>4:
                    map.create_peak_time_source2(x,y,id=int(gate[1]),T=int(gate[4]))
                else:
                    map.create_peak_time_source2(x,y,id=int(gate[1]))
                    
                    
            if gate[0]=="LED":
                if len(gate)==5:
                    if gate[4]!="None":
                        map.create_LED(x,y,id=int(gate[1]),a=int(gate[4]))
                    else:
                        map.create_LED(x,y,id=int(gate[1]))
                else:
                    map.create_LED(x,y,id=int(gate[1]))
                    
                    
                    
            if gate[0]=="xor_gate":
                if len(gate)==6:
                    if gate[4]!="None" and gate[5]!="None":
                        map.create_xor_gate(x, y,id=int(gate[1]),a=int(gate[4]),b=int(gate[5]))
                    elif gate[4]!="None" and gate[5]=="None":
                        map.create_xor_gate(x, y,id=int(gate[1]),a=int(gate[4]))
                    elif gate[4]=="None" and gate[5]!="None":
                        map.create_xor_gate(x, y,id=int(gate[1]),b=int(gate[5]))
                    elif gate[4]=="None" and gate[5]=="None":
                        map.create_xor_gate(x, y,id=int(gate[1]))
                else:
                    map.create_xor_gate(x, y,id=int(gate[1]))
                    
            if gate[0]=="nand_gate":
                if len(gate)==6:
                    if gate[4]!="None" and gate[5]!="None":
                        map.create_nand_gate(x, y,id=int(gate[1]),a=int(gate[4]),b=int(gate[5]))
                    elif gate[4]!="None" and gate[5]=="None":
                        map.create_nand_gate(x, y,id=int(gate[1]),a=int(gate[4]))
                    elif gate[4]=="None" and gate[5]!="None":
                        map.create_nand_gate(x, y,id=int(gate[1]),b=int(gate[5]))
                    elif gate[4]=="None" and gate[5]=="None":
                        map.create_nand_gate(x, y,id=int(gate[1]))
                else:
                    map.create_nand_gate(x, y,id=int(gate[1]))
                    
            if gate[0]=="not_gate":
                if len(gate)==5:
                    if gate[4]!="None":
                        map.create_not_gate(x,y,id=int(gate[1]),a=int(gate[4]))
                    else:
                        map.create_not_gate(x,y,id=int(gate[1]))
                else:
                    map.create_not_gate(x,y,id=int(gate[1])) 
                    
            if gate[0]=="node":
                if len(gate)==5:
                    if gate[4]!="None":
                        map.create_node(x,y,id=int(gate[1]),a=int(gate[4]))
                    else:
                        map.create_node(x,y,id=int(gate[1]))
                else:
                    map.create_node(x,y,id=int(gate[1])) 
                           
    map0.update()

def check_for_id_in_list0(a,all):
    a_index = None
    a_value = None
    try:
        a_index = all_id.index(a)
    except:
        pass
    
    try:
        if a_index!=None:
            a_value = all[a_index].get_value()
    except:
        pass    
    
    
    return (a_index, a_value)
    

def check_for_id_in_list(a,b,all):
    a_index = None
    b_index = None
    a_value = None
    b_value = None
    try:
        _id = all_id.index(a)
        a_index=_id
        a_value=all[_id].get_value()
    except:
        pass
    
    try:
        _id = all_id.index(b)
        b_index=_id
        b_value=all[_id].get_value()
    except:
        pass
    
    return (a_index,a_value,b_index,b_value)


def controll():
    global mode, mouse_pos, original_pos, gate_size, zoom, action, w, h
    action = None
    key = pygame.key.get_pressed()
    
    map0.get_mouse_pos()
    
    for event in pygame.event.get():
        if event.type==pygame.VIDEORESIZE:
            w,h = pygame.display.get_window_size()
            action="resize"
        if event.type==pygame.QUIT:
            quit()
        if event.type==pygame.KEYDOWN:
            # if event.key==pygame.K_ESCAPE:
            #     quit()
            if event.key==pygame.K_SPACE:
                map0.check_all_value()
                action="space"
            if event.key==pygame.K_q:
                mode = "interect"
                action="q"
            if event.key==pygame.K_e:
                mode = "build" 
                action="e"
            if event.key==pygame.K_p:
                save(map0.all_gate)
                action="p"
                
        if event.type == pygame.MOUSEWHEEL:
            map0.get_mouse_pos()
            if (event.y==1 or key[pygame.K_UP]) and zoom+0.1<=10:
                if mode!="init":
                    zoriginal_pos = (map0.mmx,map0.mmy)
                    zoriginal_pos0 = (map0.mx,map0.my)
                    zoom+=0.1
                    map0.get_mouse_pos()
                    view_point[0] = zoriginal_pos[0]-zoriginal_pos0[0]/zoom
                    view_point[1] = zoriginal_pos[1]-zoriginal_pos0[1]/zoom
                action="mousewheelup"
                
            elif (event.y==-1 or key[pygame.K_DOWN]) and zoom-0.1>=0.05:
                if mode!="init":

                    zoriginal_pos = (map0.mmx,map0.mmy)
                    zoriginal_pos0 = (map0.mx,map0.my)
                    zoom-=0.1
                    map0.get_mouse_pos()
                    view_point[0] = zoriginal_pos[0]-zoriginal_pos0[0]/zoom
                    view_point[1] = zoriginal_pos[1]-zoriginal_pos0[1]/zoom
                action="mousewheeldown"
                
    if key[pygame.K_w]:
        view_point[1]-=speed*(zoom**-1.5)
    if key[pygame.K_s]:
        view_point[1]+=speed*(zoom**-1.5)
    if key[pygame.K_a]:
        view_point[0]-=speed*(zoom**-1.5)
    if key[pygame.K_d]:
        view_point[0]+=speed*(zoom**-1.5)
        
    if pygame.mouse.get_pressed()[1]:
        mouse_pos.append(pygame.mouse.get_pos())
        original_pos.append([view_point[0],view_point[1]])
        view_point[0]=-(mouse_pos[len(mouse_pos)-1][0]-mouse_pos[0][0])*(zoom**-1.5)+original_pos[0][0]
        view_point[1]=-(mouse_pos[len(mouse_pos)-1][1]-mouse_pos[0][1])*(zoom**-1.5)+original_pos[0][1]
    else:
        mouse_pos=[]
        original_pos=[]
        
    return action
def draw_option_box(_options, mode="normal", _width=None):
    max = [-1, ""]
    for t in _options:
        if len(str(t))>max[0]:
            max = [len(str(t)), t]
            
    delta_h = font.render(str(max[1]), True, (0,0,0)).get_height()*1.5
    
    
    height = 20+delta_h*(len(_options))
    if _width==None:
        width = font.render(str(max[1]), True, (0,0,0)).get_width()+20
    else:
        width = _width
        
        
    option_box = pygame.Surface((width+20,height))
    option_box.fill((200,200,200))
    options = []
    
    for option in range(len(_options)):
        if mode=="normal":
            rect_value = (10,10+delta_h*option, width, delta_h)
            options.append([rect_value, _options[option]])
            pygame.draw.rect(option_box, (150,150,150),rect_value)
            t_r = font.render(str(_options[option]), True, (0,0,0))
            
            option_box.blit(t_r, (10+width/2-t_r.get_width()/2,12.5+delta_h*option))
            
            
            
            
        if mode=="open":
            rect_value = (10,10+delta_h*option, width, delta_h)
            options.append([rect_value, _options[option]])
            pygame.draw.rect(option_box, (150,150,150),rect_value)
            t_r = font.render(str(_options[option]), True, (0,0,0))
            
            if not(".txt" in _options[option] or not("." in _options[option]) or _options[option]=="...back" or _options[option]=="...back to original pos"):
                t_r.set_alpha(50)
                
            option_box.blit(t_r, (10+width/2-t_r.get_width()/2,12.5+delta_h*option))
        
        
        
    return [options, option_box]
                                
def check_for_collide(_mx,_my, rect):
    tmp = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
    return pygame.Rect.collidepoint(tmp, (_mx,_my))
                                
def check_for_next_empty(all_id):
    i = 0
    while(i in all_id):
        i+=1
    return i

def draw_info_box(gate):
    w, h = pygame.display.get_window_size()
    
    rs = [font.render("id: "+str(gate.id), True, (0,0,0)),
    font.render("type: "+str(gate.name), True, (0,0,0)),
    font.render("at "+str((round(gate.x,2), round(gate.y,2))), True, (0,0,0)),
    font.render("value"+str(gate.value), True, (0,0,0))]
    bigx = 0
    bigy = len(rs)*rs[0].get_height()*3
    for r in rs:
        if r.get_width()>bigx:
            bigx=r.get_width()*1.5
            
    sur = pygame.Surface((bigx, bigy))
    sur.fill((200,200,200))
    i = 0
    for r in rs:
        sur.blit(r, (10, (1+i)*rs[0].get_height()*1.5))
        i+=1
        
    sur = pygame.transform.scale(sur, (bigx*h*0.25/bigy, h*0.25))
        
    return sur


           
class gate():
    def __init__(self,environment,id,x=0,y=0):
        self.value = None
        self.x, self.y = x, y
        self.Surface = pygame.Surface((gate_size,gate_size))
        self.Surface.fill((255,255,255))
        self.blit_sur = self.Surface.copy()
        self.rect = pygame.Rect(self.x, self.y, gate_size, gate_size)
        self.connectectors = 0
        self.connected = []
        self.environment = environment
        self.id = id
        self.out_pos = (gate_size/2,0)
        self.option = ["Leave", "Destroy"]
        self.out_connection = False
        
    def update_detection_box(self):
        self.rect = pygame.Rect(self.x, self.y, gate_size, gate_size)
        # self.Surface = pygame.Surface((gate_size,gate_size))
        # self.Surface.fill((255,255,255))
        
    def update(self):
        pass
    
    def get_value(self):
        return self.value
    def touch_action(self):
        pass
    
    
    
    
class source(gate):
    def __init__(self,x,y,environment,id,value=False):
        super().__init__(environment,id,x,y)
        self.value = value
        self.name = "source"
        self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
        self.out_connection = True
        
    def update(self):
        if (self.x-view_point[0])*zoom<w and (self.x-view_point[0])*zoom>-gate_size*zoom and (self.y-view_point[1])*zoom<h and (self.y-view_point[1])*zoom>-gate_size*zoom:

            if self.value:
                self.Surface.fill((150,255,150))
                self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
            else:
                self.Surface.fill((255,150,150))
                self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
            
    def touch_action(self):
        if self.value:
            self.value=False
        else:
            self.value=True
            
class time_source(gate):
    def __init__(self,x,y,environment,id,T=5,value=False):
        super().__init__(environment,id,x,y)
        self.value = value
        self.name = "time_source"
        self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
        self.out_connection = True
        self.ini_clock=self.environment.global_tick
        self.last_on = 0
        self.T = T
        self.on_time=T*0.5
        
        
        
    def update(self):

            
        if self.environment.global_tick-self.last_on<=self.on_time:
            self.value = True
        else:
            self.value = False
            if self.environment.global_tick-self.last_on>=self.T:
                self.last_on=self.environment.global_tick
                
        if (self.x-view_point[0])*zoom<w and (self.x-view_point[0])*zoom>-gate_size*zoom and (self.y-view_point[1])*zoom<h and (self.y-view_point[1])*zoom>-gate_size*zoom:
            if self.value:
                self.Surface.fill((150,255,150))
                self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
            else:
                self.Surface.fill((255,150,150))
                self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
 
class peak_time_source(gate):
    def __init__(self,x,y,environment,id,T=5,value=False):
        super().__init__(environment,id,x,y)
        self.value = value
        self.name = "peak_time_source"
        self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
        self.out_connection = True
        self.ini_clock=self.environment.global_tick
        self.last_on = 0
        self.T = T
        self.on_time=T*0.1
    def update(self):
        if self.environment.global_tick-self.last_on<=self.on_time:
            self.value = True
        else:
            self.value = False
            if self.environment.global_tick-self.last_on>=self.T:
                self.last_on=self.environment.global_tick

        if (self.x-view_point[0])*zoom<w and (self.x-view_point[0])*zoom>-gate_size*zoom and (self.y-view_point[1])*zoom<h and (self.y-view_point[1])*zoom>-gate_size*zoom:
            if self.value:
                self.Surface.fill((150,255,150))
                self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
            else:
                self.Surface.fill((255,150,150))
                self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))

class peak_time_source2(gate):
    def __init__(self,x,y,environment,id,T=5,value=False):
        super().__init__(environment,id,x,y)
        self.value = value
        self.name = "peak_time_source2"
        self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
        self.out_connection = True
        self.ini_clock=self.environment.global_tick
        self.last_on = 0
        self.T = T
        self.on_time=T*0.1
    def update(self):
        if self.environment.global_tick-self.last_on>=self.T/2-self.on_time and self.environment.global_tick-self.last_on<self.T/2:
            self.value = True
        else:
            self.value = False
            if self.environment.global_tick-self.last_on>=self.T:
                self.last_on=self.environment.global_tick
        if (self.x-view_point[0])*zoom<w and (self.x-view_point[0])*zoom>-gate_size*zoom and (self.y-view_point[1])*zoom<h and (self.y-view_point[1])*zoom>-gate_size*zoom:
            if self.value:
                self.Surface.fill((150,255,150))
                self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
            else:
                self.Surface.fill((255,150,150))
                self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))

class peak_detector(gate):
    def __init__(self,x,y,environment,id,a,T=5,value=False):
        super().__init__(environment,id,x,y)
        self.value = value
        self.name = "peak_detector"
        self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
        self.out_connection = True
        self.ini_clock=self.environment.global_tick
        self.last_on = [self.environment.global_tick]
        self.T = T
        self.on_time=T*0.1
        
        self.input_pos = [(gate_size/2,gate_size)]
        self.option.append("change node")

        
        self.connectectors=1
        if a!=None:
            self.connected = [a]
        else:
            self.connected = [None]
        
    def update(self):
        temp = check_for_id_in_list0(self.connected[0],self.environment.all_gate)
        if temp!=None:

            if temp[1] and self.environment.global_tick-self.last_on[0]<=self.on_time:
                self.last_on.append(self.environment.global_tick)
                self.value = True
            elif temp[1] and self.environment.global_tick-self.last_on[0]>=self.on_time:
                self.value = False
            else:
                self.last_on=[self.environment.global_tick]
                self.value = False

        else:
            self.last_on=[self.environment.global_tick]
            self.value = False
            
            
        if (self.x-view_point[0])*zoom<w and (self.x-view_point[0])*zoom>-gate_size*zoom and (self.y-view_point[1])*zoom<h and (self.y-view_point[1])*zoom>-gate_size*zoom:
            if self.value:
                self.Surface.fill((150,255,150))
                self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
            else:
                self.Surface.fill((255,150,150))
                self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))


      
class LED(gate):
    def __init__(self,x,y,environment,id,a,value=False):
        super().__init__(environment,id,x,y)
        self.connectectors=1
        self.value = value
        self.name = "LED"
        self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
        self.color=(150,150,150)
        self.input_pos = [(gate_size/2,gate_size)]
        self.option.append("change node")
        if a!=None:
            self.connected = [a]
        else:
            self.connected = [None]
            
            
    def update(self):
        if self.connected[0]!=None:
            self.value = check_for_id_in_list0(self.connected[0], self.environment.all_gate)[1]
        else:
            self.value=False
        if (self.x-view_point[0])*zoom<w and (self.x-view_point[0])*zoom>-gate_size*zoom and (self.y-view_point[1])*zoom<h and (self.y-view_point[1])*zoom>-gate_size*zoom:
            if self.value:
                self.Surface.fill((150,255,150))
                self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
            else:
                self.Surface.fill((255,150,150))
                self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
        
class and_gate(gate):
    def __init__(self,x,y,environment,id,a=None,b=None):
        super().__init__(environment,id,x,y)
        self.connectectors = 2
        self.name = "and_gate"
        self.Surface.blit(font.render(self.name, True, (0,0,0)), (0,gate_size/2))
        
        self.input_pos = [(gate_size/3,gate_size), (gate_size/3*2,gate_size)]
        self.color = (255,0,0)
        self.option.append("change node")
        self.out_connection = True
        
          
        self.connected = [a,b]
        
    def update(self):
        temp = check_for_id_in_list(self.connected[0],self.connected[1],self.environment.all_gate)
        if (self.x-view_point[0])*zoom<w and (self.x-view_point[0])*zoom>-gate_size*zoom and (self.y-view_point[1])*zoom<h and (self.y-view_point[1])*zoom>-gate_size*zoom:
            self.Surface.fill((255,255,255))
            self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
        if temp[0]==None:
            self.value = False
        elif temp[2]==None:
            self.value = False
        elif temp[1] and temp[3]:
            self.value = True
        else:
            self.value = False
           
class or_gate(gate):
    def __init__(self,x,y,environment,id,a=None,b=None):
        super().__init__(environment,id,x,y)
        self.connectectors = 2
        self.name = "or_gate"
        self.Surface.blit(font.render(self.name, True, (0,0,0)), (0,gate_size/2))
        
        self.input_pos = [(gate_size/3,gate_size), (gate_size/3*2,gate_size)]
        self.color = (0,255,0)
        self.option.append("change node")
        self.out_connection = True
        
        self.connected = [a,b]
        
    def update(self):
        temp = check_for_id_in_list(self.connected[0],self.connected[1],self.environment.all_gate)
        if (self.x-view_point[0])*zoom<w and (self.x-view_point[0])*zoom>-gate_size*zoom and (self.y-view_point[1])*zoom<h and (self.y-view_point[1])*zoom>-gate_size*zoom:
            self.Surface.fill((255,255,255))
            self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
        if temp[1] or temp[3]:
            self.value = True
        else:
            self.value = False

class xor_gate(gate):
    def __init__(self,x,y,environment,id,a=None,b=None):
        super().__init__(environment,id,x,y)
        self.connectectors = 2
        self.name = "xor_gate"
        self.Surface.blit(font.render(self.name, True, (0,0,0)), (0,gate_size/2))
        
        self.input_pos = [(gate_size/3,gate_size), (gate_size/3*2,gate_size)]
        self.color = (150,150,255)
        self.option.append("change node")
        self.out_connection = True
        
        
        self.connected = [a,b]
        
    def update(self):
        temp = check_for_id_in_list(self.connected[0],self.connected[1],self.environment.all_gate)
        if (self.x-view_point[0])*zoom<w and (self.x-view_point[0])*zoom>-gate_size*zoom and (self.y-view_point[1])*zoom<h and (self.y-view_point[1])*zoom>-gate_size*zoom:
            self.Surface.fill((255,255,255))
            self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
        if temp[0]==None:
            self.value = False
        elif temp[2]==None:
            self.value = False
        elif temp[1] and temp[3]:
            self.value = False
        elif temp[1] or temp[3]:
            self.value = True
        else:
            self.value = False
            
class nand_gate(gate):
    def __init__(self,x,y,environment,id,a=None,b=None):
        super().__init__(environment,id,x,y)
        self.connectectors = 2
        self.name = "nand_gate"
        self.Surface.blit(font.render(self.name, True, (0,0,0)), (0,gate_size/2))
        
        self.input_pos = [(gate_size/3,gate_size), (gate_size/3*2,gate_size)]
        self.color = (150,255,150)
        self.option.append("change node")
        self.out_connection = True
        
        
        self.connected = [a,b]
        
    def update(self):
        temp = check_for_id_in_list(self.connected[0],self.connected[1],self.environment.all_gate)
        if (self.x-view_point[0])*zoom<w and (self.x-view_point[0])*zoom>-gate_size*zoom and (self.y-view_point[1])*zoom<h and (self.y-view_point[1])*zoom>-gate_size*zoom:
            self.Surface.fill((255,255,255))
            self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
        if temp[0]==None:
            self.value = False
        elif temp[2]==None:
            self.value = False
        elif temp[1] and temp[3]:
            self.value = False
        elif temp[1] or temp[3]:
            self.value = True
        else:
            self.value = True
            
class not_gate(gate):
    def __init__(self,x,y,environment,id,a=None):
        super().__init__(environment,id,x,y)
        self.connectectors = 1
        self.name = "not_gate"
        self.Surface.blit(font.render(self.name, True, (0,0,0)), (0,gate_size/2))
        
        self.input_pos = [(gate_size/2,gate_size)]
        self.color = (150,150,150)
        self.option.append("change node")
        self.out_connection = True
        
        self.connected = [a]
        
    def update(self):
        temp = check_for_id_in_list0(self.connected[0],self.environment.all_gate)
        if (self.x-view_point[0])*zoom<w and (self.x-view_point[0])*zoom>-gate_size*zoom and (self.y-view_point[1])*zoom<h and (self.y-view_point[1])*zoom>-gate_size*zoom:
            self.Surface.fill((255,255,255))
            self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
        if temp[0]==None:
            self.value = False
        elif temp[1]:
            self.value = False
        else:
            self.value = True

class node(gate):
    def __init__(self,x,y,environment,id,a=None):
        super().__init__(environment,id,x,y)
        self.connectectors = 1
        self.name = "node"
        self.Surface.blit(font.render(self.name, True, (0,0,0)), (0,gate_size/2))
        
        self.input_pos = [(gate_size/2,gate_size)]
        self.color = (150,150,150)
        self.option.append("change node")
        self.out_connection = True
        
        self.connected = [a]
        
    def update(self):
        temp = check_for_id_in_list0(self.connected[0],self.environment.all_gate)
        
        if (self.x-view_point[0])*zoom<w and (self.x-view_point[0])*zoom>-gate_size*zoom and (self.y-view_point[1])*zoom<h and (self.y-view_point[1])*zoom>-gate_size*zoom:
            self.Surface.fill((255,255,255))
            self.Surface.blit(font.render(self.name+str(self.id), True, (0,0,0)), (0,gate_size/2))
        
        if temp[0]==None:
            self.value = False
        elif temp[1]:
            self.value = True
        else:
            self.value = False


class environment():
    def __init__(self):
        self.select_rect=None
        self.all_gate = []
        self.global_id = 0
        self.win=win
        self.group_selected = []
        self.mouse_pos=[]
        self.original_pos=[]
        self.global_tick=0
        self.indication = None
        
        
        self.mx, self.my = pygame.mouse.get_pos()
        self.mmx, self.mmy = (self.mx/zoom)+view_point[0]*zoom, (self.my/zoom)+view_point[1]*zoom
        self.buttons = (pygame.mouse.get_pressed())
        
    def check_all_value(self):
        print("----------------")
        self.get_mouse_pos()
        print("mouse_pos:"+str((self.mmx, self.mmy)))
        for gate in self.all_gate:
            
            print("type:"+str(type(gate))+" id: "+str(gate.id)+" value: "+str(gate.get_value())+" pos: ("+str(gate.x)+","+str(gate.y)+")")
            if str(type(gate))=="<class '__main__.and_gate'>" or str(type(gate))=="<class '__main__.or_gate'>":
                print(gate.connected)
                
    def get_mouse_pos(self):
        
        self.mx, self.my = pygame.mouse.get_pos()
        # print(zoom)
        self.mmx, self.mmy = (self.mx/zoom)+view_point[0], (self.my/zoom)+view_point[1]
        
        self.buttons = pygame.mouse.get_pressed()
        
        return (self.mx, self.my, self.mmx, self.mmy,self.buttons)
        
    def controll_update(self):
        
        global mode, all_id
        
        self.get_mouse_pos()
        
        touched = 0
        key = pygame.key.get_pressed()
        
        
        
        if key[pygame.K_DELETE]:
            for _id in self.group_selected:
                self.delete(_id)
            all_id = [i.id for i in map0.all_gate]
                
        

        for gate in self.all_gate:
            if touched>0:
                break
            
            if not ((gate.x-view_point[0])*zoom<w and (gate.x-view_point[0])*zoom>-gate_size*zoom and (gate.y-view_point[1])*zoom<h and (gate.y-view_point[1])*zoom>-gate_size*zoom):
                continue
            
            
            if check_for_collide(self.mmx,self.mmy, gate.rect):
                self.indication = gate
                
                if mode=="build":
                    
                    
                    if self.buttons[0]:
                        touched+=1
                        gate.x = self.mmx-gate_size/2
                        gate.y = self.mmy-gate_size/2
                        
                        gate.update_detection_box()
                        
                    
                    
                    if self.buttons[2]:
                        
                        touched+=1
                        options, option_box = draw_option_box(gate.option)
                        ox, oy = (gate.x-view_point[0]+gate_size)*zoom, (gate.y-view_point[1])*zoom
                    
                        loop=True
                        selected=None
                        while(loop):
                            controll()
                            self.get_mouse_pos()
                            for option in options:
                                rect = pygame.Rect(ox+option[0][0],oy+option[0][1],option[0][2],option[0][3])
                                if pygame.Rect.collidepoint(rect,(self.mx,self.my)) and self.buttons[0]:
                                    loop=False
                                    selected = option[1]
                                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                                    loop=False
                                    
                            self.draw()
                            self.win.blit(option_box, (ox, oy))
                            pygame.display.update()

                        
                        print(selected)
                        
                        if selected=="Destroy":
                            self.delete(gate.id)
                            all_id = [i.id for i in map0.all_gate]
                            
                        if selected=="change node":
                            
                            tmp = gate.connected.copy()
                            tmp.append("leave")
                            options, option_box = draw_option_box(tmp)
                            ox, oy = (gate.x-view_point[0]+gate_size)*zoom+option_box.get_width(), (gate.y-view_point[1]+option_box.get_height()*0.5)*zoom
                            loop=True
                            selected=None
                            
                            while(loop):
                                controll()
                                self.get_mouse_pos()
                                highlight_node = None
                                index = 0
                                for option in options:
                                    rect = pygame.Rect(ox+option[0][0],oy+option[0][1],option[0][2],option[0][3])
                                    if pygame.Rect.collidepoint(rect,(self.mx,self.my)):
                                        if option[1]!="leave":
                                            highlight_node = [gate.id, index]
                                            if self.buttons[0]:
                                                print(index)
                                                loop=False
                                                selected = index
                                        else:
                                            if self.buttons[0]:
                                                loop=False
                                                
                                    index+=1
                                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                                    loop=False
                                    
                                self.draw(selected=highlight_node)
                                self.win.blit(option_box, (ox, oy))
                                pygame.display.update()

                                
                            big_option_box = pygame.Rect([ox,oy,option_box.get_width(),option_box.get_height()])
                            if selected!=None or selected=="leave":
                                loop=True
                                selected_node=None
                                while(loop):
                                    controll()
                                    highlight=[gate.connected[selected]]
                                    self.get_mouse_pos()
                                    for _gate in self.all_gate:
                                        if _gate.id==gate.id:
                                            continue
                                        else:
                                            if check_for_collide(self.mmx,self.mmy,_gate.rect):
                                                highlight = [_gate.id]
                                                if self.buttons[0] and not(check_for_collide(self.mx,self.my,big_option_box)):
                                                    print(_gate.id)
                                                    loop=False
                                                    selected_node=_gate.id
                                                    
                                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                                        loop=False
                                    
                                    self.win.fill((0,0,0))
                                    self.draw(highlight)
                                    pygame.display.update()

                                    
                                if selected_node!=None:
                                    sel_node_index = check_for_id_in_list0(selected_node,self.all_gate)
                                    if self.all_gate[sel_node_index[0]].out_connection:
                                        if self.all_gate[sel_node_index[0]]:
                                            gate.connected[selected]=selected_node
                                

                                

                                        
                elif mode=="selection" and gate.id in self.group_selected:
                    self.get_mouse_pos()
                    while(None in self.group_selected):
                        self.group_selected.remove(None)
                    for id in self.group_selected:
                        if check_for_id_in_list0(id, self.all_gate)[0]==None:
                            self.group_selected.remove(id)
                    
                    if self.buttons[0] and len(self.group_selected)>0:
                        mouse_pos=[]
                        touched+=1
                        _loop=True
                        all_selected_gate = [self.all_gate[check_for_id_in_list0(i, self.all_gate)[0]] for i in self.group_selected]
                        all_x = [i.x for i in all_selected_gate]
                        all_x.sort()
                        all_y = [i.y for i in all_selected_gate]
                        all_y.sort()
                        box_o_select = (abs((all_x[len(all_x)-1]-all_x[0]+gate_size))*zoom,abs(all_y[len(all_y)-1]-all_y[0]+gate_size)*zoom)
                            
                        while(_loop):
                            controll()
                            self.draw()
                            self.get_mouse_pos()
                            _loop = pygame.mouse.get_pressed()[0]
                            mouse_pos.append((self.mmx, self.mmy))
                            
                            rect = self.select_rect.copy()
                            rect.topleft=(all_x[0]+(mouse_pos[len(mouse_pos)-1][0]-mouse_pos[0][0]),all_y[0]+(mouse_pos[len(mouse_pos)-1][1]-mouse_pos[0][1]))
                            
                            sur = pygame.Surface(box_o_select)
                            
                            sur.fill((0,0,255))
                            sur.set_alpha(200)
                            
                            self.draw()
                            self.win.blit(sur, ((rect.topleft[0]-view_point[0])*zoom, (rect.topleft[1]-view_point[1])*zoom))
                            pygame.display.update()

                            
                        for _id in self.group_selected:
                            gate = self.all_gate[check_for_id_in_list0(_id, self.all_gate)[0]]
                            gate.x+=mouse_pos[len(mouse_pos)-1][0]-mouse_pos[0][0]
                            gate.y+=mouse_pos[len(mouse_pos)-1][1]-mouse_pos[0][1]
                               
                    if self.buttons[2] and len(self.group_selected)>0:
                        touched+=1
                        self.get_mouse_pos()
                        options, option_box = draw_option_box(["Leave", "Copy", "Delete"])
                        ox, oy = (gate.x-view_point[0]+gate_size)*zoom, (gate.y-view_point[1])*zoom
                        loop=True
                        selected=None
                        
                        while(loop):
                            controll()
                            self.get_mouse_pos()
                            for option in options:
                                rect = pygame.Rect(ox+option[0][0],oy+option[0][1],option[0][2],option[0][3])
                                if pygame.Rect.collidepoint(rect,(self.mx,self.my)) and self.buttons[0]:
                                    loop=False
                                    selected = option[1]
                                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                                    loop=False
                                    break
                            self.draw()
                            self.win.blit(option_box, (ox, oy))
                            pygame.display.update()

                        
                        if selected=="Delete":
                            for _id in self.group_selected:
                                self.delete(_id)
                            all_id = [i.id for i in map0.all_gate]
                        elif selected=="Copy" and len(self.group_selected)>0:
                            
                            new_id = {}
                            all_id = [i.id for i in self.all_gate]
                            
                            all_selected_gate = [self.all_gate[check_for_id_in_list0(i, self.all_gate)[0]] for i in self.group_selected]
                            all_x = [i.x for i in all_selected_gate]
                            all_x.sort()
                            all_y = [i.y for i in all_selected_gate]
                            all_y.sort()
                            offset = ((all_x[len(all_x)-1]-all_x[0]+gate_size)*1.5,(all_y[len(all_y)-1]-all_y[0])*0.1)
                            self.group_selected=[]
                            
                            for _gate in all_selected_gate:
                                index = check_for_next_empty(all_id)
                                new_id[_gate.id]=index
                                all_id.append(index)
                                
                                    
                            for _gate in all_selected_gate:
                                self.group_selected.append(new_id[_gate.id])
                                if _gate.name=="or_gate":
                                    if (_gate.connected[0]!=None and _gate.connected[1]!=None) and (_gate.connected[0] in new_id and _gate.connected[1] in new_id):
                                        self.create_or_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],a=new_id[_gate.connected[0]],b=new_id[_gate.connected[1]])
                                    elif (_gate.connected[0]==None and _gate.connected[1]!=None) and (not(_gate.connected[0] in new_id) and _gate.connected[1] in new_id):
                                        self.create_or_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],b=new_id[_gate.connected[1]])
                                    elif _gate.connected[0]!=None and _gate.connected[1]==None and (_gate.connected[0] in new_id and not(_gate.connected[1] in new_id)):
                                        self.create_or_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],a=new_id[_gate.connected[0]])
                                    else:
                                        self.create_or_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id])
                                
                                
                                if _gate.name=="and_gate":
                                    if (_gate.connected[0]!=None and _gate.connected[1]!=None) and (_gate.connected[0] in new_id and _gate.connected[1] in new_id):
                                        self.create_and_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],a=new_id[_gate.connected[0]],b=new_id[_gate.connected[1]])
                                    elif (_gate.connected[0]==None and _gate.connected[1]!=None) and (not(_gate.connected[0] in new_id) and _gate.connected[1] in new_id):
                                        self.create_and_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],b=new_id[_gate.connected[1]])
                                    elif _gate.connected[0]!=None and _gate.connected[1]==None and (_gate.connected[0] in new_id and not(_gate.connected[1] in new_id)):
                                        self.create_and_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],a=new_id[_gate.connected[0]])
                                    else:
                                        self.create_and_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id])
                                
                                if _gate.name=="source":
                                    self.create_source(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id])

                                if _gate.name=="LED":
                                        if _gate.connected[0]!=None and _gate.connected[0] in new_id:
                                            self.create_LED(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],a=new_id[_gate.connected[0]])
                                        else:
                                            self.create_LED(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id])
                                if _gate.name=="xor_gate":
                                    if (_gate.connected[0]!=None and _gate.connected[1]!=None) and (_gate.connected[0] in new_id and _gate.connected[1] in new_id):
                                        self.create_xor_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],a=new_id[_gate.connected[0]],b=new_id[_gate.connected[1]])
                                    elif (_gate.connected[0]==None and _gate.connected[1]!=None) and (not(_gate.connected[0] in new_id) and _gate.connected[1] in new_id):
                                        self.create_xor_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],b=new_id[_gate.connected[1]])
                                    elif _gate.connected[0]!=None and _gate.connected[1]==None and (_gate.connected[0] in new_id and not(_gate.connected[1] in new_id)):
                                        self.create_xor_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],a=new_id[_gate.connected[0]])
                                    else:
                                        self.create_xor_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id])
                                if _gate.name=="nand_gate":
                                    if (_gate.connected[0]!=None and _gate.connected[1]!=None) and (_gate.connected[0] in new_id and _gate.connected[1] in new_id):
                                        self.create_nand_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],a=new_id[_gate.connected[0]],b=new_id[_gate.connected[1]])
                                    elif (_gate.connected[0]==None and _gate.connected[1]!=None) and (not(_gate.connected[0] in new_id) and _gate.connected[1] in new_id):
                                        self.create_nand_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],b=new_id[_gate.connected[1]])
                                    elif _gate.connected[0]!=None and _gate.connected[1]==None and (_gate.connected[0] in new_id and not(_gate.connected[1] in new_id)):
                                        self.create_nand_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],a=new_id[_gate.connected[0]])
                                    else:
                                        self.create_nand_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id])
                                if _gate.name=="not_gate":
                                    if _gate.connected[0]!=None and _gate.connected[0] in new_id:
                                        self.create_not_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],a=new_id[_gate.connected[0]])
                                    else:
                                        self.create_not_gate(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id])
                               
                                if _gate.name=="node":
                                    print("yea")
                                    if _gate.connected[0]!=None and _gate.connected[0] in new_id:
                                        self.create_node(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id],a=new_id[_gate.connected[0]])
                                    else:
                                        self.create_node(_gate.x+offset[0], _gate.y+offset[1],id=new_id[_gate.id])
                            
                            mode="selection"
                            all_id = [i.id for i in map0.all_gate]
                            
                            print(self.group_selected)
                            
                                        
                        
                elif mode=="interect":
                    if self.buttons[0] and gate.name in interectable:
                        touched+=1
                        gate.touch_action()
                        while(self.buttons[0]):
                            self.get_mouse_pos()
                            controll()
                
                break
        
        
            
        
        
        
        
        if touched==0:
            if mode=="build" or mode=="build-0" or mode=="selection":
                shifted = pygame.key.get_pressed()[pygame.K_LSHIFT]
                if self.buttons[0]:
                    mode = "selection"
                    if not shifted:
                        self.group_selected=[]
                        
                    this_term = []
                    loop=True
                    
                    self.get_mouse_pos()
                    ox = self.mmx
                    oy = self.mmy
                    while(loop):
                        controll()
                        self.get_mouse_pos()
                        
                        loop = self.buttons[0]
                        
                        startX = ox
                        startY = oy
                        self.get_mouse_pos()
                        if self.mmx<ox:
                            startX = self.mmx
                        if self.mmy<oy:
                            startY = self.mmy
                            
                        self.select_rect=pygame.Rect(startX,startY,abs(self.mmx-ox),abs(self.mmy-oy))
                        
                        
                        select_sur = pygame.Surface((abs(self.mmx-ox)*zoom, abs(self.mmy-oy)*zoom))
                        select_sur.fill((150,150,255))
                        select_sur.set_alpha(45)
                        
                        
                        self.draw()
                        self.win.blit(select_sur, ((startX-view_point[0])*zoom, (startY-view_point[1])*zoom))
                        
                        for gate in self.all_gate:
                            if self.select_rect.colliderect(gate.rect):
                                if not(gate.id in self.group_selected) and not(gate.id in this_term):
                                    self.group_selected.append(gate.id)
                                else:
                                    if shifted and not(gate.id in this_term):
                                        self.group_selected.remove(gate.id)
                                if not(gate.id in this_term):
                                    this_term.append(gate.id)
                                
                                
                        self.group_selected.sort()
                                
                        # print(self.group_selected)
                        
                        pygame.display.update()

                        
                elif self.buttons[2]:
                    mode = "build-0"
                    loop = True
                    options, option_box = draw_option_box(gates_type)
                    self.get_mouse_pos()
                    
                    self.draw()
                    
                    ox, oy = self.mx, self.my
                    oox, ooy = self.mmx, self.mmy
                    self.win.blit(option_box, (ox, oy))
                    
                    
                    pygame.display.update()

                    loop=True
                    selected=None
                    while(loop):
                        controll()
                        mx,my=pygame.mouse.get_pos()
                        buttons = (pygame.mouse.get_pressed())
                        for option in options:
                            rect = pygame.Rect(ox+option[0][0],oy+option[0][1],option[0][2],option[0][3])
                            if pygame.Rect.collidepoint(rect,(mx,my)) and buttons[0]:
                                print(option[1])
                                loop=False
                                selected = option[1]
                        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                            loop=False 
                            
                        self.draw()
                        self.win.blit(option_box, (ox, oy))
                        pygame.display.update()

                            
                    if selected!=None:
                        x,y = oox, ooy
                        if selected=="or gate":
                            self.create_or_gate(x, y)
                            
                        if selected=="and gate":
                            self.create_and_gate(x, y)
                        if selected=="source":
                            self.create_source(x,y)
                        if selected=="time source":
                            self.create_time_source(x,y)
                            
                        if selected=="peak time source":
                            self.create_peak_time_source(x,y)
                        if selected=="peak time source 2":
                            self.create_peak_time_source2(x,y)   
                        if selected=="LED":
                            self.create_LED(x,y)
                        if selected=="xor gate":
                            self.create_xor_gate(x,y)
                            
                        if selected=="nand gate":
                            self.create_nand_gate(x,y)
                            
                        if selected=="not gate":
                            self.create_not_gate(x,y)
                            
                        if selected=="node":
                            
                            self.create_node(x,y)
                            
                        if selected=="peak detector":
                            
                            self.create_peak_detector(x,y)
                            
                        all_id = [i.id for i in map0.all_gate]
                        self.update()
                    mode="build"               
         
        return 0          
    def update(self):
        
        for gate in self.all_gate:
            # gate.update_detection_box()
            gate.update()

            
    def create_source(self,x,y,v=False,id=None):
        if id == None:
            while(check_for_id_in_list0(self.global_id,self.all_gate))!=(None,None):
                self.global_id+=1
            self.all_gate.append(source(x,y,self,self.global_id,v))
        else:
            self.all_gate.append(source(x,y,self,id,v))
            
    def create_time_source(self,x,y,T=60,v=False,id=None):
            if id == None:
                while(check_for_id_in_list0(self.global_id,self.all_gate))!=(None,None):
                    self.global_id+=1
                self.all_gate.append(time_source(x,y,self,self.global_id,T=T))
            else:
                self.all_gate.append(time_source(x,y,self,id,T=T))
                         
    def create_and_gate(self,x,y,a=None,b=None,v=False,id=None):
        if id == None:
            while(check_for_id_in_list0(self.global_id,self.all_gate))!=(None,None):
                self.global_id+=1
            self.all_gate.append(and_gate(x,y,self,self.global_id,a=a,b=b))
        else:
            self.all_gate.append(and_gate(x,y,self,id,a=a,b=b))
            
    def create_or_gate(self,x,y,a=None,b=None,v=False,id=None):
        if id == None:
            while(check_for_id_in_list0(self.global_id,self.all_gate)!=(None,None)):
                self.global_id+=1
            self.all_gate.append(or_gate(x,y,self,self.global_id,a=a,b=b))
        else:
            self.all_gate.append(or_gate(x,y,self,id,a=a,b=b))
            
    def create_xor_gate(self,x,y,a=None,b=None,v=False,id=None):
        if id == None:
            while(check_for_id_in_list0(self.global_id,self.all_gate))!=(None,None):
                self.global_id+=1
            self.all_gate.append(xor_gate(x,y,self,self.global_id,a=a,b=b))
        else:
            self.all_gate.append(xor_gate(x,y,self,id,a=a,b=b))
    
    def create_LED(self,x,y,a=None,v=False,id=None):
        if id == None:
            while(check_for_id_in_list0(self.global_id,self.all_gate))!=(None,None):
                self.global_id+=1
            self.all_gate.append(LED(x,y,self,self.global_id,a=a))
        else:
            self.all_gate.append(LED(x,y,self,id,a=a))
    
    def create_nand_gate(self,x,y,a=None,b=None,v=False,id=None):
            if id == None:
                while(check_for_id_in_list0(self.global_id,self.all_gate))!=(None,None):
                    self.global_id+=1
                self.all_gate.append(nand_gate(x,y,self,self.global_id,a=a,b=b))
            else:
                self.all_gate.append(nand_gate(x,y,self,id,a=a,b=b))    
                
    def create_not_gate(self,x,y,a=None,v=False,id=None):
            if id == None:
                while(check_for_id_in_list0(self.global_id,self.all_gate))!=(None,None):
                    self.global_id+=1
                self.all_gate.append(not_gate(x,y,self,self.global_id,a=a))
            else:
                self.all_gate.append(not_gate(x,y,self,id,a=a)) 
                        
    def create_node(self,x,y,a=None,v=False,id=None):
            if id == None:
                while(check_for_id_in_list0(self.global_id,self.all_gate))!=(None,None):
                    self.global_id+=1
                self.all_gate.append(node(x,y,self,self.global_id,a=a))
            else:
                self.all_gate.append(node(x,y,self,id,a=a)) 
      
    def create_peak_time_source(self,x,y,T=60,v=False,id=None):
            if id == None:
                while(check_for_id_in_list0(self.global_id,self.all_gate))!=(None,None):
                    self.global_id+=1
                self.all_gate.append(peak_time_source(x,y,self,self.global_id,T=T))
            else:
                self.all_gate.append(peak_time_source(x,y,self,id,T=T))
                
    def create_peak_time_source2(self,x,y,T=60,v=False,id=None):
            if id == None:
                while(check_for_id_in_list0(self.global_id,self.all_gate))!=(None,None):
                    self.global_id+=1
                self.all_gate.append(peak_time_source2(x,y,self,self.global_id,T=T))
            else:
                self.all_gate.append(peak_time_source2(x,y,self,id,T=T))        
                
                
                
    def create_peak_detector(self,x,y,a=None,T=60,v=False,id=None):
        if id == None:
            while(check_for_id_in_list0(self.global_id,self.all_gate))!=(None,None):    
                self.global_id+=1
            self.all_gate.append(peak_detector(x,y,self,self.global_id,a,T=T))
        else:
            self.all_gate.append(peak_detector(x,y,self,id,a,T=T))
                       
                       
                       
    def delete(self,id):
        global all_id
        all_id = [i.id for i in self.all_gate]
        i = 0
        for gate in self.all_gate:
            if gate.id == id:
                for _gate in self.all_gate:
                    if _gate.id==gate.id:
                        continue
                    if _gate.connectectors>0:
                        if id in _gate.connected:
                            for i in range(len(_gate.connected)):
                                if id == _gate.connected[i]:
                                    _gate.connected[i]=None
                
                
                
                
                self.all_gate.pop(check_for_id_in_list0(id,self.all_gate)[0])
                
                
                
                
            i+=1
    
    def draw(self,selected=None):
        global line_drawn, node_drawm
        w,h = pygame.display.get_window_size()
        self.win.fill((0,0,0))
        line_sur = pygame.Surface((w,h))
        line_sur.set_colorkey((0,0,0))
        node_drawm = 0
        line_drawn = 0
        
        for gate in self.all_gate:

            blit_x = (gate.x-view_point[0])*zoom
            blit_y = (gate.y-view_point[1])*zoom
            
            if blit_x<w and blit_x>-gate_size*zoom and blit_y<h and blit_y>-gate_size*zoom:
                sur = pygame.transform.scale(gate.Surface, (gate_size*zoom,gate_size*zoom))
                node_drawm+=1
                if gate.id in self.group_selected:
                    blue = sur.copy()
                    blue.fill((0,0,255))
                    blue.set_alpha(150)
                    
                    self.win.blit(sur, (blit_x, blit_y))
                    self.win.blit(blue, (blit_x, blit_y))
                else:
                    if selected!=None:
                        if len(selected)==1:
                            if gate.id==selected[0]:
                                self.win.blit(sur, (blit_x, blit_y))
                            else:
                                tmp = sur.copy()
                                tmp.convert_alpha()
                                tmp.set_alpha(50)
                                self.win.blit(tmp, (blit_x, blit_y))
                        else:
                            tmp = sur.copy()
                            tmp.convert_alpha()
                            tmp.set_alpha(50)
                            self.win.blit(tmp, (blit_x, blit_y))
                            
                    else:
                        self.win.blit(sur, (blit_x, blit_y))

                            
            if gate.connectectors>0:
                
                for node in range(len(gate.connected)):
                        
                    node1 = check_for_id_in_list0(gate.connected[node], self.all_gate)[0]
                    if node1==None:
                        continue
                    
                    
                    
                    node0 = gate.input_pos[node]
                    
                    node1=self.all_gate[node1]
                    
                    
                    pos0 = ((gate.x+node0[0]-view_point[0])*zoom, (gate.y+node0[1]-view_point[1])*zoom)
                    pos1 = ((node1.x+node1.out_pos[0]-view_point[0])*zoom, (node1.y+node1.out_pos[1]-view_point[1])*zoom)

                    
                    if not(pygame.Rect(0,0,w,h).clipline(pos0, pos1)):
                        continue
                    line_drawn+=1
                    
                    
                    if node1.value and mode=="interect":
                        pygame.draw.line(line_sur, (0,255,0), pos0, pos1, 2)
                    else:
                        pygame.draw.line(line_sur, (150,150,150), pos0, pos1, 2)
                                

        self.win.blit(line_sur, (0,0))
        # print(count)
        if self.indication!=None:
            info_box = draw_info_box(self.indication).copy()
            self.win.blit(info_box, (0,h-info_box.get_height()))
        




map0 = environment()

#game stuff
options, option_box = draw_option_box(["open", "new file"])

loop=True
selected=None

while(loop):
    controll()
    mx, my = pygame.mouse.get_pos()
    ox, oy = w/2-option_box.get_width()/2,h/2-option_box.get_height()/2
    highlight = None
    for option in options:
        rect = pygame.Rect(ox+option[0][0],oy+option[0][1],option[0][2],option[0][3])
        if pygame.Rect.collidepoint(rect,(mx,my)):
            highlight = ((ox+option[0][0],oy+option[0][1]), pygame.Surface((option[0][2],option[0][3])))
            highlight[1].fill((120,120,255))
            highlight[1].set_alpha(100)
            if pygame.mouse.get_pressed()[0]:
                loop=False
                selected = option[1]
                
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            loop=False
    win.fill((0,0,50))
    win.blit(option_box, (ox, oy))
    
    if highlight!=None:
        win.blit(highlight[1], highlight[0])
    pygame.display.update()



_dir = str(__file__) 
_dir = _dir.split("\\")
now_path = ""
for i in range(len(_dir)-1):
    now_path+=str(_dir[i])+"\\"
    
if selected == "open":
    pygame.time.delay(500)
    selected_file = None
    loop=True
    
    offsetx, offsety=0, option_box.get_height()/4
    
    
    
    
    last = _dir[len(_dir)-1]
    
    
    while(loop):
        c = controll()
        if selected_file!=None:
            loop=False
        
        files=[]
        files.append("...back to original pos")
        files.append("...back")
        for i in os.listdir(now_path):
            files.append(i)
        
        files.append("...back to original pos")
        files.append("...back")
        
        
        options, option_box = draw_option_box(files, "open", w)
        ox, oy = w/2-option_box.get_width()/2,h/2-option_box.get_height()/2
        
        highlight = None
        last_sur = None
        
        if c == "mousewheelup":
            offsety+=50
        if c == "mousewheeldown":
            offsety-=50
        ox, oy = ox+offsetx, oy+offsety
        
        for option in options:
            mx, my = pygame.mouse.get_pos()
            rect = pygame.Rect(ox+option[0][0],oy+option[0][1],option[0][2],option[0][3])
            if option[1]==last:
                last_sur =  ((ox+option[0][0],oy+option[0][1]), pygame.Surface((option[0][2],option[0][3])))
                last_sur[1].fill((255,255,0))
                last_sur[1].set_alpha(100)
                
            if pygame.Rect.collidepoint(rect,(mx,my)):
                highlight = ((ox+option[0][0],oy+option[0][1]), pygame.Surface((option[0][2],option[0][3])))
                highlight[1].fill((120,120,255))
                highlight[1].set_alpha(100)
                
                if pygame.mouse.get_pressed()[0]:
                    if option[1]=="...back":
                        now_path=now_path.split("\\")
                        while("" in now_path):
                            now_path.remove("")
                        new_path = ""
                        for i in range(len(now_path)-1):
                            new_path+=str(now_path[i])+"\\"
                        
                        last = now_path[len(now_path)-1]
                        now_path=new_path
                        
                    if option[1]=="...back to original pos":
                        _dir = str(__file__) 
                        _dir = _dir.split("\\")
                        now_path = ""
                        for i in range(len(_dir)-1):
                            now_path+=str(_dir[i])+"\\"
                        
                    elif ".txt" in option[1]:
                        selected_file = option[1]
                    elif not("." in option[1]):
                        now_path+=option[1]
                        now_path+="\\"
                    
                    
                    
                    while(pygame.mouse.get_pressed()[0]):
                        controll()
                        pygame.display.update()
                    offsetx, offsety= 0,0
                    break
                    
                    
        win.fill((0,0,50))
        
        win.blit(option_box, (ox, oy))
        if highlight!=None:
            win.blit(highlight[1], highlight[0])
        if last_sur!=None:
            win.blit(last_sur[1], last_sur[0])

        
        
        
        t_r = bfont.render(str(now_path),True,(255,255,255))
        
        
        win.blit(t_r, (w/2-t_r.get_width()/2, 0))
        
        
        
        pygame.display.update()



    openx(now_path+selected_file, map0)
    print(selected_file)


all_id = [i.id for i in map0.all_gate]

mode = "build"


while(True):
    controll()
    
    
    win.fill((50,50,50))
    map0.controll_update()


    if mode=="interect":
        map0.update()
    


        
    map0.draw()
    
    
    win.blit(bfont.render("mode: "+mode, True, (255,255,255)), (0,0))
    
    global_id_r=bfont.render("global id: "+str(map0.global_id), True, (255,255,255))
    zoom_r=bfont.render("zoom scale: "+str(zoom), True, (255,255,255))
    
    # win.blit(global_id_r, (w/2-global_id_r.get_width()/2,0))
    win.blit(zoom_r, (w/2-zoom_r.get_width()/2,0))
    
    # pos_r = bfont.render("view_point x:"+str(view_point[0])+" y:"+str(view_point[1]), True, (255,255,255))
    
    # mpos_r = bfont.render("mouse x:"+str(round(map0.mmx, 2))+" y:"+str(round(map0.mmy, 2)), True, (255,255,255))
    
    draw_r = bfont.render("nodes drawn:"+str(node_drawm)+" lines drawn:"+str(line_drawn), True, (255,255,255))
    total_node_r = bfont.render("total nodes:"+str(len(map0.all_gate)), True, (255,255,255))

    win.blit(draw_r, (w-draw_r.get_width(),0))
    
    
    win.blit(total_node_r, ((w-total_node_r.get_width()),total_node_r.get_height()))
    
    
    
    pygame.display.update()
    

    
    
    clock.tick(60)
    
    map0.global_tick+=1
    
    pygame.display.set_caption(str(clock.get_fps()))
    
