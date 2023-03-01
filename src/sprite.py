import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self,color,block_size):
        super().__init__()

        self.image = pygame.Surface([block_size*0.9, block_size*0.9])
        self.image.fill(color)
  
        self.rect = self.image.get_rect()

    def change_values(self,coord,relative=False):
        if(relative):
            self.rect.x += coord[0]
            self.rect.y += coord[1]
        else:
            self.rect.x = coord[0]
            self.rect.y = coord[1]
