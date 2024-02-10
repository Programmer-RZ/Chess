import pygame

from board.const import *
from board.pieces import *

class Board:
    def __init__(self):
        self.pieces = load_pieces()

        self.board = [None]*64

        self.LoadPositionFromFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    
    def LoadPositionFromFen(self, fen):
        pieceTypeFromSymbol = {
            'k' : KING,
            'p' : PAWN,
            'n' : KNIGHT,
            'b' : BISHOP,
            'r' : ROOK,
            'q' : QUEEN
        }

        file = 0
        rank = 7

        for symbol in fen:
            if symbol == "/":
                file = 0
                rank -= 1
            else:
                if symbol.isnumeric():
                    file += int(symbol)
                else:
                    pieceColor = WHITE if symbol.isupper() else BLACK
                    pieceType = pieceTypeFromSymbol[symbol.lower()]
                    self.board[rank * 8 + file] = pieceColor | pieceType
                    file += 1

    def draw(self, window):
        for i, square in enumerate(self.board):
            x = i % 8
            y = 7 - (i - x) / 8

            color = WHITE_COLOR if (x+y) % 2 == 0 else BLACK_COLOR

            rect = pygame.Rect(x*WIDTH/8, y*HEIGHT/8, WIDTH/8, HEIGHT/8)
            pygame.draw.rect(window, color, rect)

            if square != None:
                img = pygame.transform.scale(self.pieces[square], (WIDTH/8, HEIGHT/8))

                window.blit(img, (x*WIDTH/8, y*HEIGHT/8))