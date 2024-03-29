import pygame

class Font:
    def __init__(self,type_font,text,is_strong,size=None):
        self.type_font = type_font
        self.size = size
        self.text = text
        if(size):
            self.size = size
        else:
            self.size = 40
        self.font = pygame.freetype.Font(self.type_font, self.size)
        self.rect = self.font.get_rect(self.text)
        self.is_strong = False
        if(is_strong):
            self.font.strong = True
        else:
            self.font.strong = False
    def update_text(self,text):
        self.text = text
        self.rect = self.font.get_rect(self.text)
    def render(self,screen,position):
        self.rect.center = position
        self.font.render_to(screen, self.rect.bottomleft, self.text,(255,255,255))