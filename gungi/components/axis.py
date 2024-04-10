from .text import Text
from ..constants import XOFFSET, YOFFSET, BLACK, BACKGROUND_COLOR

class Axis:
    def __init__(self) -> None:
        self.x1 = XOFFSET - 25
        self.y1 = YOFFSET + 50
        self.x2 = XOFFSET + 50
        self.y2 = YOFFSET + 930
        self.axis1 = "abcdefghi"
        self.axis2 = "123456789"
        self.axis1_array = []
        self.axis2_array = []
    
    def draw(self, window, mouse_pos):
        x1 = self.x1
        y1 = self.y1
        x2 = self.x2
        y2 = self.y2
        for char in self.axis1:
            char_text = Text(char, 1)
            char_text.draw(window, x1, y1, BLACK, BACKGROUND_COLOR)
            y1 += 100
        for num in self.axis2:
            num_text = Text(num, 1)
            num_text.draw(window, x2, y2, BLACK, BACKGROUND_COLOR)
            x2 += 100
        
        