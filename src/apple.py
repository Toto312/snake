import pygame
from sprite import Sprite
import grid
import random

class Apple:
    def __init__(self,window):
        self.color = (224,113,113)

        self.window = window

        self.width = window.width
        self.height = window.height

        self.block_size = window.block_size
        self.apple_body = pygame.sprite.GroupSingle()
    def init(self):
        position = self.check_posibilities()
        apl = Sprite(self.color,self.block_size)
        apl.change_values(position)
        self.apple_body.add(apl)
    def change_position(self,snake):
        position = self.check_posibilities(snake)
        self.apple_body.sprite.change_values(position)
    def check_collision(self,sprite):
        if(pygame.sprite.spritecollide(sprite,self.apple_body,False)):
            return True
        return False
    def check_posibilities(self,snake=None):
        if(len(self.apple_body)==1):
            not_posibilities = [self.apple_body.sprite.rect[0:2]]
        else:
            not_posibilities = []
        
        if(snake):
            for i in snake:
                not_posibilities.append(i.rect[0:2])

        for i in range(20):
            rand = [random.randint(0,self.window.x_max),random.randint(0,self.window.y_max)]
            if(not not_posibilities):
                return grid.real_position(rand)
            is_it_equal = False
            for j in not_posibilities:
                if(j == grid.real_position(rand)):
                    is_it_equal = True
            if(is_it_equal==False):
                return grid.real_position(rand)

    def restart(self):
        self.init()
if(__name__=="__main__"):
    pass