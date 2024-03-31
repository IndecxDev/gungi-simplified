import pygame
from .button import Button
from .constants import *


class Panel:
    def __init__(self, window) -> None:
        self.window = window
        self.offset = 1000 # Horizontal offset from the board

        self._init_buttons()

    def _init_buttons(self):
        self.buttons = {
            "New Game": Button(self.offset, 50, 60, 60, "New Game", "", ICON_RESET),
            "Text Button": Button(self.offset, 140, 220, 60, "Test", "Test Text", None)
        }

    def update(self, mousePos):
        for button_name, button in self.buttons.items():
            button.draw(self.window, mousePos)

    def click_panel(self, mousePos, game):
        for button_name, button in self.buttons.items():
            if mousePos[0] >= button.x and mousePos[0] < button.x + button.width and mousePos[1] >= button.y and mousePos[1] < button.y + button.height:
                button.click(button_name, game)
    
    def deselect(self):
        for button_name, button in self.buttons.items():
            button.deselect()

    