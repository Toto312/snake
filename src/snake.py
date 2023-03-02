import pygame
import sprite
import grid

class Snake:
    def __init__(self,window_size,block_size=38):
        #Get default color
        self.color = (225,225,225)
        #get default block size
        self.block_size = block_size
        
        self.width = window_size[0]
        self.height = window_size[1]

        self.screen = pygame.display.get_surface()
        self.snake_body = pygame.sprite.Group()

        self.update_clock = pygame.time.get_ticks()

        #direction where the snake is moving with normalized distance
        #The distance to move depends of the block size
        self.direction = [-1,0]

        self.is_paused = False
        self.is_dead = False

        self.sprite_to_add = None

    def init(self,pos=None):
        sprites = sprite.Sprite(self.color, self.block_size)
        if(pos):
            sprites.change_values(grid.real_position(pos))
        else:
            sprites.change_values(grid.real_position([9,9]))
        self.snake_body.add(sprites)
        self.head = self.snake_body.sprites()[0]

    def increment_body(self):
        sprites = sprite.Sprite(self.color, self.block_size)
        pos = self.snake_body.sprites()[-1].rect[0:2]
        sprites.change_values(pos)

        self.sprite_to_add = sprites

    def move(self):
        if(self.is_paused):
            return

        last_pos = self.head.rect[0:2]

        self.head.change_values(grid.real_position(self.direction),True)
            
        for i in range(len(self.sprites())-1):
            i+=1
            actual_pos = self.snake_body.sprites()[i].rect[0:2]
            self.snake_body.sprites()[i].change_values(last_pos)

            last_pos = actual_pos[:]

    def update(self,dt):
        if(pygame.time.get_ticks()-self.update_clock<10000*dt):
            return
        self.update_clock = pygame.time.get_ticks()

        if(self.sprite_to_add):
            self.snake_body.add(self.sprite_to_add)
            self.sprite_to_add = None

        self.move()

    def check_collision(self):
        if(self.head.rect.x < 0 or self.head.rect.x > self.width or \
            self.head.rect.y < 0 or self.head.rect.y > self.height):
            self.is_paused = True
            self.is_dead = True
        if(len(pygame.sprite.spritecollide(self.head,self.snake_body,False))!=1):
            self.is_paused = True
            self.is_dead = True
        return [self.is_paused,self.is_dead]
    
    def set_states(self,is_paused,is_dead):
        self.is_paused = is_paused
        self.is_dead = is_dead

    def restart(self):
        self.snake_body.empty()
        self.init()

    def change_direction(self,new_direction):
        if(new_direction[0] == -self.direction[0] or \
            new_direction[1] == -self.direction[1]):
            return
        
        self.direction = new_direction
  
    def sprites(self):
        return self.snake_body.sprites()

if(__name__=="__main__"):
    pass