import pygame
from .constants import BLACK, WHITE, DEBUG, MOVE_LOGS
from .board import Board

class Game:
    def __init__(self, window) -> None:
        self._init()
        self.window = window

    def draw_game(self, mousePos):
        self.board.draw(self.window, self.selected, self.possible_moves, mousePos, self.turn)

    def _init(self):
        self.selected = "--"
        self.board = Board()
        self.turn = WHITE
        self.move_number = 1
        self.ply_number = 1
        self.possible_moves = []
        self.board.white_king_pos, self.board.black_king_pos = self.board.find_kings()
        self.move_log = []
        self.checkmated = None

    def reset(self):
        self._init()

    def update_shift_moves(self, shift):
        # TODO this is mostly duplicate code from click_board() function
        if self.selected != "--" and self.selected.color == self.turn:
            if self.selected.type == "King":
                self.possible_moves = self.board.get_piece_moves(self.selected, self.turn, shift, True)
                # Test if I have the opposing player's piece under this one
                # If yes, remove it temporarily, and if one of the king's possible moves are threatening (read "would put him in check") remove that move
                if self.selected.layer >= 1:
                    if self.board.get_piece(self.selected.row, self.selected.column, self.selected.layer - 1).color == self.board.switch_color(self.turn):
                        self.board.board_map[self.selected.row][self.selected.column][self.selected.layer] = "--"
                        threat_map = self.board.get_threat_map(self.turn)
                        revised_moves = []
                        for move in self.possible_moves:
                            if threat_map[move[0]][move[1]] == 0:
                                revised_moves.append(move)
                        self.board.board_map[self.selected.row][self.selected.column][self.selected.layer] = self.selected
                        self.possible_moves = revised_moves
            elif self.board.player_in_check:
                self.possible_moves = self.board.get_piece_moves(self.selected, self.turn, shift, True) # Moves when in check
            else:
                self.possible_moves = self.board.get_piece_moves(self.selected, self.turn, shift, False) # Normal moves
                # Test if I have the opposing player's piece under this one
                # If yes, remove it temporarily, and if the king is in check under that condition, remove all possible moves
                if self.selected.layer >= 1:
                    if self.board.get_piece(self.selected.row, self.selected.column, self.selected.layer - 1).color == self.board.switch_color(self.turn):
                        self.board.board_map[self.selected.row][self.selected.column][self.selected.layer] = "--"
                        if self.board.in_check(self.turn):
                            self.possible_moves = []
                        self.board.board_map[self.selected.row][self.selected.column][self.selected.layer] = self.selected

    def click_board(self, row, column, shift): 
        piece_clicked = self.board.get_top_piece(row, column) # Get the top piece in a stack

        if self.selected != "--" and self.selected.color == self.turn: # Already selected a piece and moving it
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
                self.deselect()
                self.click_board(row, column, shift)
                return
            # Successful move happened

            # Update king position
            if self.selected.type == "King":
                if self.selected.color == WHITE:
                    self.board.white_king_pos = (row,column)
                if self.selected.color == BLACK:
                    self.board.black_king_pos = (row,column)
            if DEBUG: print("King positions: " + str(self.board.white_king_pos) + ", " + str(self.board.black_king_pos))

            self.change_turn()

            # Update check
            self.board.player_in_check = self.board.in_check(self.turn)

            # BUG This will probably be bugged when a player in check gets out of check and immediately checks the other player but whatever it's not like anyone's gonna ever test this
            if self.board.player_in_check != None:
                if self.selected not in self.board.pieces_checking:
                    self.board.pieces_checking.append(self.selected)
                if self.board.checkmate_test(self.turn):
                    print("CHECKMATE")
            else:
                self.board.pieces_checking == []
    
            # Move logging
            self.move_log.append(current_move_notation) 
            if MOVE_LOGS: print(str(self.move_number) + "." + str(self.ply_number) + ":" + current_move_notation)

            if self.turn == WHITE: self.move_number += 1 # Add 1 to move number after both players play
            self.ply_number = 1 + (self.ply_number % 2)

            if DEBUG: print(self.board)
            self.selected = "--"
            self.possible_moves = []
        else: # Selecting a piece
            # If clicked on an empty square
            if piece_clicked == "--": 
                return
            
            # If clicked on my piece (Movement filtering logic)
            if piece_clicked.color == self.turn: 
                self.selected = piece_clicked
                self.board.player_in_check = self.board.in_check(self.turn)
                if self.selected.type == "King":
                    self.possible_moves = self.board.get_piece_moves(self.selected, self.turn, shift, True)
                    # Test if I have the opposing player's piece under this one
                    # If yes, remove it temporarily, and if one of the king's possible moves are threatening (read "would put him in check") remove that move
                    if self.selected.layer >= 1:
                        if self.board.get_piece(row, column, self.selected.layer - 1).color == self.board.switch_color(self.turn):
                            self.board.board_map[row][column][self.selected.layer] = "--"
                            threat_map = self.board.get_threat_map(self.turn)
                            revised_moves = []
                            for move in self.possible_moves:
                                if threat_map[move[0]][move[1]] == 0:
                                    revised_moves.append(move)
                            self.board.board_map[row][column][self.selected.layer] = self.selected
                            self.possible_moves = revised_moves
                elif self.board.player_in_check:
                    self.possible_moves = self.board.get_piece_moves(self.selected, self.turn, shift, True) # Moves when in check
                else:
                    self.possible_moves = self.board.get_piece_moves(self.selected, self.turn, shift, False) # Normal moves
                    # Test if I have the opposing player's piece under this one
                    # If yes, remove it temporarily, and if the king is in check under that condition, remove all possible moves
                    if self.selected.layer >= 1:
                        if self.board.get_piece(row, column, self.selected.layer - 1).color == self.board.switch_color(self.turn):
                            self.board.board_map[row][column][self.selected.layer] = "--"
                            if self.board.in_check(self.turn):
                                self.possible_moves = []
                            self.board.board_map[row][column][self.selected.layer] = self.selected
                
                if DEBUG: print(str(piece_clicked) + " at " + str(row) + str(column) + str(piece_clicked.layer) + " selected")
            else:
                self.selected = piece_clicked
                if DEBUG: print(str(piece_clicked) + " at " + str(row) + str(column) + str(piece_clicked.layer) + " is not your piece")
                return

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