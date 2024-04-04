import pygame

class Image:
    def __init__(self, image: pygame.surface) -> None:
        self.image = image
    
    def draw(self, window, x, y):
        if self.image != None:
            window.blit(self.image, (x, y))