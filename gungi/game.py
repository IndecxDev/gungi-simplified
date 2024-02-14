import pygame
from .constants import BLACK, WHITE, DEBUG, MOVE_LOGS
from .board import Board

class Game:
    def __init__(self, window) -> None:
        self._init()
        self.window = window

    def update(self, shift):
        self.board.draw(self.window, self.selected, self.possible_moves)
        pygame.display.update()

    def _init(self):
        self.selected = "--"
        self.board = Board()
        self.turn = WHITE
        self.move_number = 1
        self.ply_number = 1
        self.possible_moves = []
        self.white_king_pos = ()
        self.black_king_pos = ()

        self.move_log = []

        self.in_check = "x"

    def reset(self):
        self._init()

    def update_shift_moves(self, shift):
        if self.selected != "--": 
            self.possible_moves = self.board.get_piece_moves(self.selected, self.turn, shift)

    def click_board(self, row, column, shift): 
        piece_clicked = self.board.get_top_piece(row, column) # Get the top piece in a stack

        if self.selected == "--": # Selecting a piece
            # If clicked on an empty square
            if piece_clicked == "--": 
                return
            
            # If the piece is my color
            if piece_clicked.color == self.turn: 
                self.selected = piece_clicked
                self.possible_moves = self.board.get_piece_moves(self.selected, self.turn, shift) # Get the valid moves for the piece

                # TODO Maybe use a threat map instead of this https://levelup.gitconnected.com/finding-all-legal-chess-moves-2cb872d05bc6 https://peterellisjones.com/posts/generating-legal-chess-moves-efficiently/

                # Test for each move to see if it would put me in check
                """
                for move in self.possible_moves:
                    if move[0] == "x": continue
                    piece_targetted = self.board.get_top_piece(move[0], move[1])

                    # Temporarily moving the piece to test for check
                    if piece_targetted != "--":
                        if move[2] == "Friendly Stack Empty" or move[2] == "Enemy Stack Empty": # Both stacks
                            self.board.board_map[piece_clicked.row][piece_clicked.column][piece_clicked.layer] = "--"
                            self.board.board_map[piece_targetted.row][piece_targetted.column][piece_targetted.layer + 1] = piece_clicked
                        else: # Attack
                            self.board.board_map[piece_clicked.row][piece_clicked.column][piece_clicked.layer] = "--"
                            self.board.board_map[piece_targetted.row][piece_targetted.column][piece_targetted.layer] = piece_clicked
                    else: # Move
                        self.board.board_map[piece_clicked.row][piece_clicked.column][piece_clicked.layer] = "--"
                        self.board.board_map[move[0]][move[1]][0] = piece_clicked
                    
                    # Remove possible move if it puts me in check
                    if self.board.test_for_check(self.board)[0] == self.turn:
                        self.possible_moves[self.possible_moves.index(move)] = (move[0], move[1], "x") # Doesn't really remove, just flags it and therefore the move doesn't show

                    # Then moving it back to the original position
                    if piece_targetted != "--":
                        if move[2] == "Friendly Stack Empty" or move[2] == "Enemy Stack Empty": # Both stacks
                            self.board.board_map[piece_targetted.row][piece_targetted.column][piece_targetted.layer + 1] = "--"
                        else: # Attack
                            self.board.board_map[piece_targetted.row][piece_targetted.column][piece_targetted.layer] = piece_targetted
                    else: # Move
                        self.board.board_map[move[0]][move[1]][0] = "--"

                    self.board.board_map[piece_clicked.row][piece_clicked.column][piece_clicked.layer] = piece_clicked
                """
                if DEBUG: print(str(piece_clicked) + " at " + str(row) + str(column) + str(piece_clicked.layer) + " selected")
            else:
                if DEBUG: print(str(piece_clicked) + " at " + str(row) + str(column) + str(piece_clicked.layer) + " is not your piece")
                return
        else: # Moving a piece 
            
            current_move_notation = str(self.selected) + " " + str(self.selected.row) + str(self.selected.column) + str(self.selected.layer + 1)

            # Logic based on type of move
            if (row, column, "Move") in self.possible_moves:
                if DEBUG: print(str(self.selected) + " at " + str(self.selected.row) + str(self.selected.column) + str(self.selected.layer) + " moving to " + str(row) + str(column) + str(0))
                self.board.move_piece(self.selected, row, column, 0)

                # Move logging
                current_move_notation += " > " + str(row + 1) + str(column + 1) + "1"
            elif (row, column, "Attack") in self.possible_moves or (row, column, "Enemy Stack Empty") in self.possible_moves:
                if DEBUG: print(str(self.selected) + " at " + str(self.selected.row) + str(self.selected.column) + str(self.selected.layer) + " taking " + str(piece_clicked) + " at " + str(piece_clicked.row) + str(piece_clicked.column) + str(piece_clicked.layer))
                self.board.move_piece(self.selected, row, column, piece_clicked.layer)

                # Move logging
                current_move_notation += " x " + str(piece_clicked) + " " + str(row + 1) + str(column + 1) + str(piece_clicked.layer + 1)   
            elif (row, column, "Friendly Stack") in self.possible_moves:
                if DEBUG: print(str(self.selected) + " at " + str(self.selected.row) + str(self.selected.column) + str(self.selected.layer) + " friendly-stacking on " + str(piece_clicked) + " at " + str(piece_clicked.row) + str(piece_clicked.column) + str(piece_clicked.layer))
                self.board.move_piece(self.selected, row, column, piece_clicked.layer + 1)

                # Move logging
                current_move_notation += " ^ " + str(piece_clicked) + " " + str(row + 1) + str(column + 1) + str(piece_clicked.layer + 2)
            elif (row, column, "Enemy Stack") in self.possible_moves:
                if DEBUG: print(str(self.selected) + " at " + str(self.selected.row) + str(self.selected.column) + str(self.selected.layer) + " enemy-stacking on " + str(piece_clicked) + " at " + str(piece_clicked.row) + str(piece_clicked.column) + str(piece_clicked.layer))
                self.board.move_piece(self.selected, row, column, piece_clicked.layer + 1)
                
                # Move logging
                current_move_notation += " ^ " + str(piece_clicked) + " " + str(row + 1) + str(column + 1) + str(piece_clicked.layer + 2)
            else:
                return
            
            if DEBUG: print(self.board.test_for_check(self.board))

            self.change_turn()

            # Move logging
            self.move_log.append(current_move_notation) 
            if MOVE_LOGS: print(str(self.move_number) + "." + str(self.ply_number) + ":" + current_move_notation)

            if self.turn == WHITE: self.move_number += 1 # Add 1 to move number after both players play
            self.ply_number = 1 + (self.ply_number % 2)

            if DEBUG: print(self.board)
            self.selected = "--"
            self.possible_moves = []

    def deselect(self):
        self.selected = "--"
        self.possible_moves = []
        if DEBUG: print("Piece deselected")
        
    def change_turn(self):
        self.turn = self.board.switch_color(self.turn)
        if self.turn == WHITE:
            print("White's Turn")
        else:
            print("Black's Turn")