from .constants import BLACK, WHITE, DEBUG, MOVE_LOGS, GREY
from .board import Board
import random

class Game:
    def __init__(self, window) -> None:
        self._init()
        self.window = window

    def draw_game(self, mousePos):
        if self.draw: self.board.draw(self.window, self.selected, self.possible_moves, mousePos, self.turn)
        board_pos = self.board.get_board_position_from_mouse(mousePos)
        if board_pos != None:
            self.hovering_over = self.board.get_top_piece(board_pos[0], board_pos[1])

    def _init(self):
        self.selected = "--"
        self.hovering_over = None
        self.board = Board()
        self.turn = WHITE
        self.move_number = 1
        self.ply_number = 1
        self.possible_moves = []
        self.board.white_king_pos, self.board.black_king_pos = self.board.find_kings()
        self.move_log = []
        self.checkmated_state = None
        self.fifty_move_rule = 0
        self.game_message = ""
        self.draw = True # Only turn off for when simulating lots of games at once

    def reset(self):
        self._init()

    def update_shift_moves(self, shift):
        if self.selected != "--":
            self.legal_moves(self.selected, shift, True)

    def click_board(self, row, column, shift): 
        piece_clicked = self.board.get_top_piece(row, column) # Get the top piece in a stack

        if self.selected != "--" and self.selected.color == self.turn and self.checkmated_state == None: # Already selected a piece and moving it
            current_move_notation = self.board.extract_piece_type(self.selected) + str(self.board.number_to_letter(self.selected.row)) + str(self.selected.column) + "-" + str(self.selected.layer + 1)

            # Logic based on type of move
            if (row, column, "Move") in self.possible_moves:
                if DEBUG: print(str(self.selected) + " at " + str(self.selected.row) + str(self.selected.column) + str(self.selected.layer) + " moving to " + str(row) + str(column) + str(0))
                self.board.move_piece(self.selected, row, column, 0)
                self.fifty_move_rule += 1

                # Move logging
                current_move_notation += ">" + str(self.board.number_to_letter(row)) + str(column + 1) + "-1"
            elif (row, column, "Attack") in self.possible_moves or (row, column, "Enemy Stack Empty") in self.possible_moves:
                if DEBUG: print(str(self.selected) + " at " + str(self.selected.row) + str(self.selected.column) + str(self.selected.layer) + " taking " + str(piece_clicked) + " at " + str(piece_clicked.row) + str(piece_clicked.column) + str(piece_clicked.layer))
                self.board.move_piece(self.selected, row, column, piece_clicked.layer)
                self.fifty_move_rule = 0

                # Move logging
                current_move_notation += "x" + self.board.extract_piece_type(piece_clicked) + str(self.board.number_to_letter(row)) + str(column + 1) + "-" + str(piece_clicked.layer + 1)   
            elif (row, column, "Friendly Stack") in self.possible_moves:
                if DEBUG: print(str(self.selected) + " at " + str(self.selected.row) + str(self.selected.column) + str(self.selected.layer) + " friendly-stacking on " + str(piece_clicked) + " at " + str(piece_clicked.row) + str(piece_clicked.column) + str(piece_clicked.layer))
                self.board.move_piece(self.selected, row, column, piece_clicked.layer + 1)
                self.fifty_move_rule = 0

                # Move logging
                current_move_notation += "^" + self.board.extract_piece_type(piece_clicked) + str(self.board.number_to_letter(row)) + str(column + 1) + "-" + str(piece_clicked.layer + 2)
            elif (row, column, "Enemy Stack") in self.possible_moves:
                if DEBUG: print(str(self.selected) + " at " + str(self.selected.row) + str(self.selected.column) + str(self.selected.layer) + " enemy-stacking on " + str(piece_clicked) + " at " + str(piece_clicked.row) + str(piece_clicked.column) + str(piece_clicked.layer))
                self.board.move_piece(self.selected, row, column, piece_clicked.layer + 1)
                self.fifty_move_rule = 0

                # Move logging
                current_move_notation += "^" + self.board.extract_piece_type(piece_clicked) + str(self.board.number_to_letter(row)) + str(column + 1) + "-" + str(piece_clicked.layer + 2)
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

            # This will probably be bugged when a player in check gets out of check and 
            # immediately checks the other player but whatever it's not like anyone's gonna ever test this
            if self.board.player_in_check != None:
                if self.selected not in self.board.pieces_checking:
                    self.board.pieces_checking.append(self.selected)
                if self.board.checkmate_test(self.turn):
                    self.game_message = f"{self.color_to_string(self.board.switch_color(self.turn))} won by checkmate"
                    self.checkmated_state = self.turn
                    current_move_notation += "#" # Checkmate
                else:
                    current_move_notation += "+" # Check
            else:
                self.board.pieces_checking == []
            
            # Move logging
            self.move_log.append(current_move_notation) 
            if MOVE_LOGS: print(str(self.move_number) + "." + str(self.ply_number) + ":" + current_move_notation)

            # Special rules for a draw
            if self.fifty_move_rule >= 50 and self.checkmated_state == None:
                self.game_message = "Draw by 50-move rule"
                self.checkmated_state = GREY # Grey represents a draw
            elif len(self.board.get_all_pieces(False)[0]) == 1 and len(self.board.get_all_pieces(False)[1]) == 1:
                self.game_message = "Draw by insufficient material"
                self.checkmated_state = GREY

            # Ending message
            if self.game_message != "":
                print(self.game_message)

            if self.turn == WHITE: 
                self.move_number += 1 # Add 1 to move number after both players play
            self.ply_number = 1 + (self.ply_number % 2)

            if DEBUG: print(self.board)

            self.selected = "--"
            self.possible_moves = []
        elif self.checkmated_state == None: # Selecting a piece
            # If clicked on an empty square
            if piece_clicked == "--":
                self.selected = "--"
                return
            
            # Movement filtering logic
            self.legal_moves(piece_clicked, shift, True)

    def legal_moves(self, piece_clicked, shift, select_piece: bool):
        if piece_clicked.color == self.turn:
            previous_selected = self.selected
            self.selected = piece_clicked
            self.board.player_in_check = self.board.in_check(self.turn)
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

            if not select_piece:
                self.selected = previous_selected
            return self.possible_moves
        else:
            self.selected = piece_clicked
        return None

    def deselect(self):
        self.selected = "--"
        self.possible_moves = []
        if DEBUG: print("Piece deselected")
        
    def change_turn(self):
        self.turn = self.board.switch_color(self.turn)
        if self.turn == WHITE:
            if DEBUG: print("White's Turn")
        else:
            if DEBUG: print("Black's Turn")

    def make_random_move(self): # Simulates player clicks, first selects the piece, then clicks on the board to move
        if self.checkmated_state == None:
            white_pieces, black_pieces = self.board.get_all_pieces(True)
            filtered_normal_moves = []
            filtered_shift_moves = []
            chosen_piece = None
            
            if self.turn == WHITE:
                choose_tries = 0
                while filtered_normal_moves == [] and filtered_shift_moves == []:
                    choose_tries += 1
                    if choose_tries > 100:
                        self.checkmated_state = WHITE
                        print("Cannot find piece with valid moves, White Checkmated")
                        return None
                    
                    rand_num = random.randint(0, len(white_pieces) - 1)
                    chosen_piece = white_pieces[rand_num]
                    self.click_board(chosen_piece.row, chosen_piece.column, False)
                    normal_moves = self.possible_moves
                    self.click_board(chosen_piece.row, chosen_piece.column, True)
                    shift_moves = self.possible_moves

                    for move in normal_moves:
                        if "Empty" not in move[2] or "Enemy Stack Empty" in move[2]:
                            filtered_normal_moves.append(move)
                    for move in shift_moves:
                        # Special rule so that kings don't get stuck on enemy pieces unnecessarily (this is generally a bad move in a normal game)
                        if chosen_piece.type == "King" and "Enemy Stack" in move[2]:
                            continue
                        if "Empty" not in move[2]:
                            filtered_shift_moves.append(move)
            else:
                choose_tries = 0
                while filtered_normal_moves == [] and filtered_shift_moves == []:
                    choose_tries += 1
                    if choose_tries > 100:
                        self.checkmated_state = BLACK
                        print("Cannot find piece with valid moves, Black Checkmated")
                        return None
                    rand_num = random.randint(0, len(black_pieces) - 1)

                    chosen_piece = black_pieces[rand_num]
                    self.click_board(chosen_piece.row, chosen_piece.column, False)
                    normal_moves = self.possible_moves
                    self.click_board(chosen_piece.row, chosen_piece.column, True)
                    shift_moves = self.possible_moves

                    for move in normal_moves:
                        if "Empty" not in move[2] or "Enemy Stack Empty" in move[2]:
                            filtered_normal_moves.append(move)
                    for move in shift_moves:
                        # Special rule so that kings don't get stuck on enemy pieces unnecessarily (this is generally a bad move in a normal game)
                        if chosen_piece.type == "King" and "Enemy Stack" in move[2]:
                            continue
                        if "Empty" not in move[2]:
                            filtered_shift_moves.append(move)

            # 50% it will make a stack move (friendly or enemy)(if possible), otherwise a makes a normal move (move or attack)
            if (filtered_shift_moves != [] and random.randint(0, 1) == 0) or filtered_normal_moves == []:
                rand_num2 = random.randint(0, len(filtered_shift_moves) - 1)
                move = filtered_shift_moves[rand_num2]
                self.possible_moves = [move]
                self.click_board(move[0], move[1], True)
            else:
                rand_num2 = random.randint(0, len(filtered_normal_moves) - 1)
                move = filtered_normal_moves[rand_num2]
                self.possible_moves = [move]
                self.click_board(move[0], move[1], False)
        else:
            print("Cannot make move, player checkmated.")
    
    def color_to_string(self, color):
        if color == WHITE:
            return "White"
        if color == BLACK:
            return "Black"