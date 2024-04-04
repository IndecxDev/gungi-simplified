import pygame
from ..constants import PANEL_BORDER_THICKNESS, PANEL_BORDER_COLOR, PANEL_COLOR

class Panel:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, window):
        pygame.draw.rect(window, PANEL_BORDER_COLOR, (self.x - PANEL_BORDER_THICKNESS, self.y - PANEL_BORDER_THICKNESS, self.width + 2 * PANEL_BORDER_THICKNESS, self.height + 2 * PANEL_BORDER_THICKNESS), PANEL_BORDER_THICKNESS, 5)
        pygame.draw.rect(window, PANEL_COLOR, (self.x, self.y, self.width, self.height))