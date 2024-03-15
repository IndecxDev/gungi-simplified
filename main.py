import pygame
from gungi.constants import *
from gungi.game import Game

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Gungi")

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    if DEBUG: print("Game Started")

    # Main Game Loop
    while run:
        clock.tick(FPS)
        mousePos = pygame.mouse.get_pos()

        shift = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left Click
                    shift = False
                    if (pygame.key.get_mods() == 4097): # If shift is held
                        shift = True

                    row, column = game.board.get_board_position_from_mouse(mousePos)
                    # Check whether I clicked inside the board
                    if row >= 0 and row < ROWS and column >= 0 and column < COLUMNS:
                        game.click_board(row, column, shift)

                if event.button == 3: # Right Click
                    game.deselect()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    game.update_shift_moves(True)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    game.update_shift_moves(False)

        game.update(shift, mousePos)
        
        pygame.display.update()
    pygame.quit()

main()
