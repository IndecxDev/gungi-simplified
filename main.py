import pygame
from gungi.constants import *
from gungi.game import Game

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Gungi")

def get_board_position_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    column = x // SQUARE_SIZE
    return row, column

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    if DEBUG: print("Game Started")

    # Main Game Loop
    while run:
        clock.tick(FPS)

        shift = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left Click
                    shift = False
                    if (pygame.key.get_mods() == 4097): # If shift is held
                        shift = True

                    pos = pygame.mouse.get_pos()
                    row, column = get_board_position_from_mouse(pos)
                    game.click_board(row, column, shift)

                if event.button == 3: # Right Click
                    game.deselect()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    game.update_shift_moves(True)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    game.update_shift_moves(False)

        game.update(shift)
        
        pygame.display.update()
    pygame.quit()

main()
