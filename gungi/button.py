import pygame
from .constants import *
from .game import Game

class Button:
    
    def __init__(self, x, y, width, height, function, text, image) -> None:
        self.font = pygame.font.Font("assets/coolvetica.otf", 30)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.function = function
        self.text = text
        self.image = image

        self.clicked = False
    
    def draw(self, window, mousePos):
        # Border
        pygame.draw.rect(window, BUTTON_BORDER_COLOR, (self.x - BUTTON_BORDER_THICKNESS, self.y - BUTTON_BORDER_THICKNESS, self.width + 2 * BUTTON_BORDER_THICKNESS, self.height + 2 * BUTTON_BORDER_THICKNESS), BUTTON_BORDER_THICKNESS, 5)
        
        # Body
        if self.clicked:
            body_color = BUTTON_CLICKED_COLOR
        elif mousePos[0] >= self.x and mousePos[0] < self.x + self.width and mousePos[1] >= self.y and mousePos[1] < self.y + self.height:
            body_color = BUTTON_HIGHLIGHTED_COLOR
        else:
            body_color = BUTTON_COLOR
            self.deselect()
        pygame.draw.rect(window, body_color, (self.x, self.y, self.width, self.height))

        # Text
        if self.text != "":
            text = self.font.render(self.text, True, BLACK, body_color)
            textRect = text.get_rect()
            textRect.center = (self.width // 2 + self.x, self.height // 2 + self.y)
            window.blit(text, textRect)
        
        # Image
        if self.image != None:
            window.blit(ICON_RESET, (self.x, self.y))

    def click(self, button_name, game: Game):
        self.clicked = True

        if button_name == "New Game":
            game.reset()

    def deselect(self):
        self.clicked = False