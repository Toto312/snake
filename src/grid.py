import pygame
#TODO: make a class called window so it can handle the real position, including when the windows is resized
#also make a grid class to handle position
def real_position(coord):
    return [coord[0]*38,coord[1]*38]

class Vector:
    def __init__(self,values):
        self.x = values[0]
        self.y = values[1]
    def __add__(self,vector):
        self.x += vector.x
        self.y = vector.y


if(__name__=="__main__"):
    pass