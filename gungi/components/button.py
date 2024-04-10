import pygame
from ..constants import BUTTON_BORDER_COLOR, BUTTON_BORDER_THICKNESS, BUTTON_CLICKED_COLOR, BUTTON_COLOR, BUTTON_HIGHLIGHTED_COLOR, BLACK, BACKGROUND_COLOR, GREY
from ..game import Game
from .text import Text
from .image import Image
from .movelog import MoveLog

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, function: str, text_object: Text, image_object: Image) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.function = function
        self.text_object = text_object
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
                center_x, center_y = self.width // 2 + self.x, self.y - 22
                self.text_object.draw(window, center_x, center_y, BLACK, BACKGROUND_COLOR)
        
        # Image
        if self.image_object != None:
            self.image_object.draw(window, self.x, self.y)

    def click(self, button_function, game: Game, components: dict):
        # Doing stuff based on each button's function
        self.clicked = True

        if button_function == "New Game":
            game.reset()
        elif button_function == "Random Move":
            if game.checkmated_state == None:
                game.make_random_move()
            elif game.checkmated_state == GREY:
                print("Draw, cannot make a move.")
            else:
                print(game.color_to_string(game.checkmated_state) + " checkmated, cannot make a move.")
            # Update Move log
            components["Move Log"].update_text(game)
        elif button_function == "X Random Moves":
            for i in range(10):
                if game.checkmated_state == None:
                    game.make_random_move()
                elif game.checkmated_state == GREY:
                    print("Draw, cannot make a move.")
                    break
                else:
                    print(game.color_to_string(game.checkmated_state) + " checkmated, cannot make a move.")
                    break
            # Update Move log
            components["Move Log"].update_text(game)
        elif button_function == "Download":
            pass
        elif button_function == "Upload":
            pass

    def deselect(self):
        self.clicked = False