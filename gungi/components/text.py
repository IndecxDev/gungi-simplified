import pygame

smallFont = pygame.font.Font("assets/coolvetica.otf", 18)
bigFont = pygame.font.Font("assets/coolvetica.otf", 30)
moveLogFont = pygame.font.Font("assets/coolvetica.otf", 20)

class Text:
    def __init__(self, text: str, size: int) -> None:
        self.size = size
        if size == 0:
            self.font = smallFont
        elif size == 1:
            self.font = bigFont
        elif size == 2:
            self.font = moveLogFont
        self.text = text
    
    def draw(self, window, center_x, center_y, color, background_color):
        if self.text != "":
            text = self.font.render(self.text, True, color, background_color)
            textRect = text.get_rect()
            textRect.center = (center_x, center_y)
            window.blit(text, textRect)