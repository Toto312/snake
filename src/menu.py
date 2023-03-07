import pygame
import font
import states
from grid import real_position
import sys

class Menu:
    def __init__(self,state,window):
        self.buttons = []

        self.screen = pygame.display.get_surface()

        self.state = state
        self.window = window

        self.option_selected=0

        self.keys_delay = pygame.time.get_ticks()

    def init(self):
        play_button = font.Font("Resources/PixeloidSans.ttf", \
            "PLAY «",
            real_position([self.window.x_max*0.135,self.window.y_max*0.2]),
            True
            )

        option_button = font.Font("Resources/PixeloidSans.ttf", \
            "OPTIONS",
            real_position([self.window.x_max*0.15,self.window.y_max*0.35]),
            True
            )

        exit_button = font.Font("Resources/PixeloidSans.ttf", \
            "EXIT",
            real_position([self.window.x_max*0.1,self.window.y_max*0.5]),
            True
            )

        self.buttons.extend([play_button,option_button,exit_button])

        #

    def show_sprites(self):
        if(not self.state.ret_values("is_in_menu")):
            return
        for i in self.buttons:
            i.render(self.screen)

    def font_selected(self,font):
        for i in self.buttons:
            if(i.text==font.text):
                font.update_text(font.text+" «")
    
    def deselect_fonts(self,index):
        self.buttons[index].update_text(self.buttons[index].text[:-2])

    def manage_keys(self,key):
        if(pygame.time.get_ticks()-self.keys_delay<100):
            return
        self.keys_delay = pygame.time.get_ticks()



        if(key[pygame.K_DOWN] and self.option_selected<2):
            self.deselect_fonts(self.option_selected)
            self.option_selected +=1
            self.font_selected(self.buttons[self.option_selected])
        elif(key[pygame.K_UP] and self.option_selected>0):
            self.deselect_fonts(self.option_selected)
            self.option_selected -=1
            self.font_selected(self.buttons[self.option_selected])

        elif(key[pygame.K_RETURN]):
            if(self.option_selected==0):
                self.state.change_values(is_paused=True,has_started=True,is_in_menu=False)
            elif(self.option_selected==1):
                self.state.change_values(is_on_options=True)
            elif(self.option_selected==2):
                pygame.quit()
                sys.exit()

