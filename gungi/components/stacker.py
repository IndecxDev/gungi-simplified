from .panel import Panel
from .image import Image
from .text import Text
from ..constants import BLACK, BACKGROUND_COLOR, ICON_LAYERS

class Stacker:
    def __init__(self, x:int, y:int, width:int, height:int, text: str) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pieces = []
        self.text = text
    
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
        else:
            image = Image(ICON_LAYERS)
            image.draw(window, self.x + self.width // 2 - 30, self.y + self.height // 2 - 30)
        text = Text(self.text, 1)
        text.draw(window, self.x + self.width // 2, self.y - 30, BLACK, BACKGROUND_COLOR)

    def deselect(self):
        self.pieces = []
