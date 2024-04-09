from .constants import BLACK, WHITE, DEBUG, MOVE_LOGS
from .board import Board
import random
import copy

class Game:
    def __init__(self, window) -> None:
        self._init()
        self.window = window

    def draw_game(self, mousePos):
        self.board.draw(self.window, self.selected, self.possible_moves, mousePos, self.turn)
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
        self.checkmated = None

    def reset(self):
        self._init()

    def update_shift_moves(self, shift):
        if self.selected != "--":
            self.legal_moves(self.selected, shift, True)

    def click_board(self, row, column, shift): 
        piece_clicked = self.board.get_top_piece(row, column) # Get the top piece in a stack

        if self.selected != "--" and self.selected.color == self.turn and self.checkmated == None: # Already selected a piece and moving it
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

            # BUG This will probably be bugged when a player in check gets out of check and 
            # immediately checks the other player but whatever it's not like anyone's gonna ever test this
            if self.board.player_in_check != None:
                if self.selected not in self.board.pieces_checking:
                    self.board.pieces_checking.append(self.selected)
                if self.board.checkmate_test(self.turn):
                    print("CHECKMATE")
                    self.checkmated = self.turn
            else:
                self.board.pieces_checking == []
    
            # Move logging
            self.move_log.append(current_move_notation) 
            if MOVE_LOGS: print(str(self.move_number) + "." + str(self.ply_number) + ":" + current_move_notation)

            if self.turn == WHITE: 
                self.move_number += 1 # Add 1 to move number after both players play
            self.ply_number = 1 + (self.ply_number % 2)

            if DEBUG: print(self.board)

            self.selected = "--"
            self.possible_moves = []
        else: # Selecting a piece
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
            print("White's Turn")
        else:
            print("Black's Turn")

    # TODO
    def make_random_move(self):
        if self.checkmated == None:
            white_pieces, black_pieces = self.board.get_all_moveable_pieces()
            filtered_normal_moves = []
            filtered_shift_moves = []
            if self.turn == WHITE:
                while filtered_normal_moves == [] and filtered_shift_moves == []:
                    rand_num = random.randint(0, len(white_pieces) - 1)

                    self.click_board(white_pieces[rand_num].row, white_pieces[rand_num].column, False)
                    normal_moves = self.possible_moves
                    self.click_board(white_pieces[rand_num].row, white_pieces[rand_num].column, True)
                    shift_moves = self.possible_moves

                    for move in normal_moves:
                        if "Empty" not in move[2] or "Enemy Stack Empty" in move[2]:
                            filtered_normal_moves.append(move)
                    for move in shift_moves:
                        if "Empty" not in move[2]:
                            filtered_shift_moves.append(move)
            else:
                while filtered_normal_moves == [] and filtered_shift_moves == []:
                    rand_num = random.randint(0, len(black_pieces) - 1)

                    self.click_board(black_pieces[rand_num].row, black_pieces[rand_num].column, False)
                    normal_moves = self.possible_moves
                    self.click_board(black_pieces[rand_num].row, black_pieces[rand_num].column, True)
                    shift_moves = self.possible_moves

                    for move in normal_moves:
                        if "Empty" not in move or "Enemy Stack Empty" in move:
                            filtered_normal_moves.append(move)
                    for move in shift_moves:
                        if "Empty" not in move:
                            filtered_shift_moves.append(move)

            previous_board = copy.deepcopy(self.board)

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
            
            if previous_board == self.board:
                print("something went wrong")

        else:
            print("Cannot make move, player checkmated.")
            