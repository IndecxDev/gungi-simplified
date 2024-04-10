from .text import Text
from .panel import Panel
from ..constants import BLACK, BACKGROUND_COLOR, DARK_COLOR
from ..game import Game

class MoveLog:
    def __init__(self, x: int, y: int, width: int, height:int, description_text: str, game: Game) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.description_text = description_text
        self.description_text_object = Text(self.description_text, 1)
        self.panel = Panel(self.x, self.y, self.width, self.height)
        self.texts = []
        self.moves = game.move_log
    
    def update_text(self, game: Game):
        self.texts = []
        self.moves = game.move_log
        for i, move in enumerate(self.moves):
            if i % 2 == 0:
                self.texts.append(Text(f"{1 + i//2}: {move}", 2))
                previous_move = move
            else:
                self.texts.pop()
                self.texts.append(Text(f"{1 + i//2}: {previous_move} || {move}", 2))
    
    def draw(self, window, mouse_pos):
        self.panel.draw(window)
        self.description_text_object.draw(window, self.x + self.width // 2, self.y - 30, BLACK, BACKGROUND_COLOR)

        x = self.x + self.width // 2
        y = self.y + 20

        starting_point = len(self.texts) - 23
        if starting_point < 0: starting_point = 0
        counter = 0
        for i in range(starting_point, len(self.texts)):
            self.texts[i].draw(window, x, y + 25 * (i - starting_point), BLACK, DARK_COLOR)
            counter += 1
            if counter == 23:
                break
