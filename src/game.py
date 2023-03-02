import sys
import random

import pygame

from font import Font
from grid import real_position
import sprite
from snake import Snake
from apple import Apple

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
        self.apple = Apple([self.width,self.height])

        self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.block_size = 38
        self.x_max = max(round(self.width/self.block_size)-1,0)
        self.y_max = max(round(self.height/self.block_size)-1,0)
        
        self.game_over = Font("Resources/PixeloidSans.ttf", "Game over. Press \"r\" to play again", False,35)
        self.resume = Font("Resources/PixeloidSans.ttf", "Press \"p\" to resume the game", False)
        self.score_title = Font("Resources/PixeloidSans.ttf", "Score: {0}".format(self.score), False,35)

    def check_collision(self):
        self.is_paused, self.is_dead = self.snake.check_collision()

        if(self.apple.check_collision(self.snake.head)):
            self.score += 1
            self.apple.change_position()
            self.snake.increment_body()
            self.score_title.update_text("Score: {0}".format(self.score))

    def mainloop(self):
        while(True):
            #
            #   Before draw
            #
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

            #
            #   After draw
            #
            self.screen.fill((0,0,0))
            self.apple.apple_body.draw(self.screen)
            self.snake.snake_body.draw(self.screen)
            
            #
            #   UI draw
            #
            if(self.is_paused and not self.is_dead):
                self.resume.render(self.screen, real_position([self.x_max/2*1.02,(self.y_max/2)*1.75]))
            elif(self.is_dead):
                self.game_over.render(self.screen, real_position([self.x_max/2,(self.y_max/2)*1.75]))
            
            self.score_title.render(self.screen,real_position([self.x_max*0.8,1]))



            pygame.display.update()

    def restart(self):
        self.apple.restart()
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
        
    def init_sprites(self):
        self.apple.init()
        self.snake.init()

    def real_position(self,coord):
        return [coord[0]*self.block_size,coord[1]*self.block_size]

if(__name__=="__main__"):
    g = Game()
    g.init_sprites()
    g.mainloop()