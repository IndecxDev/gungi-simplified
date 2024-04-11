from .button import Button
from .text import Text
from .image import Image
from .panel import Panel
from ..game import Game
from ..constants import ICON_CLOSE, BLACK, DARK_COLOR, GREY

class Ending:
    def __init__(self, x, y, width, height, game: Game) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.game = game
        self.closed = False
        self.close_button = Button(self.x + 320, self.y + 20, 60, 60, "Close Ending", None, Image(ICON_CLOSE))
    
    def draw(self, window, mouse_pos):
        if self.game.checkmated_state is not None and not self.closed: # Game has ended
            panel = Panel(self.x, self.y, self.width, self.height)
            panel.draw(window)
            self.close_button.draw(window, mouse_pos)

            game_over_text = Text("Game Over", 1)
            game_over_text.draw(window, self.x + self.width // 2, self.y + 50, BLACK, DARK_COLOR)
            
            state = Text(f"{self.game.game_message}", 1)
            state.draw(window, self.x + self.width // 2, self.y + self.height // 2 + 30, BLACK, DARK_COLOR)
    
    def reset(self):
        self.closed = False
        self.close_button.deselect()