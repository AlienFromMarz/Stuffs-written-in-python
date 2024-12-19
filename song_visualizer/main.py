import pygame,os,math,pydub,cv2
import numpy as np
import pygame.gfxdraw
from scipy.signal import stft
from scipy.io import wavfile


pydub.AudioSegment.ffmpeg = os.getcwd()+"\\ffmpeg\\ffmpeg.exe"


pygame.init()
        
settings = {}
w,h=800,800
screen=pygame.display.set_mode((w,h), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
pygame.display.set_caption("SONG player")
clock=pygame.time.Clock()


f_name = "PMingLiu"

sfont = pygame.font.SysFont(f_name,25,False)
bsfont = pygame.font.SysFont(f_name,25,True)
mfont = pygame.font.SysFont(f_name,36,False)
bmfont = pygame.font.SysFont(f_name,36,True)
bfont = pygame.font.SysFont(f_name,42,False)
bbfont = pygame.font.SysFont(f_name,42,True)

WHITE = (255,255,255)
BLACK = (0,0,0)

with open(os.getcwd()+os.sep+"setting.txt","r+",encoding="utf-8") as f:
    mode="idle"
    for line in f.readlines():
        line = line.split("\n")
        line = line[0].split(" ")
        if mode=="idle":
            if "liked" in line[0]:
                mode="liked cluster"
                settings["liked"]=[]
                
            else:
                settings[line[0]] = float(line[1])
                
        elif "cluster" in mode:
            if "}" in line[0]:
                mode="idle"
                
                
            if "liked" in mode:
                settings["liked"].append(line[0])
            

print(settings)       
            
            
def chinese_text(text,x,y,maxw,surface,font,c=WHITE,alpha=255):
    rx,ry=x,y
    for t in text:
        t_r = font.render(t,True,c)
        if rx+t_r.get_width()>=x+maxw:
            rx=x
            ry+=font.get_height()
        
        
        t_r.set_alpha(alpha)
        surface.blit(t_r,(rx,ry))
        rx+=t_r.get_width()
        
class Button():
    def __init__(self,x,y,w,h,text,uc=(50,50,50),ac=(200,200,200),halt=False,font=mfont,curved=True,fc=(255,255,255),border=False,alpha=255):
        self.text=text
        self.x,self.y=x,y
        self.w,self.h=w,h
        self.value = False
        self.halt=halt
        self.curved=curved
        self.border=border
        self.b_width = 2
        self.uc = uc
        self.ac = ac
        self.font=font
        self.fc=fc
        
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        self.surface = pygame.Surface((self.w,self.h))
        self.focus=False
        
        self.alpha=alpha
        
    def update(self,dt):
        self.value = False
        self.focus=False
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)

        mouse = pygame.mouse.get_pressed()
        m_pos = pygame.mouse.get_pos()

        self.surface.fill(BLACK)
        if self.curved:
            pygame.draw.rect(self.surface,self.uc,[0,0,self.w,self.h],border_radius=5)
        else:
            pygame.draw.rect(self.surface,self.uc,[0,0,self.w,self.h])
            
        if self.rect.collidepoint(m_pos):
            self.focus=True
            if self.curved:
                if self.border:
                    pygame.draw.rect(self.surface,self.ac,[0,0,self.w,self.h],self.b_width,border_radius=5)
                    
                else:
                    pygame.draw.rect(self.surface,self.ac,[0,0,self.w,self.h],border_radius=5)
            else:
                if self.border:
                    pygame.draw.rect(self.surface,self.ac,[0,0,self.w,self.h],self.b_width)
                    
                else:
                    pygame.draw.rect(self.surface,self.ac,[0,0,self.w,self.h])
            if mouse[0]:
                self.value=True
                if self.halt:
                    wait_for_unclick(clock)
    
    
    
    def draw(self,screen):
        
        self.surface.set_colorkey(BLACK)
        self.surface.set_alpha(self.alpha)
        screen.blit(self.surface,(self.x,self.y))
        text_r = self.font.render(self.text,True,self.fc)
        screen.blit(text_r,(self.x+self.w/2-text_r.get_width()/2,self.y+self.h/2-text_r.get_height()/2))

class Button_sur():
    def __init__(self,x,y,w,h,usur,asur,text,halt=False):
        self.text=text
        self.x,self.y=x,y
        self.w,self.h=w,h
        self.value = False
        self.halt=halt

        
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        
        self.ousur,self.oasur=usur,asur
        self.usur,self.asur=usur,asur
        self.surface = pygame.Surface((self.w,self.h))
        self.focus=False
        
    def resize(self,w,h):
        self.usur,self.asur=pygame.transform.scale(self.ousur,(w,h)),pygame.transform.scale(self.oasur,(w,h))
        
    def update(self,dt):
        self.value = False
        self.focus=False
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        mouse = pygame.mouse.get_pressed()
        m_pos = pygame.mouse.get_pos()
        self.surface.fill((0,0,0))
        self.surface.blit(self.usur,(0,0))
            
        if self.rect.collidepoint(m_pos):
            self.surface.blit(self.asur,(0,0))
            self.focus=True
            if mouse[0]:
                self.value=True
                if self.halt:
                    
                    wait_for_unclick(clock)

        
    
    
    def draw(self,screen):
        self.surface.set_colorkey((0,0,0))
        screen.blit(self.surface,(self.x,self.y))
        # pygame.draw.rect(screen,(255,0,0),self.rect,2)
        
        
        
        
class Slider():
    def __init__(self,x,y,w,h,text,uc=(50,50,50),ac=(150,150,150),c=(200,200,200)):
        self.text=text
        self.x,self.y=x,y
        self.w,self.h=w,h
        self.value = 0
        self.uc = uc
        self.ac = ac
        self.c = c
        
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        self.surface = pygame.Surface((self.w,self.h))
        self.focus=False
    def update(self,dt):
        
        mouse = pygame.mouse.get_pressed()
        m_pos = pygame.mouse.get_pos()
        
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        self.surface = pygame.Surface((self.w,self.h))
        
        self.surface.fill(self.uc)
        
        self.focus=False
        
        if self.rect.collidepoint(m_pos):
            self.surface.fill(self.ac)
            self.focus=True
            if mouse[0]:
                self.value=round(abs((m_pos[0]-self.x))/self.w,2)
        
        pygame.draw.rect(self.surface,self.c,[0,0,self.w*self.value,self.h])
    
    def draw(self,screen):
        
        text_r = mfont.render(str(self.value),True,WHITE)
        self.surface.blit(text_r,(self.w/2-text_r.get_width()/2,self.h/2-text_r.get_height()/2))
                
        screen.blit(self.surface,(self.x,self.y))

class Slider_V():
    def __init__(self,x,y,w,h,text,uc=(30,30,30),ac=(80,80,80),c=(200,200,200),hide_when_not_focus=True):
        self.text=text
        self.x,self.y=x,y
        self.w,self.h=w,h
        self.value = 0
        self.uc = uc
        self.ac = ac
        self.c = c
        
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        self.surface = pygame.Surface((self.w,self.h))
        self.focus=False
        self.hide_when_not_focus=hide_when_not_focus
    def update(self,dt):
        
        mouse = pygame.mouse.get_pressed()
        m_pos = pygame.mouse.get_pos()
        
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        self.surface = pygame.Surface((self.w,self.h))
        self.focus=False
        
        self.surface.fill(self.uc)
        
        
        if self.rect.collidepoint(m_pos):
            self.focus=True
            self.surface.fill(self.ac)
            if mouse[0]:
                self.value=round(abs((m_pos[1]-self.y))/self.h,2)
        
        pygame.draw.rect(self.surface,self.c,[0,self.h*(self.value),self.w,10],border_radius=2)
    
    def draw(self,screen):
        
        # text_r = mfont.render(str(self.value),True,WHITE)
        # self.surface.blit(text_r,(self.w/2-text_r.get_width()/2,self.h/2-text_r.get_height()/2))
        if self.hide_when_not_focus:
            if not self.focus:
                self.surface.set_alpha(50)
            else:
                self.surface.set_alpha(255)
                
        screen.blit(self.surface,(self.x,self.y))
     

class Song():
    def __init__(self,file_name):
        self.file_name=file_name
        print(self.file_name)
        if ".wav" in self.file_name:
            self.samplerate,self.raw_data = wavfile.read(filename=file_name)
            self.lengthins = self.raw_data.shape[0] / self.samplerate
            if len(self.raw_data.shape)>1:
                self.raw_data = self.raw_data.mean(axis=1)
            
            self.normalized_data = self.raw_data/np.max(self.raw_data)
            
            
            self.frquencies,self.times,self.zxx=stft(self.normalized_data,fs=self.samplerate)
            
            self.interval = self.lengthins/self.times.shape[0]
            self.maxv = np.max(np.abs(self.zxx))
            self.avgv = np.mean(np.abs(self.zxx))
            self.stdv = np.std(np.abs(self.zxx))
            self.volume=1
            self.music = pygame.mixer.music
            self.music.load(self.file_name)
            
        elif ".mp3" in self.file_name:
            self.file=pydub.AudioSegment.from_mp3(self.file_name)
            try:
                left_channel, right_channel = self.file.split_to_mono()
                left_channel=np.frombuffer(left_channel._data,dtype=np.int16)
                right_channel=np.frombuffer(right_channel._data,dtype=np.int16)
                self.raw_data = (left_channel+right_channel)/2
            except:
                self.raw_data = np.frombuffer(self.file._data,dtype=np.int16)
                
            self.samplerate=self.file.frame_rate
            self.lengthins = self.raw_data.shape[0] / self.samplerate
            self.normalized_data = self.raw_data/np.max(self.raw_data)
            
            
            self.frquencies,self.times,self.zxx=stft(self.normalized_data,fs=self.samplerate)
            
            self.interval = self.lengthins/self.times.shape[0]
            self.maxv = np.max(np.abs(self.zxx))
            self.avgv = np.mean(np.abs(self.zxx))
            self.stdv = np.std(np.abs(self.zxx))
            self.volume=1
            self.music = pygame.mixer.music
            self.music.load(self.file_name)
                
        elif ".mp4" in self.file_name:
            
            self.file=pydub.AudioSegment.from_file(self.file_name,"mp4")
            self.file.export(out_f = "temp/temp.wav",  
                       format = "wav") 
            try:
                left_channel, right_channel = self.file.split_to_mono()
                left_channel=np.frombuffer(left_channel._data,dtype=np.int16)
                right_channel=np.frombuffer(right_channel._data,dtype=np.int16)
                self.raw_data = (left_channel+right_channel)/2
            except:
                self.raw_data = np.frombuffer(self.file._data,dtype=np.int16)
                
            self.samplerate=self.file.frame_rate
            self.lengthins = self.raw_data.shape[0] / self.samplerate
            self.normalized_data = self.raw_data/np.max(np.abs(self.raw_data))
            
            
            self.frquencies,self.times,self.zxx=stft(self.normalized_data,fs=self.samplerate)
            
            self.interval = self.lengthins/self.times.shape[0]
            self.maxv = np.max(np.abs(self.zxx))
            self.avgv = np.mean(np.abs(self.zxx))
            self.stdv = np.std(np.abs(self.zxx))
            
            self.volume=1
            self.music = pygame.mixer.music
            self.music.load(os.getcwd()+os.sep+"temp/temp.wav")
        
        
        print(self.stdv)
        
        print("----file----")
        print("total duration in second:")
        print(self.lengthins,":",self.raw_data.shape[0]*1/self.samplerate)
        print("sample rate:")
        print(self.samplerate)
        
        print("----stft_result----")
        print("times:")
        print(self.times.shape)
        
        print("frequencies:")
        print(self.frquencies.shape)
        print("zxx:")
        print(self.zxx.shape)
        

        
        
        
        self.time=0
        self.oldtime=0
        self.playing=False
        
    def change_volume(self,dv):
        self.volume+=dv
        self.music.set_volume(self.volume)
            
    def pause(self):
        self.playing=not(self.playing)
        if self.playing:
            if ".mp4" in self.file_name:
                self.music.load(os.getcwd()+os.sep+"temp/temp.wav")
            else:
                self.music.load(self.file_name)
            self.music.play(0,self.time/1000)
            self.oldtime=self.time
        else:
            self.music.stop()
            self.music.unload()
        
    def update(self,key=None):
        if self.time>=self.lengthins*1000:
            self.playing=False
            self.music.stop()
            self.music.unload()
            return 0
                        
                        
        if self.playing:
            self.time=self.oldtime+self.music.get_pos()

            
    def skip(self,t):
        if self.time>=self.lengthins*1000:
            self.playing=False
            self.music.stop()
            self.music.unload()
            return 0
        if self.playing:
            self.time=t
            self.music.stop()
            self.music.unload()
            if ".mp4" in self.file_name:
                self.music.load(os.getcwd()+os.sep+"temp/temp.wav")
            else:
                self.music.load(self.file_name)
            self.music.play(0,self.time/1000)
            self.oldtime=self.time
        else:
            self.time=t
            
            
    def get_frequencies_at_time(self,t=0):
        #x is the frequency
        i = int(t/self.interval)
        if t>=self.lengthins:
            return np.array([0,0,0,0]),np.array([0,0,0,0])
        freqstrength = np.abs(np.array([self.zxx[o][i] for o in range(self.zxx.shape[0]-1)]))
        # freqstrength/=self.maxv
        
        freq = [self.frquencies[o] for o in range(self.zxx.shape[0]-1)]
        return freq,freqstrength
    
    def play(self):
        self.playing=True
        self.music.set_volume(self.volume)
        self.music.play()

def resize(img,w,ratio):
    return cv2.resize(img, dsize=(w, int(ratio*w)), interpolation=cv2.INTER_NEAREST)
          
class Video():
    def __init__(self,file_name,song):
        self.file_name=file_name
        self.video = cv2.VideoCapture(file_name)
        while not self.video.isOpened():
            self.video = cv2.VideoCapture(file_name)
            cv2.waitKey(1000)
        self.nframes = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.song=song
        
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.alpha=40
        self.w  = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.h = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT) 
        self.ratio = self.w/self.h
        self.success,self.video_img = self.video.read()
        self.disable=False
        
    def update(self):
        if self.song.playing and not(self.disable):
            self.video.set(cv2.CAP_PROP_POS_FRAMES, int(self.song.time/1000/self.song.lengthins*self.nframes)-1)
            self.success,self.video_img = self.video.read()

    def draw(self,screen):
        if self.success and not(self.disable):

            self.video_img=cv2.resize(self.video_img, dsize=(int(self.ratio*h), h), interpolation=cv2.INTER_LINEAR)
            
            temp = pygame.image.frombuffer(self.video_img.tobytes(), self.video_img.shape[1::-1], "BGR")
            temp.set_alpha(self.alpha)

            
            screen.blit(temp, (w/2-temp.width/2, h/2-temp.height/2))
            
            
class Song_list():
    def __init__(self,file_name=None,direct_lists=[]):
        print(file_name,direct_lists)
        if file_name!=None:
            self.file_name=file_name
            self.locations=[]
            with open(self.file_name, "r+", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.split("\n")
                    self.locations.append(line[0])
        else:
            self.file_name=file_name
            self.locations=direct_lists

        self.track_number=0
        self.current=Song(self.locations[self.track_number])
        self.current.play()
        self.isVideo = ".mp4" in self.locations[self.track_number]
        if self.isVideo:
            self.currentVideo=Video(self.locations[self.track_number],self.current)
        else:
            self.currentVideo=None
        self.volume=settings["volume"]
        self.disable_video=bool(int(settings["video_disable"]))
        print("----------------")
        print(self.disable_video)
        print("----------------")
    def previous(self):
        self.track_number-=1
        
        if self.track_number>=0:
            self.current.music.stop()
            self.current.music.unload()
            self.current=Song(self.locations[self.track_number])
            self.current.play()
            self.isVideo = ".mp4" in self.locations[self.track_number]
            if self.isVideo:
                self.currentVideo=Video(self.locations[self.track_number],self.current)
            else:
                self.currentVideo=None
            
        else:
            self.current.playing=False
            self.current.pause()
            self.track_number=0
            
    def next(self):
        self.track_number+=1
        
        if self.track_number<=len(self.locations)-1:
            self.current.music.stop()
            self.current.music.unload()
            self.current=Song(self.locations[self.track_number])
            self.current.play()
            self.isVideo = ".mp4" in self.locations[self.track_number]
            if self.isVideo:
                self.currentVideo=Video(self.locations[self.track_number],self.current)
            else:
                self.currentVideo=None
                
        else:
            self.current.playing=False
            self.current.pause()
            self.track_number=len(self.locations)-1
            
    def skipto(self,num):
        self.track_number=num
        
        if self.track_number<=len(self.locations)-1:
            self.current.music.stop()
            self.current.music.unload()
            self.current=Song(self.locations[self.track_number])
            self.current.play()
            self.isVideo = ".mp4" in self.locations[self.track_number]
            if self.isVideo:
                self.currentVideo=Video(self.locations[self.track_number],self.current)
            else:
                self.currentVideo=None
                
        else:
            self.current.playing=False
            self.current.pause()
    
    def update(self):
        self.isVideo = ".mp4" in self.locations[self.track_number]
        if self.isVideo:
            self.currentVideo.disable=self.disable_video
            
        if self.current.time>=self.current.lengthins*1000:
            self.track_number+=1
            
            if self.track_number<=len(self.locations)-1:
                self.current.music.stop()
                self.current.music.unload()
                self.current=Song(self.locations[self.track_number])
                self.current.play()
                self.isVideo = ".mp4" in self.locations[self.track_number]
                if self.isVideo:
                    self.currentVideo=Video(self.locations[self.track_number],self.current)
                else:
                    self.currentVideo=None
                
            else:
                self.current.playing=False
                self.current.pause()
                
                
                
        self.current.volume=self.volume
        self.current.music.set_volume(self.volume)
        self.current.update()
        if self.isVideo:
            self.currentVideo.update()
        

def controll():
    global w,h
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            quitall()
        if e.type==pygame.VIDEORESIZE:
            w,h=pygame.display.get_window_size()

def wait_for_unclick(clock,mousei=0):
    while(True):
        dt = clock.tick(60)/1000
        controll()
        mouse = pygame.mouse.get_pressed()
        if not mouse[mousei]:
            return 0
        
        
        pygame.display.update()
    

def wait_for_unpress(clock,keyi):
    while(True):
        dt = clock.tick(60)/1000
        controll()
        key = pygame.key.get_pressed()
        if not key[keyi]:
            return 0
        
        
        pygame.display.update()
    
    
def sort_dir_to_top(list):
    temp = []
    temp2 = []
    for i in list:
        if "." not in i:
            temp.append(i)
        else:
            temp2.append(i)
                    
    for i in temp:
        temp2.insert(0,i)
    return temp2
    
def quitall():
    open(os.getcwd()+os.sep+"setting.txt", "w").close()
    with open(os.getcwd()+os.sep+"setting.txt","w+",encoding="utf-8") as f:
        for index in settings:
            print(index)
            if index=="video_disable":
                f.write(index+" "+str(settings[index])+"\n")            
            elif index=="volume":
                f.write(index+" "+str(settings[index])+"\n")            
            elif index=="liked":
                f.write(index+"{"+"\n")            
                for path in settings[index]:
                    f.write(path+"\n")     
                    
                f.write("}\n")       

    
    
    
    pygame.quit()
    quit()
    
        
def select_screen():
    global w,h
    mode = "idle"
    path = os.getcwd()
    last_path = path.split(os.sep)
    last_path = last_path[len(last_path)-1]
    back_img = pygame.image.load(os.getcwd()+os.sep+"images/back.png").convert_alpha()
    home_img = pygame.image.load(os.getcwd()+os.sep+"images/home.png").convert_alpha()
    home_img = pygame.transform.scale(home_img, (home_img.width/home_img.height*back_img.height*1.1,back_img.height*1.1))
    
    mbackButton = Button_sur(10,h-back_img.get_height()-10,back_img.get_width(),back_img.get_height(),back_img,back_img,"back",halt=True)
    homeButton = Button_sur(mbackButton.w+50,h-home_img.get_height()-20,home_img.get_width(),home_img.get_height(),home_img,home_img,"home",halt=True)
    likeButton = Button_sur(mbackButton.w+homeButton.w+90,h-home_img.get_height()-20,home_img.get_width(),home_img.get_height(),home_img,home_img,"home",halt=True)
    
    dy = 0
    while(True):
        dt = clock.tick(60)/1000
        
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                quitall()
            if e.type==pygame.VIDEORESIZE:
                w,h=pygame.display.get_window_size()
        
            if e.type==pygame.MOUSEWHEEL:
                if e.y>0 and dy+50<=0:
                    dy+=50
                elif e.y<0 and dy-50>=min(0,h-height-52*3):
                    dy-=50
        mouse=pygame.mouse.get_pressed()
        m_pos=pygame.mouse.get_pos()
        key=pygame.key.get_pressed()
            
        mbackButton.x,mbackButton.y = 20,h-back_img.get_height()-20
        homeButton.x,homeButton.y = mbackButton.w+50,h-homeButton.h-20
        likeButton.x,likeButton.y = homeButton.w+mbackButton.w+90,h-likeButton.h-20
        
        if mode=="idle":
            all_list = os.listdir(path)
            buttons = []
            i = 0
            all_list = sort_dir_to_top(all_list)
            
            
            for file in all_list:
                c = (60,60,60)
                if not("." in file):
                    c = (30,30,30)
                if last_path == file:
                    c=(50,50,50)
                    
                if path+os.sep+file in settings["liked"]:
                    c = (80, 60, 60)

                if ".wav" in file or ".mp3" in file or ".mp4" in file or ".allenlist" in file or not("." in file):
                    buttons.append(Button(0,dy+70+mfont.get_height()+52*i,w,50,file,c,halt=True,border=True))
    
                    i+=1
            
            height=52*(i)

        
        elif mode=="liked":
            all_list = settings["liked"]
            buttons = []
            i = 0
            
            for file in all_list:
                c = (60,60,60)
                if not("." in file):
                    c = (30,30,30)
                if last_path == file:
                    c=(50,50,50)
                    
                if file in settings["liked"]:
                    c = (80, 60, 60)

                if ".wav" in file or ".mp3" in file or ".mp4" in file or ".allenlist" in file or not("." in file):
                    buttons.append(Button(0,dy+70+mfont.get_height()+52*i,w,50,file,c,halt=True,border=True))
    
                    i+=1
            
            height=52*(i)
            
        
        

                
                
        
        mbackButton.update(dt)
        if mode=="idle":
            homeButton.update(dt)
            likeButton.update(dt)
            
        
        if key[pygame.K_BACKSPACE] and mode=="idle":
            dy=0
            new_path = path.split(os.sep)
            new_path = new_path[:-1]
            new_path = "\\".join(new_path)
            if not os.path.exists(new_path):
                continue
            path=new_path
            print(new_path)
            wait_for_unpress(clock,pygame.K_BACKSPACE)

        if mbackButton.value:
            if mode=="idle":
                dy=0
                new_path = path.split(os.sep)
                new_path = new_path[:-1]
                new_path = "\\".join(new_path)
                if not os.path.exists(new_path):
                    continue
                path=new_path
                print(new_path)
            elif mode=="liked":
                mode="idle"

        elif homeButton.value and mode=="idle":
            dy=0
            new_path = os.getcwd()
            if not os.path.exists(new_path):
                continue
            path=new_path
            print(new_path)

        elif likeButton.value and mode=="idle":
            mode="liked"
        selected = None
        for b in buttons:
            b.update(dt)
            if b.value:
                selected=b.text
            elif b.focus and "." in b.text:
                if mouse[2]:
                    
                    if path+os.sep+b.text in settings["liked"]:
                        settings["liked"].remove(path+os.sep+b.text)
                    else:
                        settings["liked"].append(path+os.sep+b.text)
                        
                    wait_for_unclick(clock,2)
                
                    
                
        if selected!=None:
            if "." not in selected:
                dy=0
                path+=("\\"+selected)
                continue
            else:
                if mode=="idle":
                    
                    print(path+("\\"+selected))
                    return path+("\\"+selected)
                elif mode=="liked":
                    return selected

        screen.fill(BLACK)
        

            
        for b in buttons:
            
            b.draw(screen)
            if ".wav" in b.text:
                chinese_text("WAV",10,b.y+b.h/2-bmfont.get_height()/2,w,screen,bmfont,alpha=50)
            elif ".allenlist" in b.text:
                chinese_text("PlYLST",10,b.y+b.h/2-bmfont.get_height()/2,w,screen,bmfont,alpha=50)
            elif ".mp3" in b.text:
                chinese_text("MP3",10,b.y+b.h/2-bmfont.get_height()/2,w,screen,bmfont,alpha=50)
            elif ".mp4" in b.text:
                chinese_text("MP3",10,b.y+b.h/2-bmfont.get_height()/2,w,screen,bmfont,alpha=50)
            elif not("." in b.text):
                chinese_text("DIR",10,b.y+b.h/2-bmfont.get_height()/2,w,screen,bmfont,alpha=50)
            
            
            
                
                
            
        mbackButton.draw(screen)
        if mode=="idle":
            homeButton.draw(screen)
            likeButton.draw(screen)
        
        pygame.draw.rect(screen,BLACK,(0,0,w,50+sfont.get_height()+5))
        chinese_text("current: "+str(path),0,50,w,screen,sfont)
        
        pygame.draw.line(screen,WHITE,(0,50+sfont.get_height()+5),(w,50+sfont.get_height()+5),2)
            
        pygame.display.update()    


def main(file):
    global w,h

    if ".wav" in file or ".mp3" in file or ".mp4" in file:

        s = Song_list(direct_lists=[file])
        
    elif ".allenlist" in file:
        s = Song_list(file)
    
        
    mode="circle"
    inner_r = 0.2
    outer_r = 0.8
    
    linei_r = 0.3
    lineo_r = 1
    

    getvalueinterval = 0.025
    lastshck = 0
    
    circling_theta = 0
    last_change_v_time=-10000
    
    
    temp = pygame.Surface((150,50))
    pygame.draw.polygon(temp,(255,255,255),[(75+20,25),(75-20,25+10*1.7),(75-20,25-10*1.7)],2)
    
    temp1 = pygame.Surface((150,50))
    pygame.draw.polygon(temp1,(255,255,255),[(75+20,25),(75-20,25+10*1.7),(75-20,25-10*1.7)])
    
    
    skip_img = pygame.image.load(os.getcwd()+os.sep+"images/skip.png")
    skip_img = pygame.transform.scale(skip_img,(skip_img.width*0.3,skip_img.height*0.3))
    skip1_img = pygame.image.load(os.getcwd()+os.sep+"images/skip1.png")
    skip1_img = pygame.transform.scale(skip1_img,(skip1_img.width*0.3,skip1_img.height*0.3))
    
    next_sbutton = Button_sur(w/2-100-skip_img.width/2,h-skip_img.height-10,skip_img.width,skip_img.height,skip_img,skip1_img ,"next")
    
    previous_sbutton = Button_sur(w/2+100,h-skip_img.height-10,skip_img.width,skip_img.height,pygame.transform.flip(skip_img,True,False),pygame.transform.flip(skip1_img,True,False),"previous")
    
    pause_img = pygame.Surface((50,50))
    pygame.draw.rect(pause_img,(255,255,255),[0,0,50,50],2,border_radius=2)
    pause_img1 = pygame.Surface((50,50))
    pygame.draw.rect(pause_img1,(255,255,255),[0,0,50,50],border_radius=2)
    pause_button = Button_sur(w/2-pause_img.width/2,h-pause_img.get_height()-10,pause_img.get_width(),pause_img.get_height(),pause_img,pause_img1,"pause",halt=True)
    
    file_img = pygame.image.load(os.getcwd()+os.sep+"images/files.png").convert_alpha()
    file_img = pygame.transform.scale(file_img, (file_img.width*0.25,file_img.height*0.25))
    
    change_sbutton = Button_sur(pause_button.x+pause_button.w+10,h-file_img.get_height()-10,file_img.get_width(),file_img.get_height(),file_img,file_img,"select",halt=True)
    
    Video_sbutton = Button(20,20,100,50,"video",font=bsfont,halt=True)
    
    
    
    
    
    
    scrollY_slider = Slider_V(w-20,0,20,h,"")
    
    select_songs = False
    last = None
    while(True):
        #update
        dt = clock.tick()/1000

            
        pygame.display.set_caption(str(clock.get_fps()))
        mouse = pygame.mouse.get_pressed()
        m_pos = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                quitall()
            if e.type==pygame.VIDEORESIZE:
                w,h=pygame.display.get_window_size()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_SPACE:
                    s.current.pause()
                elif e.key==pygame.K_d:
                    s.next()
                elif e.key==pygame.K_a:
                    s.previous()
                elif e.key==pygame.K_e:
                    
                    select_songs=not(select_songs)
                    
                    
            if e.type==pygame.MOUSEWHEEL:
                if select_songs:
                    if e.y<0 and scrollY_slider.value+0.1<=1:
                        scrollY_slider.value+=0.1
                    elif e.y>0 and scrollY_slider.value-0.1>=0:
                        scrollY_slider.value-=0.1

                elif not(select_songs):
                    last_change_v_time=pygame.time.get_ticks()
                    if e.y>0 and s.current.volume+0.05<=1:
                        s.volume+=0.05
                    elif e.y<0 and s.current.volume-0.05>=0:
                        s.volume-=0.05

        key=pygame.key.get_pressed()

        if mouse[2]:
            select_songs=not(select_songs)
            wait_for_unclick(clock,2)
            
        if key[pygame.K_w] and s.current.volume+0.01<=1:
            last_change_v_time=pygame.time.get_ticks()
            s.volume+=0.01
        elif key[pygame.K_s] and s.current.volume-0.01>=0:
            last_change_v_time=pygame.time.get_ticks()
            s.volume-=0.01
            
        if key[pygame.K_RIGHT] and s.current.time+100<=s.current.lengthins*1000:
            s.current.skip(s.current.time+100)
        elif key[pygame.K_LEFT] and s.current.time-100>=0:
            s.current.skip(s.current.time-100)
            
            
            
        if key[pygame.K_m]:
            last_change_v_time=pygame.time.get_ticks()
            s.volume=0

        
        
        previous_sbutton.x, previous_sbutton.y=w/2-100-previous_sbutton.w,h-previous_sbutton.h-10
        next_sbutton.x,next_sbutton.y=w/2+100,h-next_sbutton.h-10
        pause_button.x,pause_button.y=w/2-pause_button.w/2,h-pause_button.h-10
        change_sbutton.x,change_sbutton.y=pause_button.x+pause_button.w+10,h-change_sbutton.h-10
        
        previous_sbutton.update(dt)
        next_sbutton.update(dt)
        pause_button.update(dt)
        
        scrollY_slider.x=w-20
        scrollY_slider.h=h
        
        if pause_button.value:
            s.current.pause()


        if next_sbutton.value:
            s.next()
        elif previous_sbutton.value:
            s.previous()
            
        change_sbutton.update(dt)
        if change_sbutton.value:
            s.current.music.stop()
            s.current.music.unload()
            return 0
            
        s.update()
        settings["volume"]=s.volume
        
        freq,freqstrength = s.current.get_frequencies_at_time(getvalueinterval*int((s.current.time/1000)/getvalueinterval))
        
        # _c = max(0,max(10,10*freqstrength.mean()/s.current.stdv))
        screen.fill((0,0,15))
        if s.isVideo:
            s.currentVideo.draw(screen)
            
            
        #draw bars and shits
        if mode=="bar":
            #draw bar

            width = w/int(len(freq)*0.5)
            for f in range(int(len(freq)*0.5)):
                x = width*f
                y=h*freqstrength[f]
                pygame.draw.rect(screen,WHITE,[x,h-y,width,y])
            
            #draw line
            last_pos = (0,h*0.8-h*0.5*freqstrength[0])
            for f in range(1,int(len(freq)*0.5)):
                x = width*f
                y=h*0.8-h*0.5*freqstrength[f]
                
                pygame.draw.line(screen,WHITE,(x,y),last_pos)
                
                last_pos=(x,y)

        elif mode=="circle":
            #draw bar
            circling_theta+=dt*0.1
            if circling_theta>=6.28:
                circling_theta-=6.28
            delta_theta = 6.28/(len(freq)-1)
            width = 2*(inner_r)*h*3.14/(len(freq)-1)
            
            
            for f in range(int(len(freq))):
                if last!=None:
                    strength = (freqstrength[f]+last[f])/2
                else:
                    strength = freqstrength[f]

                c = max(150,min(255,150+int(255*strength)))
                theta = delta_theta*f+circling_theta
                uv=[math.cos(theta),math.sin(theta)]
                nv=[-math.sin(theta),math.cos(theta)]
                x = w/2+(inner_r)*h*uv[0]
                y = h/2+(inner_r)*h*uv[1]
                
                pos0 = [x+nv[0]*width/2,y+nv[1]*width/2]
                pos1 = [x-nv[0]*width/2,y-nv[1]*width/2]
                
                pos2 = [x+nv[0]*width/2+outer_r*h*strength*uv[0],y+nv[1]*width/2+outer_r*strength*h*uv[1]]
                pos3 = [x-nv[0]*width/2+outer_r*h*strength*uv[0],y-nv[1]*width/2+outer_r*strength*h*uv[1]]
                
                # pygame.draw.circle(screen,WHITE,(x,y),2)
                pygame.draw.polygon(screen,(c,c,c),[pos0,pos1,pos3,pos2])
                # pygame.draw.rect(screen,WHITE,[x,h-y,width,y])
                
            uv=[math.cos(-circling_theta),math.sin(-circling_theta)]
            nv=[-math.sin(-circling_theta),math.cos(-circling_theta)]
            last_pos = [w/2+(linei_r)*h*uv[0]+lineo_r*h*strength*uv[0],
                        h/2+(linei_r)*h*uv[1]+lineo_r*h*strength*uv[1]]
            for f in range(1,int(len(freq))):
                if last!=None:
                    strength = (freqstrength[f]+last[f])/2
                else:
                    strength = freqstrength[f]
                
                theta = delta_theta*f-circling_theta
                uv=[math.cos(theta),math.sin(theta)]
                nv=[-math.sin(theta),math.cos(theta)]

                now_pos = [w/2+(linei_r)*h*uv[0]+lineo_r*h*strength*uv[0],
                        h/2+(linei_r)*h*uv[1]+lineo_r*h*strength*uv[1]]
                pygame.draw.line(screen,WHITE,now_pos,last_pos)
                last_pos=now_pos
           
        #cool zoom effect   
        # print(freqstrength.mean()/s.stdv)
        # if freqstrength.mean()/s.current.stdv>=0.5 and pygame.time.get_ticks()-lastshck>100:
        #     lastshck=pygame.time.get_ticks()
        # elif pygame.time.get_ticks()-lastshck<=50:
        #     inner_r = min(inner_r+2*dt,0.21)
        #     linei_r = min(linei_r+dt,0.4)
        # else:
        #     inner_r = max(0.2,inner_r-0.5*dt)
        #     linei_r = max(0.3,linei_r-0.5*dt)



        #play bar
        playbarwp = 0.2
        playbarx,playbary = w*(1-playbarwp)/2,h*0.83
        rect = pygame.Rect(playbarx,playbary,w*playbarwp,15)
        rect2 = pygame.Rect(playbarx,playbary,w*playbarwp*s.current.time/1000/s.current.lengthins,15)
        c = (150,150,150)
        if rect.collidepoint(m_pos):
            c=(210,210,210)
            if mouse[0]:
                x = m_pos[0]-rect.x
                s.current.music.set_volume(0)
                s.current.skip(x/rect.w*s.current.lengthins*1000)
            else:
                s.current.music.set_volume(s.current.volume)
                
        pygame.draw.rect(screen,c,rect,border_radius=3)
        pygame.draw.rect(screen, WHITE,rect2,border_radius=3)
        if not rect.collidepoint(m_pos):
            time_r = sfont.render(str(int((s.current.time/1000)//60))+":"+str(round((s.current.time/1000)%60,1)),True,(100,100,100))        
        else:
            x = m_pos[0]-rect.x
            time_r = sfont.render(str(int((x/rect.w*s.current.lengthins)//60))+":"+str(round((x/rect.w*s.current.lengthins)%60,1)),True,(100,100,100))        

        
        screen.blit(time_r,(playbarx+playbarwp*w*0.5-time_r.width/2,playbary+time_r.get_height()/2+5))




        if not s.current.playing:
            prect = pygame.Rect(w/2-20,h/2-20,40,40)
            mprect = pygame.Rect(w/2-5,h/2-20,10,40)
            pygame.draw.rect(screen, WHITE,prect)
            pygame.draw.rect(screen, BLACK,mprect)


        #volume bar
        
        if pygame.time.get_ticks()-last_change_v_time<=1500:
            volumebarx,volumebary=w*0.1,h*0.3
            sur = pygame.Surface((10,200))
            volumebarh = s.current.volume*200
            
            sur.fill((50,50,50))
            pygame.draw.rect(sur,(200,200,200),[0,200-volumebarh,10,volumebarh])
            sur.set_alpha(255*max(0,1-(pygame.time.get_ticks()-last_change_v_time)/1500))
            screen.blit(sur,(volumebarx,volumebary))

        change_sbutton.draw(screen)
        next_sbutton.draw(screen)
        previous_sbutton.draw(screen)
        pause_button.draw(screen)
        
        name = s.current.file_name.split("\\")
        name = name[len(name)-1]
        name_r = bsfont.render(name,True,(150,150,150))
        screen.blit(name_r,(w/2-name_r.get_width()/2,name_r.get_height()/2+10))
        
        
        #show playlist
        if select_songs:
            Video_sbutton.update(dt)
            if Video_sbutton.value:
                if s.isVideo:
                    s.disable_video=not(s.disable_video)
        
            Black_sur = pygame.Surface((w,h))
            Black_sur.set_alpha(150)
            screen.blit(Black_sur,(0,0))
                
            
            maxwtext = 0
            scrollY_slider.update(dt)
            
            for i in s.locations:
                name = i.split("\\")
                name_r = mfont.render(name[len(name)-1],True,(0,0,0))
                if name_r.width>=maxwtext:
                    maxwtext=name_r.width
                
                
            for i in range(max(0,int((-h*0.2+sfont.get_height()+scrollY_slider.value*50*len(s.locations))/50)),min(int((h-h*0.2+sfont.get_height()+scrollY_slider.value*50*len(s.locations))/50)+1,len(s.locations))):
                y=h*0.2-sfont.get_height()+i*50-scrollY_slider.value*50*len(s.locations)

                name = s.locations[i].split("\\")
                name = name[len(name)-1]
                x=w/2-min(w*0.7,maxwtext)/2

                if i==s.track_number:
                    b=Button(x,y,min(w*0.7,maxwtext),name_r.height,name,uc=(50,50,50),ac=(70,70,70),halt=True,fc=(200,200,200),font=bsfont,alpha=150)

                else:
                    b=Button(x,y,min(w*0.7,maxwtext),name_r.height,name,uc=(0,0,0),ac=(20,20,20),halt=True,fc=(150,150,150),font=bsfont,alpha=150)
                
                
                b.update(dt)
                b.draw(screen)
                # screen.blit(name_r,(x,y))
                if b.value and not scrollY_slider.focus:
                    s.skipto(i)
                    
            scrollY_slider.draw(screen)
            Video_sbutton.draw(screen)
        last=list(freqstrength)
        pygame.display.update()
                



if __name__=="__main__":        
    while(True):
        file = select_screen()

        main(file)
            
