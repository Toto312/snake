import sys
import random

import pygame

from font import Font
from grid import real_position
import sprite
from snake import Snake

class Game:
    def __init__(self,width=None, height=None):
        pygame.init()
        self.snake_clock = pygame.time.get_ticks()
        self.FPS = 60

        self.clock = pygame.time.Clock()

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

        
        self.snake = Snake([self.width,self.height])

        self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.block_size = 38
        self.x_max = max(round(self.width/self.block_size)-1,0)
        self.y_max = max(round(self.height/self.block_size)-1,0)
        

        self.game_over = Font("Resources/PixeloidSans.ttf", "Game over. Press \"r\" to play again", False,35)
        self.resume = Font("Resources/PixeloidSans.ttf", "Press \"p\" to resume the game", False)
        self.score_title = Font("Resources/PixeloidSans.ttf", "Score: {0}".format(self.score), False,35)

        self.apple = pygame.sprite.Group()
        self.color_apple=(224,113,113)

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
            self.snake.is_paused = True
            self.is_paused = True
            print("Won")
            return

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
        self.is_paused, self.is_dead = self.snake.check_collision()

        if(pygame.sprite.spritecollide(self.snake.head,self.apple,False)):
            self.score += 1
            self.snake.increment_body()
            self.change_apple_position()
            self.score_title.update_text("Score: {0}".format(self.score))

    def mainloop(self):
        while(True):
            dt = self.clock.tick(self.FPS)/1000

            #Manage system events and keys
            self.manage_keys()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if(event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_p:
                        self.snake.is_paused = not self.snake.is_paused
                        self.is_paused = not self.is_paused
                    
                    elif(event.key == pygame.K_q):
                        pygame.quit()
                        sys.exit()

            self.check_collision()
            self.snake.update(dt)

            self.screen.fill((0,0,0))
            self.apple.draw(self.screen)
            self.snake.snake_body.draw(self.screen)
            
            if(self.is_paused and not self.is_dead):
                self.resume.render(self.screen, real_position([self.x_max/2*1.02,(self.y_max/2)*1.75]))
            elif(self.is_dead):
                self.game_over.render(self.screen, real_position([self.x_max/2,(self.y_max/2)*1.75]))
            
            self.score_title.render(self.screen,real_position([self.x_max*0.8,1]))

            pygame.display.update()

    def restart(self):
        print("si")
        self.apple.empty()
        self.init_apple()
        self.snake.restart()
        self.score = 0

        self.is_paused = True

    def manage_keys(self):
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_d]):
            self.snake.change_direction([1,0])
        elif(keys[pygame.K_a] ):
            self.snake.change_direction([-1,0])
        elif(keys[pygame.K_w]):
            self.snake.change_direction([0,-1])
        elif(keys[pygame.K_s]):
            self.snake.change_direction([0,1])
        elif(keys[pygame.K_r]):
            if(self.is_dead):
                self.restart()
                self.snake.is_dead = False
                self.is_dead = False
        
    def init(self):
        self.init_apple()
        self.snake.init()

    def real_position(self,coord):
        return [coord[0]*self.block_size,coord[1]*self.block_size]

if(__name__=="__main__"):
    g = Game()
    g.init()
    g.mainloop()