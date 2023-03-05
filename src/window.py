import pygame

class Window:
    def __init__(self,resolution):
        self.width = 760
        self.height = 760
        self.block_size = 38
        #rigth now we need the resolution in x and y be the same
        if(resolution and resolution[0] == resolution[1]):
            self.block_size *= round(resolution[0]/760)
            self.width = resolution[0]
            self.height = resolution[1]

        self.screen = pygame.display.set_mode((self.width, self.height))

        self.x_max = max(round(self.width/self.block_size)-1,0)
        self.y_max = max(round(self.height/self.block_size)-1,0)

    def screen_surface(self):
        return self.screen