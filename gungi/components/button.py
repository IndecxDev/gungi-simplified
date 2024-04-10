import pygame
from ..constants import BUTTON_BORDER_COLOR, BUTTON_BORDER_THICKNESS, BUTTON_CLICKED_COLOR, BUTTON_COLOR, BUTTON_HIGHLIGHTED_COLOR, BLACK, BACKGROUND_COLOR
from ..game import Game
from .text import Text
from .image import Image

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, function: str, text_object: Text, image_object: Image) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.function = function
        self.text_object = text_object
        if text_object != None:
            self.font = pygame.font.Font("assets/coolvetica.otf", self.text_object.size)
        self.image_object = image_object
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
        if self.text_object != None:
            if self.image_object == None:
                center_x, center_y = self.width // 2 + self.x, self.height // 2 + self.y
                self.text_object.draw(window, center_x, center_y, BLACK, body_color)
            else:
                center_x, center_y = self.width // 2 + self.x, self.y - self.text_object.size - 5
                self.text_object.draw(window, center_x, center_y, BLACK, BACKGROUND_COLOR)
        
        # Image
        if self.image_object != None:
            self.image_object.draw(window, self.x, self.y)

    def click(self, button_function, game: Game):
        # Doing stuff based on each button's function
        self.clicked = True

        if button_function == "New Game":
            game.reset()
        if button_function == "Text Smaller":
            self.text_object.change_font_size(self.text_object.size - 1)
        if button_function == "Random Move":
            if game.checkmated == None:
                game.make_random_move()
            else:
                print(str(game.checkmated) + " checkmated, cannot make a move.")
        if button_function == "Download":
            pass
        if button_function == "Upload":
            pass

    def deselect(self):
        self.clicked = False