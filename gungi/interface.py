from .components.button import Button
from .components.stacker import Stacker
from .components.text import Text
from .components.image import Image
from .components.movelog import MoveLog
from .constants import ICON_RESET, XOFFSET, YOFFSET, ICON_DOWNLOAD, ICON_UPLOAD, ICON_MAKE_MOVE, ICON_MAKE_MOVES
from .game import Game
import copy
import tkinter

# Basically the framework for the UI elements
class Interface:
    def __init__(self, window) -> None:
        self.window = window
        self.offset = 900 + 2 * XOFFSET # Horizontal offset from the board

        self._init_components()

    def _init_components(self):
        self.components = {
            "New Game": Button(self.offset + 20, YOFFSET + 840, 60, 60, "New Game", Text("New Game", 18), Image(ICON_RESET)),
            "Stacker": Stacker(self.offset, YOFFSET + 300, 100, 300, "Stack"),
            "Move Log": MoveLog(self.offset + 150, YOFFSET + 150, 400, 600, "Move Log"),
            "Make Random Move": Button(self.offset + 270, YOFFSET + 840, 60, 60, "Random Move", Text("Random Move", 18), Image(ICON_MAKE_MOVE)),
            "X Random Moves": Button(self.offset + 360, YOFFSET + 840, 60, 60, "X Random Moves", Text("10 Moves", 18), Image(ICON_MAKE_MOVES)) 
        }

    def update(self, mousePos):
        for name, component in self.components.items():
            component.draw(self.window, mousePos)     

    def click_interface(self, mousePos, game: Game):
        for name, component in self.components.items():
            if type(component) is Button:
                if mousePos[0] >= component.x and mousePos[0] < component.x + component.width and mousePos[1] >= component.y and mousePos[1] < component.y + component.height:
                    component.click(component.function, game)
            if type(component) is Stacker:
                pieces = []
                current_piece = game.selected
                if current_piece != "--":
                    layer = current_piece.layer
                    while layer >= 0:
                        pieces.append(game.board.get_piece(game.selected.row, game.selected.column, layer))
                        layer -= 1
                component.pieces = copy.deepcopy(pieces)
    
    def deselect(self):
        for name, component in self.components.items():
            if type(component) is Button:
                component.deselect()

    def right_click(self):
        for name, component in self.components.items():
            if type(component) is Stacker:
                component.deselect()

    