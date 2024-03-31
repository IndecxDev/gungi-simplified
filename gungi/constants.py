import pygame

DEBUG = True
MOVE_LOGS = False

# Game settings:

KINGS = 1
SPIES = 2
CANNONS = 2
SAMURAIS = 2
KNIGHTS = 3
ARCHERS = 2
GENERALS = 6
FORTRESSES = 5
PAWNS = 9

MAX_PIECES_IN_PLAY = 26

# Technical settings
WIDTH, HEIGHT = 1800, 1000
ROWS, COLUMNS, LAYERS = 9, 9, 3
SQUARE_SIZE = 100
YOFFSET = 50
XOFFSET = 50

BOARD_BORDER_THICKNESS = 8
BOARD_BORDER_COLOR = (69, 39, 0)

# Colors
BACKGROUND_COLOR = (180, 160, 140)
LIGHT_COLOR = (255, 220, 169)
DARK_COLOR = (212, 183, 141)
SELECTED_COLOR = (100, 140, 255)
ENEMY_SELECTED_COLOR = (255, 153, 153)
HIGHLIGHTED_COLOR = (255, 230, 194)
MADE_MOVE_COLOR = (255, 150, 150)
IN_CHECK_COLOR = (220, 50, 50)

BUTTON_BORDER_THICKNESS = 5
BUTTON_COLOR = (212, 183, 141)
BUTTON_BORDER_COLOR = (69, 39, 0)
BUTTON_HIGHLIGHTED_COLOR = (255, 220, 169)
BUTTON_CLICKED_COLOR = (255, 230, 194)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# Piece Assets
WKING1 = pygame.image.load("assets/pieces/wK1.png")
WKING2 = pygame.image.load("assets/pieces/wK2.png")
WKING3 = pygame.image.load("assets/pieces/wK3.png")
WSPY1 = pygame.image.load("assets/pieces/wS1.png")
WSPY2 = pygame.image.load("assets/pieces/wS2.png")
WSPY3 = pygame.image.load("assets/pieces/wS3.png")
WCANNON1 = pygame.image.load("assets/pieces/wC1.png")
WCANNON2 = pygame.image.load("assets/pieces/wC2.png")
WCANNON3 = pygame.image.load("assets/pieces/wC3.png")
WSAMURAI1 = pygame.image.load("assets/pieces/wM1.png")
WSAMURAI2 = pygame.image.load("assets/pieces/wM2.png")
WSAMURAI3 = pygame.image.load("assets/pieces/wM3.png")
WKNIGHT1 = pygame.image.load("assets/pieces/wN1.png")
WKNIGHT2 = pygame.image.load("assets/pieces/wN2.png")
WKNIGHT3 = pygame.image.load("assets/pieces/wN3.png")
WARCHER1 = pygame.image.load("assets/pieces/wA1.png")
WARCHER2 = pygame.image.load("assets/pieces/wA2.png")
WARCHER3 = pygame.image.load("assets/pieces/wA3.png")
WGENERAL1 = pygame.image.load("assets/pieces/wG1.png")
WGENERAL2 = pygame.image.load("assets/pieces/wG2.png")
WGENERAL3 = pygame.image.load("assets/pieces/wG3.png")
WFORTRESS1 = pygame.image.load("assets/pieces/wF1.png")
WFORTRESS2 = pygame.image.load("assets/pieces/wF2.png")
WFORTRESS3 = pygame.image.load("assets/pieces/wF3.png")
WPAWN1 = pygame.image.load("assets/pieces/wP1.png")
WPAWN2 = pygame.image.load("assets/pieces/wP2.png")
WPAWN3 = pygame.image.load("assets/pieces/wP3.png")

BKING1 = pygame.image.load("assets/pieces/bK1.png")
BKING2 = pygame.image.load("assets/pieces/bK2.png")
BKING3 = pygame.image.load("assets/pieces/bK3.png")
BSPY1 = pygame.image.load("assets/pieces/bS1.png")
BSPY2 = pygame.image.load("assets/pieces/bS2.png")
BSPY3 = pygame.image.load("assets/pieces/bS3.png")
BCANNON1 = pygame.image.load("assets/pieces/bC1.png")
BCANNON2 = pygame.image.load("assets/pieces/bC2.png")
BCANNON3 = pygame.image.load("assets/pieces/bC3.png")
BSAMURAI1 = pygame.image.load("assets/pieces/bM1.png")
BSAMURAI2 = pygame.image.load("assets/pieces/bM2.png")
BSAMURAI3 = pygame.image.load("assets/pieces/bM3.png")
BKNIGHT1 = pygame.image.load("assets/pieces/bN1.png")
BKNIGHT2 = pygame.image.load("assets/pieces/bN2.png")
BKNIGHT3 = pygame.image.load("assets/pieces/bN3.png")
BARCHER1 = pygame.image.load("assets/pieces/bA1.png")
BARCHER2 = pygame.image.load("assets/pieces/bA2.png")
BARCHER3 = pygame.image.load("assets/pieces/bA3.png")
BGENERAL1 = pygame.image.load("assets/pieces/bG1.png")
BGENERAL2 = pygame.image.load("assets/pieces/bG2.png")
BGENERAL3 = pygame.image.load("assets/pieces/bG3.png")
BFORTRESS1 = pygame.image.load("assets/pieces/bF1.png")
BFORTRESS2 = pygame.image.load("assets/pieces/bF2.png")
BFORTRESS3 = pygame.image.load("assets/pieces/bF3.png")
BPAWN1 = pygame.image.load("assets/pieces/bP1.png")
BPAWN2 = pygame.image.load("assets/pieces/bP2.png")
BPAWN3 = pygame.image.load("assets/pieces/bP3.png")

# Indicator Assets
POSSIBLE_MOVE_VISUAL = pygame.image.load("assets/indicators/possibleMove.png")
POSSIBLE_ATTACK_VISUAL = pygame.image.load("assets/indicators/possibleAttack.png")
POSSIBLE_FRIENDLY_STACK_VISUAL = pygame.image.load("assets/indicators/possibleFriendlyStack.png")
POSSIBLE_ENEMY_STACK_VISUAL = pygame.image.load("assets/indicators/possibleEnemyStack.png")
POSSIBLE_FRIENDLY_STACK_EMPTY_VISUAL = pygame.image.load("assets/indicators/possibleFriendlyStackEmpty.png")
POSSIBLE_ENEMY_STACK_EMPTY_VISUAL = pygame.image.load("assets/indicators/possibleEnemyStackEmpty.png")
POSSIBLE_MOVE_EMPTY_VISUAL = pygame.image.load("assets/indicators/possibleMoveEmpty.png")
TWO_STACK_VISUAL_B = pygame.image.load("assets/indicators/twoStackIndicatorB.png")
TWO_STACK_VISUAL_W= pygame.image.load("assets/indicators/twoStackIndicatorW.png")
THREE_STACK_VISUAL_WW = pygame.image.load("assets/indicators/threeStackIndicatorWW.png")
THREE_STACK_VISUAL_BB = pygame.image.load("assets/indicators/threeStackIndicatorBB.png")
THREE_STACK_VISUAL_WB = pygame.image.load("assets/indicators/threeStackIndicatorWB.png")
THREE_STACK_VISUAL_BW = pygame.image.load("assets/indicators/threeStackIndicatorBW.png")

# Icons
ICON = pygame.image.load("assets/icon.png")

ICON_RESET = pygame.image.load("assets/icons/reset.png")

# Movesets
KING_MOVES = [[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)],
              [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)],
              [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]]
SPY_MOVES =  [[(0,-1),(0,1)],
              [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)],
              [(-9,-9),(0,-9),(9,-9),(-9,0),(9,0),(-9,9),(0,9),(9,9)]]
CANNON_MOVES = [[(0,-1),(0,1),(1,0),(-1,0)],
                [(0,-1),(0,1),(1,0),(-1,0),(0,-2),(0,2),(2,0),(-2,0)],
                [(0,-9),(-9,0),(9,0),(0,9)]]
SAMURAI_MOVES = [[(1,1),(1,-1),(-1,1),(-1,-1)],
                 [(1,1),(1,-1),(-1,1),(-1,-1),(2,2),(2,-2),(-2,2),(-2,-2)],
                 [(9,9),(9,-9),(-9,9),(-9,-9)]]
KNIGHT_MOVES = [[(1,0),(-1,0),(-1,-2),(1,-2)],
                [(-1,-2),(1,-2),(-2,-1),(2,-1)],
                [(-1,-2),(1,-2),(-2,-1),(2,-1),(-1,2),(1,2),(-2,1),(2,1)]]
ARCHER_MOVES = [[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)],
                [(-2,-2),(0,-2),(2,-2),(-2,0),(2,0),(-2,2),(0,2),(2,2),(-1,-2),(1,-2),(-2,-1),(2,-1),(-1,2),(1,2),(-2,1),(2,1)],
                [(-3,-3),(0,-3),(3,-3),(-3,0),(3,0),(-3,3),(0,3),(3,3),(-3,1),(-3,-1),(-3,2),(-3,-2),(3,1),(3,-1),(3,2),(3,-2),(1,3),(-1,3),(2,3),(-2,3),(1,-3),(-1,-3),(2,-3),(-2,-3)]]
GENERAL_MOVES = [[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(0,1)],
                 [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)],
                 [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1),(-1,-2),(0,-2),(1,-2)]]
FORTRESS_MOVES = [[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)],
                  [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)],
                  [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]]
PAWN_MOVES = [[(0,-1)],
              [(-1,-1),(0,-1),(1,-1)],
              [(-1,-1),(0,-1),(1,-1)]]

MAX_PIECES = KINGS + SPIES + CANNONS + SAMURAIS + KNIGHTS + ARCHERS + GENERALS + FORTRESSES + PAWNS # 32 normally