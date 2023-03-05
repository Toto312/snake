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
import window

class Game:
    def __init__(self,resolution=None):
        pygame.init()

        self.FPS = 60
        self.snake_clock = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.restart_clock=0

        self.score = 0

        self.state = states.StateGame(is_dead=False, is_paused=True, has_restarted=True, is_snake_incrementing=False)
        self.windows = window.Window(resolution,is_resizable=True)
        self.ui = ui_manager.UIManager(self.state)
        
        self.snake = Snake(self.windows,self.state)
        self.apple = Apple(self.windows)

    def check_collision(self):
        if(self.snake.does_collided()):
            self.state.change_values(is_dead=True, is_paused=True)
        if(self.apple.check_collision(self.snake.head)):
            self.score += 1
            self.apple.change_position(self.snake.sprites())
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
                        self.state.change_values(is_paused= not self.state.is_paused)
                    elif(event.key == pygame.K_q):
                        pygame.quit()
                        sys.exit()

            self.check_collision()
            self.snake.update()

            #
            #   Draw
            #
            #restart background
            self.windows.screen.fill((0,0,0))
            #draw sprites
            self.apple.apple_body.draw(self.windows.screen)
            self.snake.snake_body.draw(self.windows.screen)
            
            #
            #   UI draw
            #
            self.ui.show_fonts()


            pygame.display.update()

    def restart(self):
        self.state.change_values(has_restarted=True)

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
        if(not self.state.ret_values("is_paused")):

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
            real_position([self.windows.x_max/2,(self.windows.y_max/2)*1.75]),
            False,
            35)

        self.resume = Font("Resources/PixeloidSans.ttf", \
            "Press \"p\" to resume the game", 
            real_position([self.windows.x_max/2*1.02,(self.windows.y_max/2)*1.75]),
            False
            )

        self.score_title = Font("Resources/PixeloidSans.ttf", \
            "Score: {0}".format(self.score),
            real_position([self.windows.x_max*0.8,1]),
            False,
            35
            )

        self.fps_show = Font("Resources/PixeloidSans.ttf", \
            "Fps: {0}".format(self.clock.get_fps()),
            real_position([self.windows.x_max*0.2,1]),
            False)

        self.ui.add_font(self.game_over,states.StateGame(is_dead=True, is_paused=True,is_snake_incrementing=False,has_restarted=True))
        self.ui.add_font(self.resume,states.StateGame(is_dead=False, is_paused=True,is_snake_incrementing=False,has_restarted=True))
        self.ui.add_font(self.score_title,"always")
        self.ui.add_font(self.fps_show,"always")

if(__name__=="__main__"):
    g = Game()
    g.init_sprites()
    g.mainloop()