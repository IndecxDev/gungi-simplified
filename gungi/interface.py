from .components.button import Button
from .components.stacker import Stacker
from .components.text import Text
from .components.image import Image
from .constants import ICON_RESET, XOFFSET, YOFFSET
from .game import Game
import copy

class Interface:
    def __init__(self, window) -> None:
        self.window = window
        self.offset = 900 + 2 * XOFFSET # Horizontal offset from the board

        self._init_components()

    def _init_components(self):
        self.components = {
            "New Game": Button(self.offset, YOFFSET, 60, 60, "New Game", None, Image(ICON_RESET)),
            "Text Button": Button(self.offset, YOFFSET + 100, 220, 60, "Text Smaller", Text("Test Text", 30), None),
            "Stacker": Stacker(self.offset, YOFFSET + 300, 100, 300) 
        }

    def update(self, mousePos):
        for component_name, component in self.components.items():
            component.draw(self.window, mousePos)
            

    def click_interface(self, mousePos, game: Game):
        for component_name, component in self.components.items():
            if type(component) is Button:
                if mousePos[0] >= component.x and mousePos[0] < component.x + component.width and mousePos[1] >= component.y and mousePos[1] < component.y + component.height:
                    component.click(component_name, component.function, game)
            if type(component) is Stacker:
                pieces = []
                current_piece = game.selected
                if current_piece != "--":
                    layer = current_piece.layer
                    while layer >= 0:
                        pieces.append(game.board.get_piece(game.selected.row, game.selected.column, layer))
                        layer -= 1
                component.update_pieces(copy.deepcopy(pieces))
    
    def deselect(self):
        for component_name, component in self.components.items():
            if type(component) is Button:
                component.deselect()

    def right_click(self):
        for component_name, component in self.components.items():
            if type(component) is Stacker:
                component.deselect()

    