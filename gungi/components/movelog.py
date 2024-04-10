from .text import Text
from .image import Image
from .panel import Panel
from ..constants import BLACK, BACKGROUND_COLOR

class MoveLog:
    def __init__(self, x: int, y: int, width: int, height:int, description_text: str) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.description_text = description_text
        self.moves = []
    
    def update_moves(self):
        pass

    def clear_moves(self):
        pass

    def draw(self, window, mouse_pos):
        panel = Panel(self.x, self.y, self.width, self.height)
        panel.draw(window)
        text = Text(self.description_text, 30)
        text.draw(window, self.x + self.width // 2, self.y - 30, BLACK, BACKGROUND_COLOR)
