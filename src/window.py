import pygame

class Window:
    def __init__(self,resolution,is_resizable):
        self.width = 760
        self.height = 760
        self.block_size = 38
        self.is_resizable = is_resizable
        #rigth now we need the resolution in x and y be the same
        if(resolution and resolution[0] == resolution[1]):
            self.block_size *= round(resolution[0]/760)
            self.width = resolution[0]
            self.height = resolution[1]

        if(is_resizable):
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))
        self.x_max = max(round(self.width/self.block_size)-1,0)
        self.y_max = max(round(self.height/self.block_size)-1,0)

    def screen_surface(self):
        return self.screen
    def change_screen_size(self,width,height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        self.block_size *= round(resolution[0]/760)

        self.x_max = max(round(self.width/self.block_size)-1,0)
        self.y_max = max(round(self.height/self.block_size)-1,0)