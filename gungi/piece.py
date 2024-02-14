from .constants import *

class Piece:
    PADDING = 20
    OUTLINE = 2
    
    def __init__(self, row, column, layer, color, type) -> None:
        self.row = row
        self.column = column
        self.layer = layer
        self.color = color
        self.type = type

        self.x = 0
        self.y = 0
        self.calculate_pos()
        
    def calculate_pos(self):
        self.x = SQUARE_SIZE * self.column
        self.y = SQUARE_SIZE * self.row

    def draw(self, window):
        if self.color == WHITE:
            if self.type == "King":
                if self.layer == 0:
                    window.blit(WKING1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(WKING2, (self.x, self.y))
                else:
                    window.blit(WKING3, (self.x, self.y))
            if self.type == "Spy":
                if self.layer == 0:
                    window.blit(WSPY1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(WSPY2, (self.x, self.y))
                else:
                    window.blit(WSPY3, (self.x, self.y))
            if self.type == "Cannon":
                if self.layer == 0:
                    window.blit(WCANNON1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(WCANNON2, (self.x, self.y))
                else:
                    window.blit(WCANNON3, (self.x, self.y))
            if self.type == "Samurai":
                if self.layer == 0:
                    window.blit(WSAMURAI1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(WSAMURAI2, (self.x, self.y))
                else:
                    window.blit(WSAMURAI3, (self.x, self.y))
            if self.type == "Knight":
                if self.layer == 0:
                    window.blit(WKNIGHT1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(WKNIGHT2, (self.x, self.y))
                else:
                    window.blit(WKNIGHT3, (self.x, self.y))
            if self.type == "Archer":
                if self.layer == 0:
                    window.blit(WARCHER1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(WARCHER2, (self.x, self.y))
                else:
                    window.blit(WARCHER3, (self.x, self.y))
            if self.type == "General":
                if self.layer == 0:
                    window.blit(WGENERAL1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(WGENERAL2, (self.x, self.y))
                else:
                    window.blit(WGENERAL3, (self.x, self.y))
            if self.type == "Fortress":
                if self.layer == 0:
                    window.blit(WFORTRESS1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(WFORTRESS2, (self.x, self.y))
                else:
                    window.blit(WFORTRESS3, (self.x, self.y))
            if self.type == "Pawn":
                if self.layer == 0:
                    window.blit(WPAWN1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(WPAWN2, (self.x, self.y))
                else:
                    window.blit(WPAWN3, (self.x, self.y))
        else:
            if self.type == "King":
                if self.layer == 0:
                    window.blit(BKING1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(BKING2, (self.x, self.y))
                else:
                    window.blit(BKING3, (self.x, self.y))
            if self.type == "Spy":
                if self.layer == 0:
                    window.blit(BSPY1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(BSPY2, (self.x, self.y))
                else:
                    window.blit(BSPY3, (self.x, self.y))
            if self.type == "Cannon":
                if self.layer == 0:
                    window.blit(BCANNON1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(BCANNON2, (self.x, self.y))
                else:
                    window.blit(BCANNON3, (self.x, self.y))
            if self.type == "Samurai":
                if self.layer == 0:
                    window.blit(BSAMURAI1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(BSAMURAI2, (self.x, self.y))
                else:
                    window.blit(BSAMURAI3, (self.x, self.y))
            if self.type == "Knight":
                if self.layer == 0:
                    window.blit(BKNIGHT1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(BKNIGHT2, (self.x, self.y))
                else:
                    window.blit(BKNIGHT3, (self.x, self.y))
            if self.type == "Archer":
                if self.layer == 0:
                    window.blit(BARCHER1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(BARCHER2, (self.x, self.y))
                else:
                    window.blit(BARCHER3, (self.x, self.y))
            if self.type == "General":
                if self.layer == 0:
                    window.blit(BGENERAL1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(BGENERAL2, (self.x, self.y))
                else:
                    window.blit(BGENERAL3, (self.x, self.y))
            if self.type == "Fortress":
                if self.layer == 0:
                    window.blit(BFORTRESS1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(BFORTRESS2, (self.x, self.y))
                else:
                    window.blit(BFORTRESS3, (self.x, self.y))
            if self.type == "Pawn":
                if self.layer == 0:
                    window.blit(BPAWN1, (self.x, self.y))
                elif self.layer == 1:
                    window.blit(BPAWN2, (self.x, self.y))
                else:
                    window.blit(BPAWN3, (self.x, self.y))

    def move(self, row, column, layer):
        self.row = row
        self.column = column
        self.layer = layer
        self.calculate_pos()

    def __repr__(self) -> str:
        if (self.color == WHITE):
            if self.type == "King":
                return "wK"
            if self.type == "Spy":
                return "wS"
            if self.type == "Cannon":
                return "wC"
            if self.type == "Samurai":
                return "wM"
            if self.type == "Knight":
                return "wN"
            if self.type == "Archer":
                return "wA"
            if self.type == "General":
                return "wG"
            if self.type == "Fortress":
                return "wF"
            if self.type == "Pawn":
                return "wP"
        else:
            if self.type == "King":
                return "bK"
            if self.type == "Spy":
                return "bS"
            if self.type == "Cannon":
                return "bC"
            if self.type == "Samurai":
                return "bM"
            if self.type == "Knight":
                return "bN"
            if self.type == "Archer":
                return "bA"
            if self.type == "General":
                return "bG"
            if self.type == "Fortress":
                return "bF"
            if self.type == "Pawn":
                return "bP"