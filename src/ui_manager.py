import pygame

class UIManager:
    def __init__(self,state):
        #fonts in UIManager, its an 2d array
        self.fonts = []
        self.screen = pygame.display.get_surface()
        self.state = state

    def add_font(self,font,what_state_activate):
        self.fonts.append([font,what_state_activate])

    def change_name(self,font,name):
        for i in self.fonts:
            if(i[0].text == font.text):
                i[0].text = name[:]

    def show_fonts(self):
        for i in self.fonts:
            if(i[1] == "always"):
                i[0].render(self.screen)

            elif(i[1].ret_values("all") == self.state.ret_values("all")):
                i[0].render(self.screen)