import pygame
import sprite

class Snake:
    def __init__(self,color=None,block_size=None):

        #Get default color
        self.color = (225,225,225)
        if(color):
            self.color = color
        #get default block size
        self.block_size = 38
        if(block_size):
            self.block_size = block_size

        self.screen = pygame.display.get_surface()
        self.snake_body = pygamesprite.Group()

        #direction where the snake is moving with normalized distance
        #The distance to move depends of the block size
        self.direction = [-1,0]

    def init(self,pos=None):
        sprite = sprite.Sprite(self.color, self.block_size)
        if(pos):
            sprite.change_values(pos)
        else:
            sprite.change_values([9,9])
        self.snake_body.add(sprite)

    def update():
        pass
