import pygame
import sprite
import sys
import copy
import random
from font import Font
import math
from grid import real_position

class Game:
    pygame.init()

    def __init__(self,width=None, height=None):

        self.snake_clock = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.FPS = 60        
        self.is_paused = True
        self.is_dead = False
        self.score = 0
        
        """
            Things than doesnt need to be in this class
        """
        if(width):
            self.width = width
        if(height):
            self.height = height
        if(not width):
            self.width = 760
        if(not height):
            self.height = 760

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.block_size = 38
        
        self.game_over = Font("Resources/PixeloidSans.ttf", "Game over. Press \"r\" to play again", False,35)
        self.resume = Font("Resources/PixeloidSans.ttf", "Press \"p\" to resume the game", False)
        self.score_title = Font("Resources/PixeloidSans.ttf", "Score: {0}".format(self.score), False,35)
       
        self.snake = pygame.sprite.Group()
        self.apple = pygame.sprite.Group()

        self.x_max = max(round(self.width/self.block_size)-1,0)
        self.y_max = max(round(self.height/self.block_size)-1,0)

        self.color_snake=(225,225,225)
        self.color_apple=(224,113,113)

        self.snake_position = [-1,0]
        
        """
            ---------------------------------------------
        """

    def snake_update(self,dt):
        if(self.is_paused or self.is_dead):
            return

        if(pygame.time.get_ticks()-self.snake_clock<10*dt):
            return
        self.snake_clock = pygame.time.get_ticks()

        self.move_snake()
            
    def move_snake(self):
        head = self.snake.sprites()[0]

        last_pos = head.rect[0:2]

        head.change_values(real_position(self.snake_position),True)
            
        for i in range(len(self.snake.sprites())-1):
            i+=1
            actual_pos = self.snake.sprites()[i].rect[0:2]
            self.snake.sprites()[i].change_values(last_pos)

            last_pos = actual_pos[:]

    def change_apple_position(self):
        not_posibilites = [self.apple.sprites()[0].rect[0:2]]

        for i in self.snake.sprites():
            not_posibilites.append(i.rect[0:2])

        position=[]
        i=0
        while(True):
            if(i==100):
                break
            rand = [random.randint(0,self.x_max),random.randint(0,self.y_max)]
            
            if(not real_position(rand) in not_posibilites):
                position=rand
                break
            i+=1

        if(not position):
            self.is_paused = True
            print("Won")
            return
        
        """print(position)
        for i in not_posibilites:
            print(i[0]/38,i[1]/38)"""
        for i in self.apple:
            i.change_values(real_position(position))

    def init_apple(self):
        not_posibilites = []

        for i in self.snake.sprites():
            not_posibilites.append(i.rect[0:2])

        position=[]

        for i in range(20):
            rand = [random.randint(0,self.x_max),random.randint(0,self.y_max)]
            if(not [real_position(rand)] in not_posibilites):
                position = rand
                break
        
        apple = sprite.Sprite(self.color_apple, self.block_size)
        apple.change_values(real_position(position))
        self.apple.add(apple)

    def check_collision(self):
        head = self.snake.sprites()[0]
        if(head.rect.x < 0 or head.rect.x > self.width or \
            head.rect.y < 0 or head.rect.y > self.height):
            self.is_paused = True
            self.is_dead = True
        if(len(pygame.sprite.spritecollide(head,self.snake,False))!=1):
            self.is_paused = True
            self.is_dead = True
        if(pygame.sprite.spritecollide(head,self.apple,False)):
            self.score += 1
            self.createBlock(self.snake.sprites()[-1].rect[0:2], self.color_snake)
            self.change_apple_position()
            self.score_title.update_text("Score: {0}".format(self.score))

    def mainloop(self):
        while(True):
            dt = self.clock.tick(self.FPS)

            #Manage system events and keys
            self.manage_keys()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if(event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_p:
                        self.is_paused = not self.is_paused
                    
                    elif(event.key == pygame.K_q):
                        pygame.quit()
                        sys.exit()

            self.check_collision()
            self.snake_update(dt)
            self.screen.fill((0,0,0))
            self.apple.draw(self.screen)
            self.snake.draw(self.screen)

            if(self.is_paused and not self.is_dead):
                self.resume.render(self.screen, real_position([self.x_max/2*1.02,(self.y_max/2)*1.75]))
            elif(self.is_dead):
                self.game_over.render(self.screen, real_position([self.x_max/2,(self.y_max/2)*1.75]))
            
            self.score_title.render(self.screen,real_position([self.x_max*0.8,1]))

            pygame.display.update()

    def restart(self):
        self.apple.empty()
        self.snake.empty()
        self.init_sprites()
        self.score = 0
        self.is_paused = True

    def manage_keys(self):
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_d]):
            if(len(self.snake)>1 and self.snake_position == [-1,0]):
                return
            self.snake_position = [1,0]
        elif(keys[pygame.K_a] ):
            if(len(self.snake)>1 and self.snake_position == [1,0]):
                return
            self.snake_position = [-1,0]
        elif(keys[pygame.K_w]):
            if(len(self.snake)>1 and self.snake_position == [0,1]):
                return
            self.snake_position = [0,-1]
        elif(keys[pygame.K_s]):
            if(len(self.snake)>1 and self.snake_position == [0,-1]):
                return
            self.snake_position = [0,1]
        elif(keys[pygame.K_r]):
            if(self.is_dead):
                self.restart()
                self.is_dead = False

    def init_sprites(self):
        self.createBlock([9,9], self.color_snake)
        self.init_apple()

    def real_position(self,coord):
        return [coord[0]*self.block_size,coord[1]*self.block_size]

    def createBlock(self,coordenade,color):
        sprites = sprite.Sprite(color,self.block_size)
        sprites.change_values(real_position(coordenade))
        self.snake.add(sprites)

if(__name__=="__main__"):
    g = Game()
    g.init_sprites()
    g.mainloop()