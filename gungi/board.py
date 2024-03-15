import pygame
import time
from .constants import *
from .piece import Piece
import datetime

class Board:
    def __init__(self):
        self.board_map = []
        self.create_board()

    def get_board_position_from_mouse(self, pos):
        x, y = pos
        row = (y - YOFFSET) // SQUARE_SIZE
        column = (x - XOFFSET) // SQUARE_SIZE
        return row, column

    # Creating the array that has all of the pieces
    def create_board(self): 
        self.board_map = self.convert_notation_to_board([
            [["--", "--", "--"],["--", "--", "--"],["bM", "--", "--"],["bF", "bC", "--"],["bK", "--", "--"],["bF", "bP", "bA"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"]],
            [["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["bP", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"]],
            [["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"]],
            [["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"]],
            [["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"]],
            [["--", "--", "--"],["wF", "wP", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"]],
            [["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"]],
            [["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"],["wA", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"]],
            [["--", "--", "--"],["wG", "wN", "wS"],["--", "--", "--"],["wM", "--", "--"],["wK", "--", "--"],["wP", "--", "--"],["--", "--", "--"],["--", "--", "--"],["--", "--", "--"]]])
        
    def convert_notation_to_board(self, board):
        piece_color = None
        piece_type = ""
        for row in range(ROWS):
            for column in range(COLUMNS):
                for layer in range(LAYERS):
                    if board[row][column][layer][0] == "b":
                        piece_color = BLACK
                    elif board[row][column][layer][0] == "w":
                        piece_color = WHITE
                    else:
                        board[row][column][layer] = "--"
                        continue
                    
                    if board[row][column][layer][1] == "K":
                        piece_type = "King"
                    if board[row][column][layer][1] == "S":
                        piece_type = "Spy"
                    if board[row][column][layer][1] == "C":
                        piece_type = "Cannon"
                    if board[row][column][layer][1] == "M":
                        piece_type = "Samurai"
                    if board[row][column][layer][1] == "N":
                        piece_type = "Knight"
                    if board[row][column][layer][1] == "A":
                        piece_type = "Archer"
                    if board[row][column][layer][1] == "F":
                        piece_type = "Fortress"
                    if board[row][column][layer][1] == "G":
                        piece_type = "General"
                    if board[row][column][layer][1] == "P":
                        piece_type = "Pawn"

                    board[row][column][layer] = Piece(row, column, layer, piece_color, piece_type)
    
        return board

    # Returns whatever is on the position (Piece object or "--" if nothing is there)
    def get_piece(self, row, column, layer):
        return self.board_map[row][column][layer]
    
    def get_top_piece(self, row, column): # Returns the top piece in a stack
        for layer in range(LAYERS - 1, -1, -1):
            piece = self.get_piece(row, column, layer)
            if piece != "--":
                return piece
        return "--"

    # Move a piece to a precise location (doesn't care about what it's replacing)
    def move_piece(self, piece, row, column, layer):
        self.board_map[row][column][layer] = self.board_map[piece.row][piece.column][piece.layer]
        self.board_map[piece.row][piece.column][piece.layer] = "--"
        piece.move(row, column, layer)
    
    # Drawing the board and pieces
    def draw(self, window, selected, moves, mousePos):

        # Draw the board
        window.fill(BACKGROUND_COLOR)
        pygame.draw.rect(window, BOARD_BORDER_COLOR, (XOFFSET - BOARD_BORDER_THICKNESS, YOFFSET - BOARD_BORDER_THICKNESS, ROWS * SQUARE_SIZE + 2 * BOARD_BORDER_THICKNESS, COLUMNS * SQUARE_SIZE + 2 * BOARD_BORDER_THICKNESS), BOARD_BORDER_THICKNESS, 10, 10, 10, 10)
        for row in range(ROWS):
            for column in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, DARK_COLOR, (row * SQUARE_SIZE + XOFFSET, column * SQUARE_SIZE + YOFFSET, SQUARE_SIZE, SQUARE_SIZE))
            for column in range((row + 1) % 2, ROWS, 2):
                pygame.draw.rect(window, LIGHT_COLOR, (row * SQUARE_SIZE + XOFFSET, column * SQUARE_SIZE + YOFFSET, SQUARE_SIZE, SQUARE_SIZE))
                
        

        # If I have a piece selected, make the square under it blue
        if selected != "--":
            pygame.draw.rect(window, SELECTED_COLOR, (selected.column * SQUARE_SIZE + XOFFSET, selected.row * SQUARE_SIZE + YOFFSET, SQUARE_SIZE, SQUARE_SIZE))

        #Draw the pieces
        for row in range(ROWS):
            for column in range(COLUMNS):
                for layer in range(LAYERS):
                    piece = self.board_map[row][column][layer]
                    if piece != "--":
                        # Draw the piece itself
                        piece.draw(window)

                        # Draw the stack indicators
                        if layer == 1:
                            if self.board_map[row][column][0].color == BLACK:
                                window.blit(TWO_STACK_VISUAL_B, (piece.x, piece.y))
                            else:
                                window.blit(TWO_STACK_VISUAL_W, (piece.x, piece.y))
                            
                        if layer == 2:
                            if self.board_map[row][column][0].color == BLACK:
                                if self.board_map[row][column][1].color == BLACK:
                                    window.blit(THREE_STACK_VISUAL_BB, (piece.x, piece.y))
                                else:
                                    window.blit(THREE_STACK_VISUAL_BW, (piece.x, piece.y))
                            else:
                                if self.board_map[row][column][1].color == BLACK:
                                    window.blit(THREE_STACK_VISUAL_WB, (piece.x, piece.y))
                                else:
                                    window.blit(THREE_STACK_VISUAL_WW, (piece.x, piece.y))
        
        # Draw the possible moves for the selected piece
        for move in moves:
            if type(move) == str: 
                continue

            moveArgument = (move[1] * SQUARE_SIZE + XOFFSET, move[0] * SQUARE_SIZE + YOFFSET)
            if (move[2] == "Move"):
                window.blit(POSSIBLE_MOVE_VISUAL, moveArgument)
            elif(move[2] == "Attack"):
                window.blit(POSSIBLE_ATTACK_VISUAL, moveArgument)
            elif(move[2] == "Friendly Stack"):
                window.blit(POSSIBLE_FRIENDLY_STACK_VISUAL, moveArgument)
            elif(move[2] == "Enemy Stack"):
                window.blit(POSSIBLE_ENEMY_STACK_VISUAL, moveArgument)
            elif(move[2] == "Friendly Stack Empty"):
                window.blit(POSSIBLE_FRIENDLY_STACK_EMPTY_VISUAL, moveArgument)
            elif(move[2] == "Enemy Stack Empty"):
                window.blit(POSSIBLE_ENEMY_STACK_EMPTY_VISUAL, moveArgument)
            elif(move[2] == "Move Empty"):
                window.blit(POSSIBLE_MOVE_EMPTY_VISUAL, moveArgument)
                    
    def get_piece_moves(self, piece, turn, shift):
        valid_moves = []
        moveset = []

        if piece.type == "King":
            moveset = KING_MOVES
        elif piece.type == "Spy":
            moveset = SPY_MOVES
        elif piece.type == "Cannon":
            moveset = CANNON_MOVES
        elif piece.type == "Samurai":
            moveset = SAMURAI_MOVES
        elif piece.type == "Knight":
            moveset = KNIGHT_MOVES
        elif piece.type == "Archer":
            moveset = ARCHER_MOVES
        elif piece.type == "General":
            moveset = GENERAL_MOVES
        elif piece.type == "Fortress":
            moveset = FORTRESS_MOVES
        elif piece.type == "Pawn":
            moveset = PAWN_MOVES

        for possible_move in moveset[piece.layer]:
                if 9 in possible_move or -9 in possible_move: # Checking for infinite movement
                    nine_moves = self._nine_moves(possible_move, piece, turn, shift)
                    for nine_move in nine_moves:
                        valid_moves.append(nine_move)
                else: # Normal moves
                    valid_move = self._check_and_format_move(possible_move, piece, turn, shift)
                    if (valid_move != "x"):
                        valid_moves.append(valid_move)

        if DEBUG: print("Valid moves for " + str(piece) + str(piece.row) + str(piece.column) + str(piece.layer) + ": " + str(valid_moves))
        return valid_moves

    # TODO Second part of this function is unreadable shit
    # Check what type of move would it be for a space
    def _check_and_format_move(self, possible_move, piece, turn, shift):
        if turn == BLACK: # Flip the moveset for black
            reversed_y = possible_move[1] * -1
            possible_move = (possible_move[0], reversed_y)

        checking_x = piece.row + possible_move[1]
        checking_y = piece.column + possible_move[0]
        state = ""

        # If the checked position is out of bounds, skip
        if checking_x > (ROWS - 1) or checking_x < 0:
            return "x"
        if checking_y > (COLUMNS - 1) or checking_y < 0:
            return "x"

        # Get the piece at the checked position
        target_piece = self.get_top_piece(checking_x, checking_y)
        # Move logic
        if target_piece != "--":
            # Check for too high of a stack
            if target_piece.layer >= (LAYERS - 1) and target_piece.color == turn:
                return "x"
            
            # !!! THIS IS AN UNDREADABLE BODGED MESS, DO NOT TOUCH UNLESS ABSOLUTELY NECESSARY
            if target_piece.color != turn: # Looking at enemy piece
                if not shift:
                    if target_piece.layer < LAYERS - 1 and piece.type != "Fortress" and target_piece.type != "King":
                        state = "Enemy Stack Empty"
                    else:
                        state = "Attack"
                elif target_piece.layer < LAYERS - 1 and piece.type != "Fortress" and target_piece.type != "King":
                    state = "Enemy Stack"
                elif target_piece.type != "King":
                    return "x"
                else:
                    return "xKing"
            else: # Looking at friendly piece
                if piece.type != "Fortress" and target_piece.type != "King":
                    if not shift:
                        state = "Friendly Stack Empty"
                    else:
                        state = "Friendly Stack"
                else:
                    return "x"
        elif not shift:
            state = "Move"
        else:
            state = "Move Empty"
            pass

        return (piece.row + possible_move[1], piece.column + possible_move[0], state)

    def _nine_moves(self, possible_move, piece, turn, shift):
        moves = []
        sign_x = possible_move[0] // 9
        sign_y = possible_move[1] // 9

        for i in range(1, 10):
            if sign_x * sign_y != 0: # Diagonals
                valid_move = self._check_and_format_move((i * sign_x, i * sign_y), piece, turn, shift)
                if (valid_move != "x"):
                    moves.append(valid_move)
                    if valid_move[2] == "Attack" and self.get_top_piece(valid_move[0],valid_move[1]).layer == 2 and MAX_STACKS_BLOCK_SIGHT:
                        break
                elif MAX_STACKS_BLOCK_SIGHT:
                    break
            elif sign_x == 0: # Columns
                valid_move = self._check_and_format_move((possible_move[0], i * sign_y), piece, turn, shift)
                if (valid_move != "x"):
                    moves.append(valid_move)
                    if valid_move[2] == "Attack" and self.get_top_piece(valid_move[0],valid_move[1]).layer == 2 and MAX_STACKS_BLOCK_SIGHT:
                        break
                elif MAX_STACKS_BLOCK_SIGHT:
                    break
            elif sign_y == 0: # Rows
                valid_move = self._check_and_format_move((i * sign_x, possible_move[1]), piece, turn, shift)
                if (valid_move != "x"):
                    moves.append(valid_move)
                    if valid_move[2] == "Attack" and self.get_top_piece(valid_move[0],valid_move[1]).layer == 2 and MAX_STACKS_BLOCK_SIGHT:
                        break
                elif MAX_STACKS_BLOCK_SIGHT:
                    break
            
        return moves

    # TODO Inefficient function. Eventually change this to keep track of all pieces on the board for each player and not just going through the entire board.
    # DEPRECATED
    def test_for_check(self, board_to_check): # Returns the color of the player that's in check

        start_time = datetime.datetime.now()

        players = [WHITE,BLACK]
        king = ""
        in_check = "x"
        checking_pieces = []

        for player in players:
            for row in range(ROWS):
                for column in range(COLUMNS):
                    piece = board_to_check.get_top_piece(row, column)
                    if piece != "--":
                        if piece.type == "King" and piece.color != player:
                            king = piece
                            break   
            
            for row in range(ROWS):
                for column in range(COLUMNS):
                    piece = board_to_check.get_top_piece(row, column)
                    if piece != "--":
                        if piece.color == player:
                            moveset = board_to_check.get_piece_moves(piece, player, False)
                            for move in moveset:
                                if move[2] == "Attack" and move[0] == king.row and move[1] == king.column:
                                    in_check = self.switch_color(player)
                                    checking_pieces.append(piece)

        end_time = datetime.datetime.now()
        print("Amount of frames this shitty code takes: " + str(((end_time - start_time).microseconds/1000)/(1000/60.0)))

        return (in_check, checking_pieces)
    
    def get_threat_map(self, player_color):
        threat_map = []
        
        for j in range(ROWS):
            section = []
            for i in range(COLUMNS):
                section.append(0)
            threat_map.append(section)

        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.get_top_piece(row, column)
                if piece != "--" and piece.color == player_color:
                    move_set = self.get_piece_moves(piece, player_color, False)
                    for move in move_set:
                        threat_map[move[0]][move[1]] += 1

        if DEBUG: print("Threat map for " + str(player_color) + " is: " + str(threat_map))
        return threat_map


    def switch_color(self, color):
        if color == WHITE:
            return BLACK
        else:
            return WHITE

    # For visualizing in the terminal
    def __repr__(self) -> str:
        state = ""
        for row in range(ROWS):
            state += "\n"
            for column in range(COLUMNS):
                state += "| "
                for layer in range(LAYERS):
                    piece = self.get_piece(row, column, layer)
                    state += str(piece) + " "
        return state
    
