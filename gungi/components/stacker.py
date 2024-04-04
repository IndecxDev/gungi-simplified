import pygame
from .panel import Panel
from .image import Image
from ..constants import *

class Stacker:
    def __init__(self, x:int, y:int, width:int, height:int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pieces = []
    
    def draw(self, window, mousePos):
        panel = Panel(self.x, self.y, self.width, self.height)
        panel.draw(window)
        if self.pieces != []:
            layer = len(self.pieces)
            for piece in self.pieces:
                piece.x = self.x
                piece.y = self.y + self.height - layer * 100
                piece.layer = layer - 1
                layer -= 1
                piece.draw(window)

    def update_pieces(self, pieces):
        self.pieces = pieces

    def deselect(self):
        self.pieces = []
