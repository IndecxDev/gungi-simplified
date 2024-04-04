import pygame

class Text:
    def __init__(self, text: str, size: int) -> None:
        self.size = size
        self.font = pygame.font.Font("assets/coolvetica.otf", self.size)
        self.text = text
    
    def draw(self, window, center_x, center_y, color, background_color):
        if self.text != "":
            text = self.font.render(self.text, True, color, background_color)
            textRect = text.get_rect()
            textRect.center = (center_x, center_y)
            window.blit(text, textRect)
    
    def change_font_size(self, new_size):
        self.font = pygame.font.Font("assets/coolvetica.otf", new_size)
        self.size = new_size