import sys
import random
import time

import pygame

from font import Font
from grid import real_position
import sprite
from snake import Snake
from apple import Apple
import ui_manager
import states

class Game:
    def __init__(self,width=None, height=None):
        pygame.init()
        self.snake_clock = pygame.time.get_ticks()
        self.FPS = 60

        self.clock = pygame.time.Clock()
        self.restart_clock=0

        self.is_paused = True
        self.is_dead = False

        self.score = 0

        self.state = states.StateGame(self.is_dead, self.is_paused)

        """
            Things than doesnt need to be in this class
        """

        self.width = 760
        self.height = 760
        
        self.snake = Snake([self.width,self.height],self.state)
        self.apple = Apple([self.width,self.height])

        self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.block_size = 38
        self.x_max = max(round(self.width/self.block_size)-1,0)
        self.y_max = max(round(self.height/self.block_size)-1,0)

        self.ui = ui_manager.UIManager(self.state)

    def check_collision(self):
        if(self.snake.does_collided()):
            self.state.change_values(is_dead=True, is_paused=True)
        if(self.apple.check_collision(self.snake.head)):
            self.score += 1
            self.apple.change_position()
            self.snake.increment_body()
            self.ui.change_name(self.score_title,"Score: {0}".format(self.score))

    def mainloop(self):
        while(True):
            #
            #   Before draw
            #
            deltaT = self.clock.tick(self.FPS)

            self.ui.change_name(self.fps_show, "MS: {0}".format(round(1000/max(self.clock.get_fps(),1))))

            #Manage system events and keys
            self.manage_keys()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if(event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_p:
                        self.state.change_values(self.state.ret_isDead(), not self.state.is_paused)
                    elif(event.key == pygame.K_q):
                        pygame.quit()
                        sys.exit()

            self.check_collision()
            self.snake.update()

            #
            #   Draw
            #
            #restart background
            self.screen.fill((0,0,0))
            #draw sprites
            self.apple.apple_body.draw(self.screen)
            self.snake.snake_body.draw(self.screen)
            
            #
            #   UI draw
            #
            self.ui.show_fonts()


            pygame.display.update()

    def restart(self):
        self.state.change_restarted(has_restarted=True)

        if(pygame.time.get_ticks()-self.restart_clock < 500):
            return
        self.restart_clock = pygame.time.get_ticks()

        self.score = 0
        self.ui.change_name(self.score_title,"Score: {0}".format(self.score))

        self.apple.restart()
        self.snake.restart()

        self.snake.direction = [-1,0]

        self.state.change_values(is_dead=False, is_paused=True)

    def manage_keys(self):
        keys=pygame.key.get_pressed()

        # manage movement keys
        if(not self.state.ret_isPaused()):

            if(keys[pygame.K_d]):
                self.snake.change_direction([1,0])
            elif(keys[pygame.K_a] ):
                self.snake.change_direction([-1,0])
            elif(keys[pygame.K_w]):
                self.snake.change_direction([0,-1])
            elif(keys[pygame.K_s]):
                self.snake.change_direction([0,1])


        # manage misc keys
        if(keys[pygame.K_r]):
            self.restart()

    def init_sprites(self):
        self.apple.init()
        self.snake.init()
        
        self.game_over = Font("Resources/PixeloidSans.ttf", \
            "Game over. Press \"r\" to play again",
            real_position([self.x_max/2,(self.y_max/2)*1.75]),
            False,
            35)

        self.resume = Font("Resources/PixeloidSans.ttf", \
            "Press \"p\" to resume the game", 
            real_position([self.x_max/2*1.02,(self.y_max/2)*1.75]),
            False
            )

        self.score_title = Font("Resources/PixeloidSans.ttf", \
            "Score: {0}".format(self.score),
            real_position([self.x_max*0.8,1]),
            False,
            35
            )

        self.fps_show = Font("Resources/PixeloidSans.ttf", \
            "Fps: {0}".format(self.clock.get_fps()),
            real_position([self.x_max*0.2,1]),
            False)

        self.ui.add_font(self.game_over,states.StateGame(is_dead=True, is_paused=True))
        self.ui.add_font(self.resume,states.StateGame(is_dead=False, is_paused=True))
        self.ui.add_font(self.score_title,"always")
        self.ui.add_font(self.fps_show,"always")

if(__name__=="__main__"):
    g = Game()
    g.init_sprites()
    g.mainloop()