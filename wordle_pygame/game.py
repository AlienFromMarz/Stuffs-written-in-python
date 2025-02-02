import pygame
import sys
import random

def writein(word, list, index):
    temp_list = []
    for w in word:
        temp_list.append(w)
    list[index]=temp_list
    
def find_letter_in(char, word):
    index = 0
    list = []
    for c in word:
        if char==c:
            list.append(index)    
        index+=1
    return list
def find(word):
    txt_file = open("words.txt")
    for line in txt_file:
        if line[:-1]==word:
            return True
    return False
class main():
    def __init__(self, width, height):
        self.done = ""
        pygame.init()
        pygame.font.get_fonts()
        self.width, self.height = width, height
        # self.screen = pygame.display.set_mode((width, height))
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.screen = pygame.Surface(self.window.get_size())
        pygame.display.set_caption("WORDLE")
        #14854-0
        self.answer_index = random.randint(0,14854)
        i = 0
        txt_file = open("words.txt")

        for line in txt_file:
            if i==self.answer_index:
                print(line)
                self.answer = str(line)
                break
            i+=1
        
        self.map = [["","","","",""],
                    ["","","","",""],
                    ["","","","",""],
                    ["","","","",""],
                    ["","","","",""],
                    ["","","","",""]]
        self.correct = [[0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0]]
        
        
        self.now_row=0
        self.text = ""
        
        self.listen_to_keys=True
        self.letters0 = []
        self.letters1 = []
        self.letters3 = []
        self.press_key_ = ""
        
        self.main_loop()
    def reset(self):
        self.done = ""
        # self.screen = pygame.display.set_mode((width, height))

        #14854-0
        self.answer_index = random.randint(0,14854)
        i = 0
        txt_file = open("words.txt")

        for line in txt_file:
            if i==self.answer_index:
                print(line)
                self.answer = str(line)
                break
            i+=1
        
        self.map = [["","","","",""],
                    ["","","","",""],
                    ["","","","",""],
                    ["","","","",""],
                    ["","","","",""],
                    ["","","","",""]]
        self.correct = [[0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0]]
        
        
        self.now_row=0
        self.text = ""
        
        self.listen_to_keys=True
        self.letters0 = []
        self.letters1 = []
        self.letters3 = []
        self.press_key_ = ""
        self.screen.fill((0,0,0))
        
    def draw_text(self, text, spacing, x, y, size, row_=None, mode="back", color_=(255,255,255)):
        index=0
        for char in text:
            if mode=="back":
                if self.correct[row_][index]==0:
                    color = (50,50,50)
                elif self.correct[row_][index]==1:
                    color = (100,255,100)
                elif self.correct[row_][index]==2:
                    color = (172,205,22)
                elif self.correct[row_][index]==3:
                    color = (50,50,50)

                surface = pygame.Surface((size, size))#x+(size+spacing)*index-size/4, y-size/64, 
                surface.fill(color)
                surface.set_alpha(190)
                self.screen.blit(surface, (x+(size+spacing)*index-size/4, y-size/64))
            font = pygame.font.Font(pygame.font.get_default_font(), size)
            text_sur = font.render(str(char), True, color_)
            self.screen.blit(text_sur, (x+(size+spacing)*index, y))
            index+=1
            
    def key_check(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.now_row <= 6:
                self.press_key_ = ""
                if event.key == pygame.K_LSHIFT:
                    self.reset()
                if event.key == pygame.K_RETURN:
                    
                    
                    
                    if len(self.text) == 5 and find(self.text):
                        writein(self.text, self.map, self.now_row)
                        index = 0
                        for c in self.text:
                            self.correct[self.now_row][index]=0
                            poso = find_letter_in(c, self.text)
                            pos = find_letter_in(c, self.answer)
                            posoo = find_letter_in(c, self.text)
                            if len(pos)>0:
                                for i in poso:
                                    if i in pos:
                                        self.correct[self.now_row][i]=1
                                        posoo.remove(i)
                                        pos.remove(i)
                                        if not(c in self.letters0):
                                            self.letters0.append(str(c))
                                for i in posoo:
                                    if len(pos)>0:
                                        self.correct[self.now_row][i]=2
                                        pos.pop()
                                        print(pos)
                                        if not(c in self.letters1) and not(c in self.letters0):
                                            self.letters1.append(str(c))
                            else:
                                self.correct[self.now_row][index]=3
                                self.letters3.append(str(c))
                            index+=1
                    
                        if str(self.text) == str(self.answer[:-1]):
                            self.listen_to_keys = False
                            self.done = "win"
                            print(self.done)
                            print("yes")
                        elif self.now_row==5:
                            self.listen_to_keys = False
                            self.done = "lost"
                            print("no")
                        self.text = ""
                        self.now_row+=1
                        
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode:
                    if len(self.text) < 5 and 97<=ord(event.unicode.lower()) and ord(event.unicode.lower())<=122:
                        # print(int(event.unicode))
                        self.text += event.unicode
                        self.press_key_ = event.unicode
    
    def render(self):
        self.screen.fill((0,0,0))
        
        
        black_transp = pygame.Surface(self.screen.get_size())
        black_transp.set_alpha(128)
        black_transp.fill((0,0,0))
        self.screen.blit(black_transp, (0,0))
        
        
        print_list = [[],[],[],[],[],[]]
        for words in range(0, 6):
            print_list[words] = self.map[words][0]+self.map[words][1]+self.map[words][2]+self.map[words][3]+self.map[words][4]
        
        # print(print_list)
        # font = pygame.font.Font(None, 64)
        for row in range(0,6):
            self.draw_text(print_list[row], 15, 45, 25+90*row, 80, row)
            # text_sur = font.render(str(print_list[row]), True, (255,255,255))
            # self.screen.blit(text_sur, (50, 50+64*row))
        
        self.draw_text(self.text, 15, 45, 25+90*self.now_row, 80, self.now_row, mode="front")
        # text_sur = font.render(self.text, True, (255,255,255))
        # self.screen.blit(text_sur, (50, 50+64*self.now_row))
        surface = pygame.Surface((50,50))
        for i in range(97, 107):
            # surface = pygame.Rect(10+50*(i-97)-15, 550-10, 50, 50)
            
            color = (100,100,100)
            if chr(i) in self.letters0:
                color = (100,255,100)
            elif chr(i) in self.letters1:
                color = (172,205,22)
            elif chr(i) in self.letters3:
                color = (50,50,50)
            if chr(i)==self.press_key_:
                color = (25,25,25)
                surface.set_alpha(1000)
            else:
                surface.set_alpha(150)
                
            surface.fill(color)
            
            self.screen.blit(surface, (10+50*(i-97)-15, 550-10))
            
            # pgyame.draw.rect(self.screen, color, surface)
            
            self.draw_text(chr(i), 0, 10+50*(i-97), 550, 40, mode="front")
            
        for i in range(107, 117):
            # surface = pygame.Rect(10+50*(i-107)-15, 600-10, 50, 50)
            color = (100,100,100)
            if chr(i) in self.letters0:
                color = (100,255,100)
            elif chr(i) in self.letters1:
                color = (172,205,22)
            elif chr(i) in self.letters3:
                color = (50,50,50)
            if chr(i)==self.press_key_:
                color = (25,25,25)
                surface.set_alpha(1000)
            else:
                surface.set_alpha(150)
                
            surface.fill(color)
            
            self.screen.blit(surface, (10+50*(i-107)-15, 600-10))
            
            self.draw_text(chr(i), 0, 10+50*(i-107), 600, 40, mode="front")
            
        for i in range(117, 123):
            # surface = pygame.Rect(10+50*(i-117)-15, 650-10, 50, 50)
            color = (100,100,100)
            if chr(i) in self.letters0:
                color = (100,255,100)
            elif chr(i) in self.letters1:
                color = (172,205,22)
            elif chr(i) in self.letters3:
                color = (50,50,50)
            if chr(i)==self.press_key_:
                color = (25,25,25)
                surface.set_alpha(1000)
            else:
                surface.set_alpha(150)
                
            surface.fill(color)
            
            self.screen.blit(surface, (10+50*(i-117)-15, 650-10))
                
            self.draw_text(chr(i), 0, 10+50*(i-117), 650, 40, mode="front")
        blit_screen = pygame.transform.scale(self.screen, (pygame.display.get_window_size()[1]/self.height*self.width, pygame.display.get_window_size()[1])) 
        self.window.blit(blit_screen, (pygame.display.get_window_size()[0]/2 - pygame.display.get_window_size()[1]/self.height*self.width/2,0))
            
            
        pygame.display.update()

    def main_loop(self):
        while(True):
            while(self.listen_to_keys):
                self.key_check()
                self.render()
            if self.done=="lost":
                self.draw_text(self.done+" ans: "+self.answer[:-1], 0, 10, 480, 30, 0, mode="front", color_=(255,100,100))
            else:
                self.draw_text(self.done+" ans: "+self.answer[:-1], 0, 10, 480, 30, 0, mode="front", color_=(255,255,255))
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                if event.type==pygame.KEYDOWN:
                    self.reset()
            blit_screen = pygame.transform.scale(self.screen, (pygame.display.get_window_size()[1]/self.height*self.width, pygame.display.get_window_size()[1])) 
            self.window.blit(blit_screen, (pygame.display.get_window_size()[0]/2 - pygame.display.get_window_size()[1]/self.height*self.width/2,0))
            pygame.display.update()
            
if __name__ == "__main__":
    app = main(500,700)
